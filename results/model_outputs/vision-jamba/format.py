import os
import json


files = os.listdir('/mntcephfs/data/med/shunian/GPT4V-Web/model_outputs/vision-jamba')

for file in files:
    if file.endswith('.py'):
        continue
    data = json.load(open(f'/mntcephfs/data/med/shunian/GPT4V-Web/model_outputs/vision-jamba/{file}/merge.json'))
    format_data = []
    for d in data:
        temp = {
            'unique_idx': str(d['unique_idx']),
            'answer': d['raw_response'],
            'gen_model_id': d['model_id'],
        }
        format_data.append(temp)
    with open(f'/mntcephfs/data/med/shunian/GPT4V-Web/model_outputs/vision-jamba/{file}/formated_merge.json', 'w') as f:
        json.dump(format_data, f)