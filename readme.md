# 說明
- 目前寫3個port 
- 第一個是一問一答 需要將任務內容 輸入資料一起輸入給模型 不限log分析(預設是log分析 所以system prompt可不輸入) 可自由輸入系統提示詞和任務需求 裡面會將他們合起來
- 第二個限制為log分析 同樣要把log資料和使用者提問一起輸入 有聊天歷史紀錄
- 第三個有RAG 但資料目前開發中

# Set Up
## 1. Install Dependency
```bash
pip install --no-cache-dir -r requirements.txt
```

## 2. Start Fast API
```bash
cd src/
uvicorn main:app --reload
```

# Talent Analyze log API

## Request
### Curl
#### 一問一答
``` bash
curl -X 'POST' \
  'http://127.0.0.1:8000/openapi/v1/watsonai/analysis_log?model_name=meta-llama%2Fllama-3-1-70b-instruct&system_prompt=1&require_text=2' \
  -H 'accept: application/json' \
  -d ''
```

#### 聊天
``` bash
curl -X 'POST' \
  'http://127.0.0.1:8000/openapi/v1/watsonaix/analysis_log_chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_name": "1",
  "require_text": "2",
  "history": ["3"]
}'
```

#### 聊天 + RAG
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/openapi/v1/watsonaix/rag_log_chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "log_data": {
    "log1": "l",
    "log2": "o",
    "log3": "g",
    "log4": "1"
  },
  "input_data": {
    "model_name": "2",
    "require_text": "3",
    "history": ["4"]
  }
}'
```

## Response

```json
{"analysis": "result"}
```

```json
{"analysis": "result", "history": []}
```

## Errors
### Not Input Error
- 400 Not input model name or require

## Python
POST
```python
import requests
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonxai/analysis_log'

param = {"model_name":"meta-llama/llama-3-1-70b-instruct", "system_prompt":"", "require_text": require_text}

response = requests.post(api_url, params=param)
print(response)
```

### 備註
- 用英文寫提示詞效果較好
- API KEY需要申請 加在.env