#!/bin/bash

# rate per minute
rpm=100
# timeout in seconds
timeout=30

output_dir=./outputs
model_name=qwen-vl-chat
model1_path=./data/anchor.json
model2_path=./data/$model_name.json
eval_data_path=$output_dir/data_4_eval/${model_name}.json
save_dir=$output_dir/eval_res/${model_name}

python ./scripts/arrange_data_for_eval.py \
    --model_1_ans_path $model1_path \
    --model_2_ans_path $model2_path \
    --output_path $eval_data_path \

python ./scripts/evaluate.py \
    --HOME_DIR $save_dir \
    --annotation_path $eval_data_path \
    --rate_per_minute $rpm \
    --max_retry 3 \
    --timeout $timeout \

cp $save_dir/vote_counts.json ./results/counts/${model_name}.json
cp $save_dir/vote_results.json ./results/results/${model_name}.json
