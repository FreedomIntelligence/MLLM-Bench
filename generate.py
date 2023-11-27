
import json
from argparse import ArgumentParser

import json, os, pdb
from accelerate import Accelerator

from utils import get_dataloader, get_worker_class
from omegaconf import OmegaConf
from tqdm import tqdm



def get_args():
    parser = ArgumentParser()
    parser.add_argument('--model_name', required=True)
    parser.add_argument('--output_dir', default='outputs')
    parser.add_argument('--question_pth', default='data/questions.json')
    parser.add_argument('--bsz', default=3, type=int)
    parser.add_argument('--model_configs', default='configs/model_configs.yaml')
    parser.add_argument('--overwrite', action='store_true')

    args = parser.parse_args()

    args.tmp_output_pth = os.path.join(args.output_dir, 'tmp', f"{args.model_name}_tmp.json")
    args.output_pth = os.path.join(args.output_dir, f"{args.model_name}.json")
    os.makedirs(os.path.dirname(args.tmp_output_pth), exist_ok=True)
    os.makedirs(os.path.dirname(args.output_pth), exist_ok=True)



    return args

def init_worker(args, accelerator: Accelerator):
    
    worker_class = get_worker_class(args.model_name)


    config = OmegaConf.load(args.model_configs)
    if not config.get(args.model_name):
        raise ValueError
    
    config = config[args.model_name]
    # pdb.set_trace()

    config.device = str(accelerator.device)

    worker = worker_class.from_config(config=config, output_pth=args.tmp_output_pth)


    return worker


def load_all_data(data_pth):
    lines = {}
    with open(data_pth) as f:
        # for line in f:
        data = json.load(f)
        for line in data:
            # line = json.loads(line)
            lines[line['id']] = line
    
    
    return lines


def filter_previous_lines(output_pth, all_data):
    results = []
    if os.path.exists(output_pth):
        with open(output_pth) as f:
            # data = json.load(f)
            # for line in data:
            #     if line['id'] in all_data:
            #         all_data.pop(line['id'])
            #         results.append(line)

            for line in f:
                line = json.loads(line)
                if line['unique_idx'] in all_data:
                    all_data.pop(line['unique_idx'])
                    results.append(line)


    print(f'{len(all_data)} will be evaluated')
                
    return results, list(all_data.values())



def run(args, worker, data, results: list[dict], accelerator: Accelerator):


    dataloader = get_dataloader(data, args.bsz)
    
    dataloader = worker.prepare(dataloader, accelerator) # prepare dataloader and model (implicitly)


    # if accelerator.is_main_process:
    #     pbar = tqdm(dataloader)

    iterator = tqdm(dataloader) if accelerator.is_main_process else dataloader
    

    for batch in iterator:
        # batch: question, image_path, id
        # try:
        outputs = worker(device=accelerator.device, **batch) # list[dict], with the key "answer" added to each item
        # except Exception as e:
            # print(e)
            # continue
        
        # pdb.set_trace()

        results.extend(outputs)

        worker.save(outputs)
        # if accelerator.is_main_process:
        #     pbar.update()

    
    
    print(f'generation done')
    accelerator.wait_for_everyone()
    # gather all results

    save(results, accelerator, args)

def save(results, accelerator, args):
    if accelerator.is_main_process:
        results = []
        with open(args.tmp_output_pth, 'r') as f:
            for line in f:
                line = json.loads(line)
                results.append(line)

        if os.path.exists(args.output_pth):
            if not args.overwrite:
                print(f'{args.output_pth} exists. Please pass `overwrite=True` to avoid unwanted overwriting.')
                exit(0)
        with open(args.output_pth, 'w') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        


def main(args):
    import torch.distributed as dist
    accelerator = Accelerator()
    
    accelerator.state.deepspeed_plugin.deepspeed_config['train_micro_batch_size_per_gpu'] = args.bsz
    accelerator.state.deepspeed_plugin.deepspeed_config['train_batch_size'] = args.bsz * dist.get_world_size()

    accelerator.print(f'generating {args.model_name}')

    all_data = load_all_data(args.question_pth)

    # results, to_be_evaluated = filter_previous_lines(args.output_pth, all_data)
    results, to_be_evaluated = filter_previous_lines(args.tmp_output_pth, all_data)

    if len(to_be_evaluated) == 0:
        save(results, accelerator, args)
        exit()

    worker = init_worker(args, accelerator)

    run(args, worker, to_be_evaluated, results, accelerator)




if __name__ == '__main__':
    args = get_args()
    main(args)

