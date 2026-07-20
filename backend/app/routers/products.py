from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.product import HealthResponse, ProductDetail, ProductListResponse
from app.services import cache_service, product_service

router = APIRouter()


@router.get("/products", response_model=ProductListResponse)
def list_products(
    name: Optional[str] = Query(None, description="Filter by name (case-insensitive substring)"),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    sort_by: Literal["price", "name"] = Query("name", description="Sort field"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort direction"),
):
    summaries, total = product_service.get_products(name, category, sort_by, order)
    return ProductListResponse(
        data=summaries,
        total=total,
        filters={"name": name, "category": category, "sort_by": sort_by, "order": order},
    )


@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: str):
    product = product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found.")
    return product


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", redis=cache_service.redis_status())
