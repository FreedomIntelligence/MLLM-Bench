import io
import os
import json
import time
import base64
import requests
import argparse
import threading
import pandas as pd
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "YOUR_API_KEY"
FOWARD_URL = "https://api.openai.com/v1/chat/completions"
HOME_DIR = '../outputs'
TIME_OUT = 40
TIMEOUT_ERROR_CODE = 1000
EMPTY_RESPONSE_CODE = 1001
TEXT_MODEL_ERROR_CODE = 1002
VIOLATION_ERROR_CODE = 1004
EXTRACT_FAIL_CODE = 1003
AMBIGUOUS_ERROR_CODE = 1005
EXTRACT_ERROR_CODE = 1006
UNSUPPORTED_IMAGE_TYPE_CODE = 3000
FINISH_CODE = 999
BAD_GATE_ERROR = 1010
SANITIZER_ERROR_CODE = 8002

# create a list to store the request times
request_times = []

# create a lock to control the access to the request_times
lock = threading.Lock()

def get_image(image_path):
    img2format = {
        'png': 'PNG',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        "PNG": "PNG",
        "JPG": "JPEG",
        "JPEG": "JPEG",
        'webp': 'WEBP',
    }
    try:
        img = Image.open(image_path).convert('RGB')
        img_type = img.format
        if img_type not in img2format:
            img_type = image_path.split('.')[-1]
    except Exception as e:
        print(e)
        print(image_path)
        return None, None

    if img_type not in img2format:
        print(f'Unsupported image type: {img_type}')
        return None, None

    # Save the resized image to a BytesIO object
    byte_arr = io.BytesIO()
    img.save(byte_arr, format=img2format[img_type], quality=95)
    byte_arr.seek(0)
    return byte_arr, img_type

# check if result is valid and parse the result
def parse_api_response(raw_response, api_key, sample):
    try:
        response = json.loads(raw_response.content.decode("utf-8"))
    except Exception as e:
        print(e)
        print(raw_response)
        print(raw_response.content)
        print(sample)
        print("response decode error")
        if '502 Bad Gateway' in raw_response.content:
            return None, BAD_GATE_ERROR
        return None, 500
    try:
        content = response["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        print(response)
        print(sample)
        content = response["error"]["code"]
        print(f"api key: {api_key}, error code: {content}")
    if content is None:
        print("content is None")
        return None, 500
    elif type(content) == int:
        print(f"error code: {content}")
        return None, content
    elif 'insufficient_quota' in content:
        print(f"quota insufficient for key: {api_key}")
        return None, 400
    elif 'account_deactivated' in content:
        print(f"account deactivated: {api_key}")
        return None, 400
    elif "billing_not_active" in content:
        print(f"billing_not_active: {api_key}")
        return None, 400
    elif "model_not_found" in content:
        print(f"model_not_found: {api_key}")
        return None, 300
    elif "rate_limit" in content:
        return None, 429
    elif "invalid_api_key" in content:
        print(f"invalid_api_key: {api_key}")
        return None, 400
    elif 'content_policy_violation' in content:
        return None, VIOLATION_ERROR_CODE
    elif 'sanitizer_server_error' in content:
        return None, SANITIZER_ERROR_CODE
    return content, 200

def request_api(sample):
    # check if the result is already in the success folder
    if os.path.exists(f"{HOME_DIR}/sample_output_success/{sample['unique_idx']}.json"):
        return sample, FINISH_CODE

    # make sure the request is not sent too frequently
    while True:
        current_time = time.time()
        with lock:
            # remove the request times that are older than 60 seconds
            while request_times and current_time - request_times[0] > 60:
                request_times.pop(0)
            # if the number of requests sent in the past minute exceeds the limit, wait for a while before sending the request
            if len(request_times) < RATE_PER_MINUTE:
                # add the current request time
                request_times.append(current_time)
                break
        # wait for 1 second
        time.sleep(1)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    image, img_type = get_image(sample['image'])
    if image is None:
        sample['answer'] = None
        return sample, UNSUPPORTED_IMAGE_TYPE_CODE
    image = base64.b64encode(image.getvalue()).decode()

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": sample['prompt']
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/{img_type};base64,{image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 4096,
        "temperature": 0.5,
    }
    
    try:
        response = requests.post(FOWARD_URL, headers=headers, json=payload, verify=False, timeout=TIME_OUT)
    except Exception as e:
        print(e)
        print("request timeout")
        sample['answer'] = None
        return sample, TIMEOUT_ERROR_CODE
    
    ans, status_code = parse_api_response(response, API_KEY, sample)
    sample['response'] = json.loads(response.content.decode("utf-8"))
    sample['answer'] = ans
    if 'gen_model_id' not in sample:
        sample['gen_model_id'] = 'gpt4v-api'
    return sample, status_code

# check if result is in the answer set
def check(a, b):
    return any(s.lower() in b for s in a)

# delete the error files
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f'no such file: {file_path}')

# parse the output into answer1, answer2, unable to decide: situation one, unable to decide: situation two, and then count the votes
def parse_output():
    with open(f'{HOME_DIR}/sample_output_success.json', 'r') as f:
        results = json.load(f)
    
    error_samples = []
    votes = {}

    # convert answer 1 and answer 2 to model_1 and model_2, or unable to decide
    for res in results:
        unique_idx = res['unique_idx'].split('_')[0]
        if unique_idx not in votes:
            votes[unique_idx] = []
        if res['answer'] == None:
            error_samples.append(res['unique_idx'])
            continue
        if check(res['answer'].split('\n'), ['Answer1', 'answer1']):
            votes[unique_idx].append(res['model_1'])
            res['vote'] = res['model_1']
        elif check(res['answer'].split('\n'), ['Answer2', 'answer2']):
            votes[unique_idx].append(res['model_2'])
            res['vote'] = res['model_2']
        elif check(res['answer'].split('\n'), ["unable to decide: situation one", "Unable to decide: situation one"]):
            votes[unique_idx].append('unable to decide: situation one')
            res['vote'] = 'unable to decide: situation one'
        elif check(res['answer'].split('\n'), ["unable to decide: situation two", "Unable to decide: situation two"]):
            votes[unique_idx].append('unable to decide: situation two')
            res['vote'] = 'unable to decide: situation two'
        else:
            error_samples.append(res['unique_idx'])

    for filename in error_samples:
        file_path = os.path.join(HOME_DIR, 'sample_output_success', f'{filename}.json')
        delete_file(file_path)

    print(f'Error samples: {len(error_samples)}')

    # count the votes by question
    vote_results = {res['model_1']: 0, res['model_2']: 0, 'unable to decide: situation one': 0, 'unable to decide: situation two': 0, 'unable to decide': 0, 'tie': 0}
    for unique_idx, vote in votes.items():
        if len(vote) != 2:
            # print('Vote Error!')
            # print(vote)
            # print(unique_idx)
            continue
        if vote[0] == vote[1]:
            # unable to decide: situation one, unable to decide: situation two, model_1 model_1, model_2 model_2
            vote_results[vote[0]] += 1
        elif res['model_1'] in vote and ("unable to decide: situation one" in vote or "unable to decide: situation two" in vote):
            # model_1 unable to decide
            vote_results[res['model_1']] += 1
        elif res['model_2'] in vote and ("unable to decide: situation one" in vote or "unable to decide: situation two" in vote):
            # model_2 unable to decide
            vote_results[res['model_2']] += 1
        elif res['model_1'] in vote and res['model_2'] in vote:
            # model_1 model_2
            vote_results['tie'] += 1
        elif "unable to decide: situation one" in vote and "unable to decide: situation two" in vote:
            # unable to decide: situation one unable to decide: situation two
            vote_results['unable to decide'] += 1
        else:
            print('Vote Error!')
            print(vote)
    
    total = 0
    for k, v in vote_results.items():
        total += v
    vote_results['total'] = total
    with open(f'{HOME_DIR}/vote_counts.json', 'w') as f:
        json.dump(vote_results, f, indent=4)
    with open(f'{HOME_DIR}/vote_results.json', 'w') as f:
        json.dump(results, f, indent=4)

# write the sample to the success folder if the status code is 200, otherwise write it to the fail folder
def write_samples(sample, status_code):
    if status_code == 200:
        with open(f"{HOME_DIR}/sample_output_success/{sample['unique_idx']}.json", 'w') as f:
            f.write(json.dumps(sample, ensure_ascii=False, indent=4))
            with lock:
                del SAMPLE_LIST[SAMPLE_LIST.index(sample['unique_idx'])]
    else:
        with open(f"{HOME_DIR}/sample_output_fail/{sample['unique_idx']}.json", 'w') as f:
            f.write(json.dumps(sample, ensure_ascii=False, indent=4))

# merge the output files
def merge():
    files = os.listdir(f'{HOME_DIR}/sample_output_success/')
    files = [i for i in files if i.endswith('.json')]
    files = sorted(files, key=lambda x: x.split('.')[0])
    contents = []
    with open(f'{HOME_DIR}/sample_output_success.json', 'w') as f:
        for file in tqdm(files):
            try:
                with open(f'{HOME_DIR}/sample_output_success/{file}', 'r') as f1:
                    content = json.load(f1)
                    contents.append(content)
            except Exception as e:
                print(e)
                print(file)
                delete_file(f'{HOME_DIR}/sample_output_success/{file}')

        f.write(json.dumps(contents, ensure_ascii=False, indent=4))

def main(sample):
    try:
        sample, status_code= request_api(sample=sample)
        if status_code != FINISH_CODE:
            if status_code != TIMEOUT_ERROR_CODE:
                # if the answer is not in the answer set and the status code is 200, set the status code to ambiguous
                if (sample['answer'] is not None) and (not check(sample['answer'].split('\n'), ['answer1', 'answer2', "unable to decide: situation one", "unable to decide: situation two"])) and (status_code == 200):
                    status_code = AMBIGUOUS_ERROR_CODE
                    print(sample['unique_idx'], sample['answer'])
                write_samples(sample, status_code)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    '''
    When sending a request, it will check whether the number of requests sent in the past minute exceeds the limit. If it exceeds the limit, wait for a while before sending the request
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--HOME_DIR', type=str, default='../outputs')
    parser.add_argument('--rate_per_minute', type=int, default=5)
    parser.add_argument('--annotation_path', type=str, default='../data/anchor.json')
    parser.add_argument('--image_dir', type=str, default='../data/images')
    parser.add_argument('--max_retry', type=int, default=3)
    parser.add_argument('--timeout', type=int, default=40)
    args = parser.parse_args()

    HOME_DIR = args.HOME_DIR
    RATE_PER_MINUTE = args.rate_per_minute
    num_of_threads = RATE_PER_MINUTE // 2
    ANNOTATION_PATH = args.annotation_path
    IMAGE_DIR = args.image_dir
    MAX_RETRY = args.max_retry
    TIME_OUT = args.timeout

    # create the output folders
    if not os.path.exists(HOME_DIR):
        os.mkdir(HOME_DIR)
    if not os.path.exists(f'{HOME_DIR}/sample_output_success/'):
        os.mkdir(f'{HOME_DIR}/sample_output_success/')
        os.mkdir(f'{HOME_DIR}/sample_output_fail/')
        os.mkdir(f'{HOME_DIR}/sample_output_all/')
        os.mkdir(f'{HOME_DIR}/raw_output/')

    # collet the samples to be evaluated
    start = time.time()
    print('-'*80)
    print('sampling data')
    SAMPLE_LIST = []
    samples = pd.read_json(ANNOTATION_PATH, lines=True, dtype={'unique_idx': str})
    SAMPLE_LIST += samples['unique_idx'].tolist()
    success_samples = [str(i.split('.')[0]) for i in os.listdir(f'{HOME_DIR}/sample_output_success/')]
    SAMPLE_LIST = [i for i in SAMPLE_LIST if i not in success_samples]
    print('sampling done')
    print('-'*80)

    print('-'*80)
    print(f'Using {num_of_threads} threads!')
    print(f'Using {RATE_PER_MINUTE} requests per minute!')

    # start the evaluation
    num_round = 0
    while SAMPLE_LIST and num_round < MAX_RETRY:
        num_round += 1
        print('-'*80)
        print(f'Round {num_round}, {len(SAMPLE_LIST)} samples left! Timeout: {TIME_OUT} seconds!')
        with ThreadPoolExecutor(max_workers=num_of_threads) as executor:
            futures = []
            # Convert DataFrame to dict for faster lookup
            samples_dict = {str(row['unique_idx']): row for row in samples.to_dict('records')}
            for i in tqdm(SAMPLE_LIST):
                # Convert i to string if it's not
                i = str(i)
                if os.path.exists(samples_dict[i]['image']):
                    futures.append(executor.submit(main, samples_dict[i].copy()))
            results = []
            for future in tqdm(as_completed(futures)):
                results.append(future.result())
        TIME_OUT += 20

        merge()
        parse_output()
    merge()
    parse_output()
