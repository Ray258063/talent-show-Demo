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
``` bash
curl -X 'POST' \
  'http://127.0.0.1:8000/openapi/v1/watsonai/analysis_log?model_name=meta-llama%2Fllama-3-1-70b-instruct&system_prompt=1&require_text=2' \
  -H 'accept: application/json' \
  -d ''
```


## Response

```json
{"analysis": "result"}
```

## Errors
### Not Input Error
- 400 Not input model name or require

## Python
POST
```python
import requests
api_url = 'http://127.0.0.1:8000/openapi/v1/watsonxai/analysis_log'

param = {"model_name":"meta-llama/llama-3-1-70b-instruct", "require_text": require_text}

response = requests.post(api_url, params=param)
print(response)
```

### 備註
- 用英文寫提示詞效果較好