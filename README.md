# MLLM-Bench
Evaluating Multi-modal LLMs using GPT-4V
<center>

![Python 3.9+](https://img.shields.io/badge/Python-3.9-lightblue) ![Pytorch 1.13.0](https://img.shields.io/badge/PyTorch-1.13-lightblue) ![transformers](https://img.shields.io/badge/transformers-4.36.0.dev0%2B-lightblue) ![accelerate](https://img.shields.io/badge/accelerate-0.22-lightblue)
</center>

<p align="center">
   📃 <a href="arxiv.org" target="_blank">Paper</a> • 🌐 <a href="https://mllm-bench.llmzoo.com/" target="_blank">Website</a> • 🤗 <a href="huggingface.com" target="_blank">HuggingFace</a>  

<p align="center">
<img src="./image.png" alt="Data Composition" width="550" height="550">


## 🌈 Update
* **[2023.11.18]** 🎉🎉🎉 This repo is made public!🎉🎉🎉

## Leaderboard


## How to use
### Environment Setup
<details><summary>Click to expand</summary>
   
Install required packages:
```bash
pip install -r requirements.txt
```
Update `transformers` (we used `4.36.0.dev0`):
```bash
pip install git+https://github.com/huggingface/transformers
```

</details>



### Answer generation
<details><summary>Click to expand</summary>

- Configurate `accelerate` settings. We use `bf16` inference by default. If this is not supported by your device, set `downcast_bf16` to `false` and `mixed_precision` to `fp16`.

- Add model information in [configs/model_configs.yaml](./configs/model_configs.yaml)

- Create a model worker in [workers/model_workers.py](./workers/model_workers.py). The worker should inherit `BaseWorker`.
Rewrite `init_components()` and `forward()` method. Explanations of parameters and outputs of the two methods are in [workers/baseworker.py](./workers/baseworker.py).

- Run `bash generate.sh`.


</details>



### Submission for Leaderboard
