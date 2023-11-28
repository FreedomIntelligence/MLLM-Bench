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
* **[2023.11.18]** 🎉🎉🎉 This repo is made public!🎉🎉🎉

## Leaderboard
We present the results of voting using GPT-4V as anchor. The numbers denote *win/tie/lose* of a benchmarked model over GPT-4V. See more results of different evaluation protocols and anchors in our  [paper](https://arxiv.org/abs/2311.13951). The information of benchmarked models is [here](./Model_cards.md).

| **Rank** | **Models**    | **Perception** | **Understanding** | **Applying** | **Analyzing** | **Evaluation** | **Creation** | **$\sum$ wins** |
|:----------:|---------------|----------------|-------------------|--------------|---------------|----------------|--------------|-----------------|
| 🏅️        | LLaVA-v1.5    | 5/15/50        | 10/39/51          | 14/18/38     | 6/41/53       | 10/12/18       | 6/19/15      | 51              |
| 🥈        | LVIS          | 5/18/47        | 11/33/56          | 10/16/44     | 9/31/60       | 8/15/17        | 5/20/15      | 48              |
| 🥉       | mPLUG-Owl2    | 3/12/55        | 12/31/57          | 12/9/49      | 5/34/61       | 8/9/23         | 5/18/17      | 48              |
| 4        | CogVLM-Chat   | 6/15/49        | 11/31/58          | 6/21/43      | 6/28/66       | 7/16/17        | 6/12/22      | 42              |
| 5        | Qwen-VL-Chat  | 7/15/48        | 13/33/54          | 7/27/36      | 4/43/53       | 8/16/16        | 2/22/16      | 41              |
| 6        | MiniGPT-v2    | 3/14/53        | 9/29/62           | 3/22/45      | 5/28/67       | 7/17/16        | 4/18/18      | 31              |
| 7        | InstructBLIP  | 2/12/56        | 10/19/71          | 7/9/54       | 3/24/73       | 5/9/26         | 1/15/24      | 28              |
| 8        | Fuyu-8B       | 3/7/60         | 9/13/78           | 3/5/62       | 1/15/84       | 6/9/25         | 1/9/30       | 23              |
| 9        | IDEFICS-9B    | 2/13/55        | 9/16/75           | 4/16/50      | 3/23/74       | 3/17/20        | 2/16/22      | 23              |
| 10       | SEED-LLaMA    | 4/9/57         | 2/21/77           | 5/18/47      | 7/22/71       | 2/17/21        | 3/10/27      | 23              |
| 11       | kosmos2       | 3/7/60         | 8/14/78           | 4/10/56      | 4/17/79       | 3/12/25        | 0/8/32       | 22              |
| 12       | BLIP2         | 0/4/66         | 2/8/90            | 2/6/62       | 2/5/93        | 2/6/32         | 1/7/32       | 9               |





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
