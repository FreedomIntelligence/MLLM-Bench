from typing import Any
from accelerate import Accelerator
from workers.baseworker import *
import sys




class Fuyu(BaseWorker):


    def init_components(self, config):
        from transformers import FuyuForCausalLM, FuyuProcessor

        self.processor = FuyuProcessor.from_pretrained(config.model_dir)
        self.model = FuyuForCausalLM.from_pretrained(config.model_dir)
        self.model.eval()

    

    def forward(self, questions, image_paths, device, gen_kwargs):

        inputs = self.processor(text=questions, images=[Image.open(p).convert('RGB') for p in image_paths], return_tensors="pt")
        for k, v in inputs.items():
            if isinstance(v, list):
                for i in range(len(v)):
                    inputs[k][i] = v[i].to(device)

            else:
                inputs[k] = v.to(device)
        input_len = inputs.input_ids.shape[1]
        outputs = self.model.generate(**inputs, **gen_kwargs)
            
        answers = self.processor.batch_decode(outputs[:, input_len:], skip_special_tokens=True)

        return questions, answers
    




class InstructBLIPVicuna13B(BaseWorker):
    def init_components(self, config) -> None:
        from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration

        self.processor = InstructBlipProcessor.from_pretrained(config.model_dir, use_fast=False)
        self.model = InstructBlipForConditionalGeneration.from_pretrained(config.model_dir)
        self.model.eval()


    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs) -> list[str]:

        images = [Image.open(p).convert('RGB') for p in image_paths]
        answers = []
        # inputs = self.processor(images=images, text=questions, padding=True, return_tensors="pt").to(device)
        for img, q in zip(images, questions):
            inputs = self.processor(images=img, text=q, return_tensors="pt").to(device)
            
            outputs = self.model.generate(
                    **inputs,
                    **gen_kwargs,
            )
            answer = self.processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
            answers.append(answer)

        return questions, answers

class Blip2FlanT5XL(BaseWorker):
    def init_components(self, config) -> None:
        from transformers import Blip2Processor, Blip2ForConditionalGeneration

        self.processor = Blip2Processor.from_pretrained(config.model_dir, use_fast=False)
        self.model = Blip2ForConditionalGeneration.from_pretrained(config.model_dir,)

        self.model.eval()


    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs) -> list[str]:
        # question = "how many dogs are in the picture?"
        images = [Image.open(p).convert('RGB') for p in image_paths]
        answers = []

        # inputs = self.processor(images, questions, return_tensors="pt").to(device)
        for img, q in zip(images, questions):
            inputs = self.processor(images=img, text=q, return_tensors="pt").to(device)
            
            outputs = self.model.generate(
                    **inputs,
                    **gen_kwargs,
            )
            answer = self.processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
            answers.append(answer)

        return questions, answers


class idefics9BInstruct(BaseWorker):
    def init_components(self, config) -> None:
        from transformers import IdeficsForVisionText2Text, AutoProcessor, IdeficsProcessor

        self.model = IdeficsForVisionText2Text.from_pretrained(config.model_dir)
        self.processor = AutoProcessor.from_pretrained(config.model_dir)

        self.model.eval()


    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs) -> list[str]:
        # question = "how many dogs are in the picture?"
        images = [Image.open(p).convert('RGB') for p in image_paths]

        prompts = [[
            "User:",
            img,
            f"{question}<end_of_utterance>",
            "\nAssistant:",
        ] for img, question in zip(images, questions)]

        # prompts = [[img, q] for img, q in zip(images, questions)]

        inputs = self.processor(prompts, add_end_of_utterance_token=False, return_tensors="pt", padding=True).to(device)
        # --single sample mode
        # inputs = processor(prompts[0], return_tensors="pt").to(device)

        # Generation args
        exit_condition = self.processor.tokenizer("<end_of_utterance>", add_special_tokens=False).input_ids
        bad_words_ids = self.processor.tokenizer(["<image>", "<fake_token_around_image>"], add_special_tokens=False).input_ids



        input_len = inputs.input_ids.shape[1]

        # Generation args
        bad_words_ids = self.processor.tokenizer(["<image>", "<fake_token_around_image>"], add_special_tokens=False).input_ids

        outputs = self.model.generate(**inputs, **gen_kwargs, eos_token_id=exit_condition, bad_words_ids=bad_words_ids,)
        answers = self.processor.batch_decode(outputs[:, input_len:], skip_special_tokens=True)

        # print(answers)
        return [''.join([str(_) for _ in p]) for p in prompts], answers



class KOSMOS2(BaseWorker):
    def init_components(self, config) -> None:
        from transformers import AutoProcessor, Kosmos2ForConditionalGeneration

        self.model = Kosmos2ForConditionalGeneration.from_pretrained(config.model_dir)
        self.processor = AutoProcessor.from_pretrained(config.model_dir)

        self.model.eval()


    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs) -> list[str]:
        # question = "how many dogs are in the picture?"
        images = [Image.open(p).convert('RGB') for p in image_paths]
        prompts = [f'Question: {q} Answer:' for q in questions]
        answers = []
        for prompt, image in zip(prompts, images):
            inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(device)
            input_len = inputs.input_ids.shape[1]


            outputs = self.model.generate(pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                image_embeds=None,
                image_embeds_position_mask=inputs["image_embeds_position_mask"],
                use_cache=True,
                **gen_kwargs,
            )
            answer = self.processor.batch_decode(outputs[:, input_len:], skip_special_tokens=True)[0]
            answers.append(answer)

        return prompts, answers




class QwenVLChat(BaseWorker):

    def init_components(self, config) -> None:

        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(config.model_dir, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(config.model_dir, trust_remote_code=True).eval()
        self.model.eval()

    def forward(self, questions: list[str], image_paths: list[str], device, gen_kwargs) -> list[str]:
        # images = [Image.open(p).convert('RGB') for p in image_paths]
        answers = []

        for question, image in zip(questions, image_paths):
            query = self.tokenizer.from_list_format([
                {'image': image},
                {'text': question},
            ])
            response, history = self.model.chat(self.tokenizer, query=query, history=None)
            answers.append(response)
        
        return questions, answers


    