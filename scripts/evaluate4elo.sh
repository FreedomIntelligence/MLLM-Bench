#!/bin/bash

# rpm=$1
# timeout=$2

rpm=100
timeout=90

home_dir=result

model=#model

api_key=#apikey

mkdir -p $home_dir/data_4_eval
mkdir -p $home_dir/eval_res
mkdir -p $home_dir/res

model_dir="model_ans"
model_files=($(ls $model_dir*.json))

for ((i=0; i<${#model_files[@]}-1; i++)); do
    for ((j=i+1; j<${#model_files[@]}; j++)); do
        model1_path="${model_files[$i]}"
        model2_path="${model_files[$j]}"

        model1_name=$(basename "$model1_path" .json)
        model2_name=$(basename "$model2_path" .json)
        
        eval_data_path=$home_dir/data_4_eval/${model1_name}_${model2_name}.json

        save_dir=$home_dir/eval_res/${model1_name}_${model2_name}

        python arrange_data_for_eval.py \
            --model_1_ans_path $model1_path \
            --model_2_ans_path $model2_path \
            --output_path $eval_data_path \
            --criteria $criteria \


        python evaluate.py \
            --HOME_DIR $save_dir \
            --annotation_path $eval_data_path \
            --rate_per_minute $rpm \
            --max_retry 3 \
            --timeout $timeout \
            --model $model \
            --API_KEY "$api_key" \
            --FORWARD_URL "$forward_url" \
            --use_web False

        cp $save_dir/vote_results.json $home_dir/res/${model1_name}_${model2_name}.json
        cp $save_dir/sample_output_success.json model_outputs/${model1_name}_${model2_name}.json
    done
done

python cal_clo.py
