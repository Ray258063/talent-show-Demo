import os
from fastapi import APIRouter, Response, status
from asyncio import get_event_loop, Lock
import asyncio
from dotenv import load_dotenv
from toolkit.method import *
from toolkit.lib import (AnalyzeResponse, ChatResponse, LogCategoryResponse, LogData, InputFormat, Errors, HTTPErrorResult, catch_error, healthcheck, env_config, model_config)
import concurrent.futures

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials

if __name__ == 'routers.classifier_v1':
    TAG_MODEL_VERSION = 'v1'
    router = APIRouter(prefix='/v1/watsonaix', tags=[TAG_MODEL_VERSION])
    lock = Lock()
    EXECUTOR = concurrent.futures.ThreadPoolExecutor()
    

@router.on_event("startup")
async def startup():
    
    try:
        load_dotenv() 
        env_config.WATSONX_API_KEY = os.environ['WATSONX_API_KEY']
        env_config.watsonx_project_id = os.environ['WATSONX_PROJECT_ID']
        env_config.region = os.environ['REGION']

        credentials = Credentials(
            url = f"https://{env_config.region}.ml.cloud.ibm.com",
            api_key = env_config.WATSONX_API_KEY,
        )
        model_config.Client = APIClient(credentials)

        healthcheck.get_env = True
    except:
        healthcheck.get_env = False
    healthcheck.model_loaded = True

# health_check
@router.get('/alive')
async def liveness_probe():
    return {'status': 'ok'}

@router.get("/ready", status_code=200)
def readiness_probe(response: Response) -> healthcheck:
    if healthcheck.model_loaded and healthcheck.get_env:
        return healthcheck(status='Readiness check succeeded.', model_loaded=True, get_env=True)
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return healthcheck(status='Readiness check failed.')

@router.post('/analysis_log', responses={
    200: {'model': AnalyzeResponse},
    400: {'model': HTTPErrorResult},
    500: {'model': HTTPErrorResult},
})
@catch_error
async def watsonx_generate(model_name:str = "", system_prompt:str = None, require_text:str = None):
    if model_name == "" or require_text == None or require_text == "":
        return Errors.NO_INPUT_ERROR
    event_loop = get_event_loop()
    async with lock:
        analysis_result = await event_loop.run_in_executor(None, generate_text, model_name, system_prompt, require_text, model_config, env_config)
    return AnalyzeResponse(analysis=analysis_result)

@router.post('/question_generate_chat', responses={
    200: {'model': LogCategoryResponse},
    400: {'model': HTTPErrorResult},
    500: {'model': HTTPErrorResult},
})
@catch_error
async def watsonai_question_chat(input_data:InputFormat):
    model_name = input_data.model_name
    require_text = input_data.require_text
    history = input_data.history
    
    if model_name == "" or require_text == None or require_text == "":
        return Errors.NO_INPUT_ERROR
    event_loop = get_event_loop()
    async with lock:
        log_category_list, history = await event_loop.run_in_executor(None, question_generate_chat, model_name, require_text, history, model_config, env_config)
    return LogCategoryResponse(log_category_list=log_category_list, history=history)

@router.post('/analysis_log_chat', responses={
    200: {'model': ChatResponse},
    400: {'model': HTTPErrorResult},
    500: {'model': HTTPErrorResult},
})
@catch_error
async def watsonai_chat(input_data:InputFormat):
    model_name = input_data.model_name
    require_text = input_data.require_text
    history = input_data.history
    
    if model_name == "" or require_text == None or require_text == "":
        return Errors.NO_INPUT_ERROR
    event_loop = get_event_loop()
    async with lock:
        analysis_chat_result, history = await event_loop.run_in_executor(None, generate_chat, model_name, require_text, history, model_config, env_config)
    return ChatResponse(analysis=analysis_chat_result, history=history)

@router.post('/rag_log_chat', responses={
    200: {'model': ChatResponse},
    400: {'model': HTTPErrorResult},
    500: {'model': HTTPErrorResult},
})
@catch_error
async def watsonai_rag_chat(log_data:LogData, input_data:InputFormat):
    model_name = input_data.model_name
    require_text = input_data.require_text
    history = input_data.history
    
    if model_name == "" or require_text == None or require_text == "":
        return Errors.NO_INPUT_ERROR
    event_loop = get_event_loop()
    async with lock:
        analysis_chat_result, history = await event_loop.run_in_executor(None, generate_rag_chat, log_data, model_name, require_text, history, model_config, env_config)
    return ChatResponse(analysis=analysis_chat_result, history=history)