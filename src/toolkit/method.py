from toolkit.lib import (model_config, env_config, LogData)

from langchain_core.prompts import PromptTemplate
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_ibm import WatsonxLLM

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

def generate_chat(model_name: str, require_text: str, history: list, model_config: object, env_config: object) -> str:
    
    system_prompt = """\n"""
    
    if len(history) == 0:
        message = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        messages = message
    else:
        messages = history

    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        messages = messages,
        params = {
            "min_new_tokens": 1,
            "max_new_tokens": 300,
            "seed": 42
        }
    )
    try:
        response = watsonx_llm.generate([require_text])
        print("生成結果:\n", response)
        out_text = response[0]['results'][0]['generated_text']
        history = process_history(out_text, messages)
        return out_text, history
    except Exception as e:
        print("Error", e)
        return e

def process_history(generate_text, history):
    new_text = {
      "role": "assistant",
      "content": generate_text
    }
    history.append(new_text)
    return history

def generate_rag_chat(log_data:LogData, model_name: str, require_text: str, history: list, model_config: object, env_config: object) -> str:
    system_prompt = """Analyze the content from the input log information and detect error messages, resource overload and system anomalies.\n"""
    
    if len(history) == 0:
        message = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        messages = message
    else:
        messages = history

    watsonx_llm = ModelInference(
        model_id=model_name,
        api_client=model_config.Client,
        project_id=env_config.watsonx_project_id,
        messages = messages,
        params = {
            "min_new_tokens": 1,
            "max_new_tokens": 300,
            "seed": 42
        }
    )

    with open('vector_store.pkl', 'rb') as f:
        loaded_vectorstore = pickle.load(f)
    retriever = loaded_vectorstore.as_retriever()
    relevant_documents = retriever.invoke("程式語言")

    require_text = process_require_text(log_data, relevant_documents, require_text)
    try:
        response = watsonx_llm.generate([require_text])
        print("生成結果:\n", response)
        out_text = response[0]['results'][0]['generated_text']
        history = process_history(out_text, messages)
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
