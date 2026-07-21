from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import products

app = FastAPI(title="Mini E-Commerce API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
