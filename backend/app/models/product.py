from pydantic import BaseModel
from typing import Optional


class ReviewModel(BaseModel):
    id: str
    author: str
    rating: int
    comment: str
    date: str


class ProductSummary(BaseModel):
    id: str
    name: str
    price: float
    shortDescription: str
    thumbnailUrl: str
    category: str


class ProductDetail(ProductSummary):
    longDescription: str
    reviews: list[ReviewModel]


class ProductListResponse(BaseModel):
    data: list[ProductSummary]
    total: int
    filters: dict


class HealthResponse(BaseModel):
    status: str
    redis: str
