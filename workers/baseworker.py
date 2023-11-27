



from typing import Any

from accelerate import Accelerator
import os
import json
from PIL import Image
import pdb
import torch


class BaseWorker():
    def __init__(self, config, output_pth) -> None:
        self.init_components(config)
        self.output_pth = output_pth
        self.gen_kwargs = config.get('gen_kwargs', {})
        self.model_id = config.model_name


    @classmethod
    def from_config(cls, **kwargs):
        return cls(**kwargs)

    def init_components(self) -> None:
        '''
        Initialize model and processor, and anything needed in forward().
        '''
        raise NotImplementedError
    




    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs: dict) -> list[str]:
        '''
        Parameters: 
            `questions`: a list of questions to ask the model.

            `image_paths`: a list of image paths for the images.

            `device`: the correct device allocated automatically by `accelerate`. Use it by calling `.to(device)`.

            `gen_kwargs`: generation hyperparameters supported by `transformers.GenerationConfigs`. 


        Returns:
            `prompts`: a list of prompts that are actually fed into the model. If they are the same as `questions`, return `questions` here.
            
            `answers`: a list of answers from the model.

        '''
        raise NotImplementedError

    def __call__(self, device, **kwargs: Any) -> Any:
        for k in ['question', 'image_path']:
            assert k in kwargs, f'the key {k} is missing'
        questions = kwargs['question']
        image_paths = kwargs['image_path']
        prompts, answers = self.forward(
            questions=questions, 
            image_paths=image_paths, 
            device=device,
            gen_kwargs=self.gen_kwargs,
        ) 
        outputs = self.collate_batch_for_output(kwargs, answers=answers, prompts=prompts)
        return outputs
    
    
    def prepare(self, dataloader, accelerator: Accelerator):
        self.model, dataloader = accelerator.prepare(self.model, dataloader)
        return dataloader
        

    def collate_batch_for_output(self, batch, answers, prompts):

        ret = []
        len_batch = len(batch['id'])
        assert len(answers) == len_batch

        for i in range(len_batch):
            new = {}
            for k in batch.keys():
                if k == 'image_path': # modify the key
                    new['image'] = batch[k][i]
                    continue
                elif k == 'id': # modify the key
                    new['unique_idx'] = batch[k][i]
                    continue
                    
                new[k] = batch[k][i]
            new['gen_model_id'] = self.model_id
            


            new['prompt'] = prompts[i] # this can be different from the raw question.
            new['answer'] = answers[i]
            new['gen_kwargs'] = dict(self.gen_kwargs) # omegaconf -> dict
        
            ret.append(new)
        
        return ret
    
    def save(self, results):
        with open(self.output_pth, 'a') as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')

    


