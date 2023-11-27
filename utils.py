
from torch.utils.data import Dataset, DataLoader
from workers.model_workers import (
    Fuyu,
    InstructBLIPVicuna13B,
    QwenVLChat, 
    Blip2FlanT5XL,
    idefics9BInstruct,
    KOSMOS2
)

name2worker = {
    'fuyu-8b': Fuyu,
    'kosmos-2': KOSMOS2,
    'instructblip-vicuna-13b': InstructBLIPVicuna13B,
    'qwen-vl-chat':QwenVLChat,
    'blip2-flan-t5-xl': Blip2FlanT5XL,
    'idefics-9b-instruct': idefics9BInstruct,
    # 'llava-v1.5-13b':LLaVA13B,
    # 'cogvlm-chat': CogVLMChat,
    # 'mPLUG-owl2': mPLUGOWL2,
    # 'minigpt-v2': MiniGPTv2,
    # 'seed-llama-14b': SEEDLLaMa14B,
    # 'lvis-instruct4v-llava-7b': LVIS_Instruct4V_LLaVA7B,
}


def get_worker_class(name):
    return name2worker[name]


class BenchmarkDataset(Dataset):
    def __init__(self, data) -> None:
        # super().__init__()
        self.data = data

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        '''
{
    'id': 1,
    'image_path': '/path/to/image',
    'question': 'what is the image about?',
    'reference': '',
    'meta' {
        'ability': 'ab',
        'task': 'cd',
        'url': 'http',
    },
}
'''

        return self.data[index]
    
    
    def collate_fn(self, batch):

        keys = batch[0].keys()
        ret = {k: [] for k in keys}


        for line in batch:
            for k in line:
                ret[k].append(line[k])

        return ret


def get_dataloader(data: list[dict], bsz, ):
    
    ds = BenchmarkDataset(data)

    test_loader = DataLoader(ds, batch_size=bsz, collate_fn=ds.collate_fn, shuffle=False)

    return test_loader