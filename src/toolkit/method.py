from toolkit.lib import (model_config)

from langchain_core.prompts import PromptTemplate
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_ibm import WatsonxLLM

def generate_text(model_name: str, system_prompt: str, require_text: str, model_config: object, env_config: object) -> str:
    if system_prompt == None:
        system_prompt = """You are a log analysis expert who can analyze the content from the input log information and detect error messages, resource overload and system anomalies.\n"""
    
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
        print(response)
        out_text = response[0]['results'][0]['generated_text']
        return out_text
    except Exception as e:
        print("Error", e)
        return e