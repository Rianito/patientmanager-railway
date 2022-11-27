from fastapi import FastAPI
from app.routers import patients
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DB_URL)
    app.database = app.mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(patients)

@app.get("/")
def read_home():
    return "Running!"
