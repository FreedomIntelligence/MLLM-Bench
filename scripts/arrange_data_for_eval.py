import os
import json
import argparse
from prompts import gpt4v_eval_template as template
from prompts import gpt4v_role as role
from prompts import reference_template


def format_input(model_1_path, model_2_path, output_path):
    print('-'*50)
    print('model_1_path:', model_1_path)
    print('model_2_path:', model_2_path)
    print('-'*50)

    system = role
    
    with open(model_1_path, 'r') as f:
        model_1_ans = json.load(f)
    with open(model_2_path, 'r') as f:
        model_2_ans = json.load(f)
    with open('./data/questions.json', 'r') as f:
        question_types = json.load(f)

    model_1_dict = {}
    model_2_dict = {}
    question_type_dict = {}
    
    # convert the list to dictionary, the key is unique_idx
    for ans in model_1_ans:
        model_1_dict[str(ans['unique_idx'])] = ans
    model1 = model_1_dict[str(ans['unique_idx'])]['gen_model_id']

    for ans in model_2_ans:
        model_2_dict[str(ans['unique_idx'])] = ans
    model2 = model_2_dict[str(ans['unique_idx'])]['gen_model_id']
    
    for i in question_types:
        question_type_dict[str(i['id'])] = i['meta']['question type']

    input_file = []

    print('model1:', model1)
    print('model2:', model2)
    
    for idx in model_1_dict:
        # only include the unique_idx that both model_1 and model_2 have
        if idx not in model_2_dict:
            continue
        
        ans1 = model_1_dict[idx]['answer']
        ans2 = model_2_dict[idx]['answer']
        question_type = question_type_dict[idx]

        # left, choose 1 is model_1, choose 2 is model_2
        item1 = {}
        item1['unique_idx'] = str(idx) + '_1'
        item1['prompt'] = system + template.format(question=model_1_dict[idx]['prompt'], question_type = question_type, answer1=ans1, answer2=ans2)
        item1['image'] = model_1_dict[idx]['image']
        item1['model_1'] = model1
        item1['model_2'] = model2
        item1['raw_answer1'] = model_1_dict[idx]['answer']
        item1['raw_answer2'] = model_2_dict[idx]['answer']
        input_file.append(item1)
    
        # right, choose 1 is model_2, choose 2 is model_1
        item2 = {}
        item2['unique_idx'] = str(idx) + '_2'
        item2['prompt'] = system + template.format(question=model_2_dict[idx]['prompt'], question_type = question_type, answer1=ans2, answer2=ans1)
        item2['image'] = model_2_dict[idx]['image']
        item2['model_1'] = model2
        item2['model_2'] = model1
        item2['raw_answer1'] = model_2_dict[idx]['answer']
        item2['raw_answer2'] = model_1_dict[idx]['answer']
        input_file.append(item2)

    with open(output_path, 'w') as f:
        print('saving to', output_path)
        print('total number of examples:', len(input_file))
        for item in input_file:
            f.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_1_ans_path", type=str)
    parser.add_argument("--model_2_ans_path", type=str)
    parser.add_argument("--output_path", type=str)

    args = parser.parse_args()
    format_input(args.model_1_ans_path, args.model_2_ans_path, args.output_path)


