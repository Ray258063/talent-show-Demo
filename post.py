import requests
import time
from prompt import *

st = time.time()

with open("log_text/test_cpu.txt", "r", encoding="utf-8") as f:
    cpu_data = f.read()

with open("log_text/test_security_incident.txt", "r", encoding="utf-8") as f:
    security_incident_data = f.read()

with open("log_text/test_user_action.txt", "r", encoding="utf-8") as f:
    user_action_data = f.read()

# api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/question_generate_chat'
# # Question = "What's the problem with server?"
# Question = "伺服器有什麼問題嗎？"
# require_text = f"<User_question>{Question}</User_question>"
# history = []
# input_body = {"model_name":"meta-llama/llama-3-1-8b-instruct", "require_text": require_text, "history": history}

# response = requests.post(api_url, json = input_body, verify=False)
# print(response.json())

# 聊天 直接輸入問題和log
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/analysis_log_chat'
require_text = f"<cpu_utilization_log>{cpu_data}<cpu_utilization_log>\n<security_incident_log>{security_incident_data}<security_incident_log>\n<user_action_log>{user_action_data}<user_action_log>"
history = []
input_body = {"model_name":"meta-llama/llama-3-1-70b-instruct", "require_text": require_text, "history": history}

response = requests.post(api_url, json = input_body, verify=False)
print(response.json())

# RAG + 聊天
# api_url = 'http://127.0.0.1:8000/openapi/v1/watsonaix/rag_log_chat'

# with open("log_text/analysis_result.txt", "r", encoding="utf-8") as f:
#     analysis_result = f.read()

# with open("log_text/solution.txt", "r", encoding="utf-8") as f:
#     solution_data = f.read()

# require_text = f"<analysis_result>{analysis_result}</analysis_result>\n<Related_solutions>{solution_data}</Related_solutions>"
# history = []

# input_body = {
#   "model_name": "meta-llama/llama-3-1-70b-instruct",
#   "require_text": require_text,
#   "history": history
# }

# response = requests.post(api_url, json = input_body, verify=False)
# print(response.json())