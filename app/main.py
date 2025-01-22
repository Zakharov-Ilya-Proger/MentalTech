from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.endpoints.analyzes import analyzes
from app.endpoints.clients import clients
from app.endpoints.sing import sing

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],)


app.include_router(sing, prefix="/sing")
app.include_router(clients, prefix="/clients")
app.include_router(analyzes, prefix="/analyses")
