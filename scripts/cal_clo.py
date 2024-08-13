
import json
import os
import pandas as pd
import numpy as np

from collections import defaultdict
from tqdm import tqdm

def parse_json_files(directory):
    battles = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                content = json.load(file)
                
                # Filter only the relevant models and tie
                models = [model for model in content if model not in ["tie", "unable to decide: situation one", "unable to decide: situation two", "unable to decide", "total"]]
                tie_count = content.get("tie", 0)
                
                # Generate battles based on win counts
                for model_a in models:
                    for model_b in models:
                        if model_a == model_b:
                            continue
                        
                        # Add battles based on the counts
                        wins_a = content.get(model_a, 0)
                        wins_b = content.get(model_b, 0)
                        
                        if wins_a > 0:
                            battles.append({'model_a': model_a, 'model_b': model_b, 'winner': 'model_a', 'count': wins_a})
                        if wins_b > 0:
                            battles.append({'model_a': model_a, 'model_b': model_b, 'winner': 'model_b', 'count': wins_b})
                        
                        # Add tie counts if applicable
                        if tie_count > 0:
                            battles.append({'model_a': model_a, 'model_b': model_b, 'winner': 'tie', 'count': tie_count})
    
    # Create DataFrame from the list of battles, keeping the 'count' column
    return pd.DataFrame(battles)



def compute_elo(battles, K=4, SCALE=400, BASE=10, INIT_RATING=1000):
    rating = defaultdict(lambda: INIT_RATING)

    for _, model_a, model_b, winner, count in battles[['model_a', 'model_b', 'winner', 'count']].itertuples():
        ra = rating[model_a]
        rb = rating[model_b]
        ea = 1 / (1 + BASE ** ((rb - ra) / SCALE))
        eb = 1 / (1 + BASE ** ((ra - rb) / SCALE))
        if winner == "model_a":
            sa = 1
        elif winner == "model_b":
            sa = 0
        elif winner == "tie":
            sa = 0.5
        else:
            raise Exception(f"unexpected vote {winner}")
        rating[model_a] += K * count * (sa - ea)
        rating[model_b] += K * count * (1 - sa - eb)

    return rating

def get_bootstrap_result(battles, func_compute_elo, num_round):
    rows = []
    for _ in tqdm(range(num_round), desc="bootstrap"):
        sample_battles = battles.sample(frac=1.0, replace=True)
        rows.append(func_compute_elo(sample_battles))
    df = pd.DataFrame(rows)
    return df.median().sort_values(ascending=False)

def pretty_print_elo_ratings(ratings):
    df = pd.DataFrame([
        [n, ratings[n]] for n in ratings.keys()
    ], columns=["Model", "Elo rating"]).sort_values("Elo rating", ascending=False).reset_index(drop=True)
    df["Elo rating"] = (df["Elo rating"] + 0.5).astype(int)
    df.index = df.index + 1
    return df





# Parameters
BOOTSTRAP_ROUNDS = 1000

np.random.seed(42)


if __name__=='__main__':
    # Directory containing JSON files
    directory = 'result/res'
    df = parse_json_files(directory)

    # print(df)
    bootstrap_elo_lu = get_bootstrap_result(df, compute_elo, BOOTSTRAP_ROUNDS)
    # Print the final Elo ratings
    final_ratings = compute_elo(df)
    print(pretty_print_elo_ratings(final_ratings))

    # Assuming bootstrap_elo_lu is a Series where index is the model and values are Elo ratings
    bootstrap_lu_median = pd.DataFrame({
        "model": bootstrap_elo_lu.index,
        "Elo rating": bootstrap_elo_lu.values
    })

    # Adjust the Elo ratings to integers
    bootstrap_lu_median["Elo rating"] = (bootstrap_lu_median["Elo rating"] + 0.5).astype(int)

    # Display the result
    print(bootstrap_lu_median)


