


# for model in fuyu-8b  instructblip-vicuna-13b qwen-vl-chat blip2-flan-t5-xl idefics-9b-instruct kosmos-2 mPLUG-owl2 minigpt-v2

accelerate launch --config_file ./configs/accelerate_configs.yaml \
    --main_process_port 29501  \
    --num_machines 1 \
    --machine_rank 0 \
    --num_processes 7  \
    --deepspeed_multinode_launcher standard ./generate.py \
    --question_pth data/questions.json  \
    --model_name qwen-vl-chat \
    --bsz 6  \
    --overwrite 