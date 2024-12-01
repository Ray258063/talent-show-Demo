import requests
import time
from prompt import *

st = time.time()

# 直接生成
# api_url = 'http://127.0.0.1:8000/openapi/v1/watsonxai/analysis_log'

with open("test_switch_log.txt", "r", encoding="utf-8") as f:
    log_data = f.read()

# require_text = f"<log_data>{log_data}<log_data>\n" + user_prompt

# param = {"model_name":"meta-llama/llama-3-1-70b-instruct", "system_prompt":system_prompt, "require_text": require_text}

# response = requests.post(api_url, params = param, verify=False) 
# print(response.json()['analysis'])
# print(time.time()-st)

# api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/question_generate_chat'
# # Question = "What's the problem with server?"
# Question = "伺服器有什麼問題嗎？"
# require_text = f"<User_question>{Question}</User_question>"
# history = []
# input_body = {"model_name":"meta-llama/llama-3-1-8b-instruct", "require_text": require_text, "history": history}

# response = requests.post(api_url, json = input_body, verify=False)
# print(response.json())

# 聊天 直接輸入問題和log
# api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/analysis_log_chat'
# Question = "What's the cpu problem with this log?"
# require_text = f"<log_data>{log_data}<log_data>"
# history = []
# input_body = {"model_name":"meta-llama/llama-3-1-70b-instruct", "require_text": require_text, "history": history}

# response = requests.post(api_url, json = input_body, verify=False)
# print(response.json())

# RAG + 聊天
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/rag_log_chat'

with open("solution.txt", "r", encoding="utf-8") as f:
    solution_data = f.read()

require_text = f"<log_data>{log_data}<log_data>\n<Related_solutions>{solution_data}</Related_solutions>"
history = []

input_body = {
  "log_data": {
    "log1": "l1",
    "log2": "l2",
    "log3": "l3",
    "log4": "l4"
  },
  "input_data": {
    "model_name": "meta-llama/llama-3-1-70b-instruct",
    "require_text": require_text,
    "history": history
  }
}

response = requests.post(api_url, json = input_body, verify=False)
print(response.json())