# MLLM-Bench
Evaluating Multi-modal LLMs using GPT-4V.
<center>

![Python 3.9+](https://img.shields.io/badge/Python-3.9+-lightblue) ![Pytorch 2.0](https://img.shields.io/badge/PyTorch-2.0+-lightblue) ![transformers](https://img.shields.io/badge/transformers-4.36.0.dev0%2B-lightblue) ![accelerate](https://img.shields.io/badge/accelerate-0.22+-lightblue)
</center>

<p align="center">
   📃 <a href="https://arxiv.org/abs/2311.13951" target="_blank">Paper</a> • 🌐 <a href="https://mllm-bench.llmzoo.com/" target="_blank">Website</a> • 🤗 <a href="huggingface.com" target="_blank">HuggingFace</a>  

<p align="center">
<img src="./image.png" alt="Data Composition" width="550" height="550">


## 🌈 Update
* **[2024.1.7]** V2 data, reuslts and leaderboard are updated.

* **[2023.11.18]** 🎉🎉🎉 This repo is made public!🎉🎉🎉

## Leaderboard
We present the results of voting using GPT-4V as anchor. The numbers denote *win/tie/lose* of a benchmarked model over GPT-4V. See more results of different evaluation protocols and anchors in our  [paper](https://arxiv.org/abs/2311.13951). The information of benchmarked models is [here](./Model_cards.md).

| **Rank** | **Models**       | **Perception**  | **Understanding** | **Applying** | **Analyzing** | **Evaluation** | **Creation** | **Win Rates over GPT-4V** |
|------|--------------|-------------|---------------|----------|-----------|------------|----------|-----------|
| 🏅️    | LLaVA-v1.5   | 2/3/65      | 6/14/90       | 11/3/46  | 4/10/86   | 8/1/31     | 0/3/37   | 0.07      |
| 🥈    | mPLUG-Owl2   | 3/3/64      | 7/6/97        | 8/9/43   | 3/8/89    | 7/2/31     | 2/1/37   | 0.07      |
| 🥉    | LVIS         | 2/3/65      | 5/11/94       | 10/4/46  | 2/9/89    | 6/4/30     | 0/5/35   | 0.06      |
| 4    | Qwen-VL-Chat | 3/6/61      | 3/12/95       | 11/6/43  | 3/11/86   | 6/3/31     | 0/3/37   | 0.06      |
| 5    | kosmos2      | 2/2/66      | 2/2/106       | 8/2/50   | 3/1/96    | 4/0/36     | 0/0/40   | 0.05      |
| 6    | MiniGPT-v2   | 2/5/63      | 4/6/100       | 7/7/46   | 1/7/92    | 7/0/33     | 2/0/38   | 0.05      |
| 7    | InstructBLIP | 3/1/66      | 2/6/102       | 5/6/49   | 1/6/93    | 6/2/32     | 0/1/39   | 0.04      |
| 8    | Fuyu-8B      | 1/3/66      | 3/0/107       | 3/3/54   | 1/4/95    | 4/2/34     | 0/0/40   | 0.03      |
| 9    | SEED-LLaMA   | 1/2/67      | 2/2/106       | 5/4/51   | 2/1/97    | 3/4/33     | 0/0/40   | 0.03      |
| 10   | BLIP2        | 3/1/66      | 1/2/107       | 3/6/51   | 1/1/98    | 1/2/37     | 0/0/40   | 0.02      |





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



### Answer Generation
<details><summary>Click to expand</summary>

- Configurate `accelerate` settings. We use `bf16` inference by default. If this is not supported by your device, set `downcast_bf16` to `false` and `mixed_precision` to `fp16`.

- Add model information in [configs/model_configs.yaml](./configs/model_configs.yaml)

- Create a model worker in [workers/model_workers.py](./workers/model_workers.py). The worker should inherit `BaseWorker`.
Rewrite `init_components()` and `forward()` method. Explanations of parameters and outputs of the two methods are in [workers/baseworker.py](./workers/baseworker.py).

- Run `bash generate.sh`.


</details>

### Self Evaluate
<details><summary>Click to expand</summary>

- Prepare the data in the format as shown in [data/anchor.json](./data/anchor.json), note that the key "unique_idx", "gen_model_id", and "answer" are required. Move your data under [data](./data/) folder.

- Modify the parameters in [evaluate.sh](./evaluate.sh), especially "model_name" and "model2_path".

- Put your OpenAI API key in [evaluate.py](./scripts/evaluate.py), please make sure you have access to model "gpt-4-vision-preview".

- Run `bash evaluate.sh`.

- NOTE: The per sample criteria is not provided for self-evaluate and this self-evaluation process is just used for your reference. If you wish your results to be displayed on the leaderboard, please refer to [Submission for Leaderboard](#submission-for-leaderboard).

</details>

### Submission for Leaderboard



## Citation
```angular2
@misc{ge2023mllmbench,
      title={MLLM-Bench, Evaluating Multi-modal LLMs using GPT-4V}, 
      author={Wentao Ge and Shunian Chen and Guiming Chen and Junying Chen and Zhihong Chen and Shuo Yan and Chenghao Zhu and Ziyue Lin and Wenya Xie and Xidong Wang and Anningzhe Gao and Zhiyi Zhang and Jianquan Li and Xiang Wan and Benyou Wang},
      year={2023},
      eprint={2311.13951},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


## Star History

<a href="https://star-history.com/#FreedomIntelligence/MLLM-Bench&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=FreedomIntelligence/MLLM-Bench&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=FreedomIntelligence/MLLM-Bench&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=FreedomIntelligence/MLLM-Bench&type=Date" />
  </picture>
</a>