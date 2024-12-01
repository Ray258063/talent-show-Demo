from toolkit.lib import (model_config, env_config, LogData)
from toolkit.prompt_lib import *
from langchain_core.prompts import PromptTemplate
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_ibm import WatsonxLLM

import re
import pickle

def generate_text(model_name: str, system_prompt: str, require_text: str, model_config: object, env_config: object) -> str:
    if system_prompt == None:
        system_prompt = """Analyze the content from the input log information and detect error messages, resource overload and system anomalies.\n"""
    
    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        params = {
            "min_new_tokens": 1,
            "max_new_tokens": 300,
            "seed": 42
        }
    )
    try:
        # PromptTemplate.from_template(system_prompt)
        response = watsonx_llm.generate([system_prompt + require_text])
        print("生成結果:\n", response)
        out_text = response[0]['results'][0]['generated_text']
        return out_text
    except Exception as e:
        print("Error", e)
        return e

def question_generate_chat(model_name: str, require_text: str, history: list, model_config: object, env_config: object) -> str:
    
    if len(history) == 0:
        require_message = [
            {
                "role": "system",
                "content": question_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": require_text
                    }
                ]
            }
        ]
    else:
        input_text = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": require_text
                }
            ]
        }
        history.append(input_text)
        require_message = history

    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        params = {
            "max_tokens": 300
        }
    )
    
    try:
        response = watsonx_llm.chat(messages=require_message)
        print("生成結果:\n", response["choices"][0]["message"]["content"])
        history = process_history(response["choices"][0]["message"], require_message)
        out_text = response["choices"][0]["message"]["content"]
        match = re.search(r"<log_category>(.*?)</log_category>", out_text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            log_category_list = content.split("\n")
            print(log_category_list)
            return log_category_list, history
        else:
            print("未找到匹配內容。")
            all_log_list = ["Troubleshooting messages","security incident","port state",
            "protocol activity","Hardware and resource usage","System events","User action"]
            return all_log_list, history
    except Exception as e:
        print("Error", e)
        return e

def generate_chat(model_name: str, require_text: str, history: list, model_config: object, env_config: object) -> str:
    
    if len(history) == 0:
        require_message = [
            {
                "role": "system",
                "content": first_cpu_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": require_text + first_cpu_reply
                    }
                ]
            }
        ]
    else:
        input_text = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": require_text
                }
            ]
        }
        history.append(input_text)
        require_message = history

    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        params = {
            "max_tokens": 300
        }
    )
    
    try:
        response = watsonx_llm.chat(messages=require_message)
        print("生成結果:\n", response["choices"][0]["message"]["content"])
        out_text = response["choices"][0]["message"]["content"]
        history = process_history(response["choices"][0]["message"], require_message)
        return out_text, history
    except Exception as e:
        print("Error", e)
        return e

def process_history(generate_text, history):
    history.append(generate_text)
    return history

def generate_rag_chat(log_data:LogData, model_name: str, require_text: str, history: list, model_config: object, env_config: object) -> str:
    
    # with open('vector_store.pkl', 'rb') as f:
    #     loaded_vectorstore = pickle.load(f)
    # retriever = loaded_vectorstore.as_retriever()
    # relevant_documents = retriever.invoke("程式語言")

    # require_text = process_require_text(log_data, relevant_documents, require_text)

    if len(history) == 0:
        require_message = [
            {
                "role": "system",
                "content": second_cpu_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": require_text + second_cpu_reply
                    }
                ]
            }
        ]
    else:
        input_text = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": require_text
                }
            ]
        }
        history.append(input_text)
        require_message = history

    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        params = {
            "max_tokens": 500
        }
    )
    
    try:
        response = watsonx_llm.chat(messages=require_message)
        print("生成結果:\n", response["choices"][0]["message"]["content"])
        out_text = response["choices"][0]["message"]["content"]
        history = process_history(response["choices"][0]["message"], require_message)
        return out_text, history
    except Exception as e:
        print("Error", e)
        return e

def process_require_text(log_data, relevant_documents, require_text):
    input_log = f"""<Log1>{log_data.log1}</Log1>
    <Log2>{log_data.log2}</Log2>
    <Log3>{log_data.log3}</Log3>
    <Log4>{log_data.log4}</Log4>
    """
    input_solution = ""
    return input_log + require_text
