import requests
import time
from prompt import *

st = time.time()

# 直接生成
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonxai/analysis_log'

with open("test_switch_log.txt", "r", encoding="utf-8") as f:
    log_data = f.read()

require_text = "<log_data>{log_data}<log_data>\n".format(log_data=log_data) + user_prompt

param = {"model_name":"meta-llama/llama-3-1-70b-instruct", "system_prompt":system_prompt, "require_text": require_text}

response = requests.post(api_url, params = param, verify=False) 
print(response.json()['analysis'])
print(time.time()-st)

# 聊天 直接輸入問題和log
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/analysis_log_chat'
require_text = "test chat"
history = [{"test": "history"}]
input_body = {"model_name":"meta-llama/llama-3-1-70b-instruct", "require_text": require_text, "history": history}

response = requests.post(api_url, json = input_body, verify=False)
print(response.json())

# RAG + 聊天
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/rag_log_chat'

require_text = "test chat"
history = [{"test": "history"}]

input_body = {
  "log_data": {
    "log1": "l1",
    "log2": "l2",
    "log3": "l3",
    "log4": "l4"
  },
  "input_data": {
    "model_name": "1",
    "require_text": require_text,
    "history": history
  }
}

response = requests.post(api_url, json = input_body, verify=False)
print(response.json())