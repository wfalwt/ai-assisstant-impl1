

### 大模型
采用[Qwen2-7B-Instruct](https://www.modelscope.cn/models/qwen/Qwen2-7B-Instruct/summary)大模型，使用vllm启用openai的api服务，启动命令如下
```shell
python -m vllm.entrypoints.openai.api_server --served-model-name Qwen2-7B-Instruct --api-key api_key  --model /llm/models/Qwen2-7B-Instruct --dtype=float16
```
推理机显卡(Tesla V100-SXM3-32GB * 2) 配置
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.90.07              Driver Version: 550.90.07      CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla V100-SXM3-32GB           Off |   00000000:05:00.0 Off |                    0 |
| N/A   45C    P0             61W /  350W |       1MiB /  32768MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  Tesla V100-SXM3-32GB           Off |   00000000:06:00.0 Off |                    0 |
| N/A   46C    P0             51W /  350W |       1MiB /  32768MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```
