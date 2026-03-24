from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.constants.cors_configuration import ORIGINS, ALLOW_HEADERS, ALLOW_METHODS


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=False,
        allow_methods=ALLOW_METHODS,
        allow_headers=ALLOW_HEADERS,
    )
