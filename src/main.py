from fastapi import FastAPI
from routers import classifier_v1
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='ibmapi-analysis-log')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(classifier_v1.router, prefix='/openapi')
