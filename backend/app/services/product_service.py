import json
import os
from typing import Optional

from app.models.product import ProductDetail, ProductSummary
from app.services import cache_service

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")

TTL_LIST = 300
TTL_DETAIL = 600

_products: Optional[list[dict]] = None


def _load_products() -> list[dict]:
    global _products
    if _products is None:
        with open(DATA_PATH, encoding="utf-8") as f:
            _products = json.load(f)
    return _products


def _make_list_key(name: Optional[str], category: Optional[str], sort_by: str, order: str) -> str:
    n = name.lower() if name else "_"
    c = category.lower() if category else "_"
    return f"ecom:products:q:{n}:{c}:{sort_by}:{order}"


def get_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: str = "name",
    order: str = "asc",
) -> tuple[list[ProductSummary], int]:
    cache_key = _make_list_key(name, category, sort_by, order)
    cached = cache_service.cache_get(cache_key)
    if cached:
        data = json.loads(cached)
        return [ProductSummary(**p) for p in data["items"]], data["total"]

    products = _load_products()

    if name:
        products = [p for p in products if name.lower() in p["name"].lower()]
    if category:
        products = [p for p in products if p["category"] == category]

    reverse = order == "desc"
    if sort_by == "price":
        products = sorted(products, key=lambda p: p["price"], reverse=reverse)
    else:
        products = sorted(products, key=lambda p: p["name"].lower(), reverse=reverse)

    summaries = [ProductSummary(**p) for p in products]
    total = len(summaries)

    payload = json.dumps({"items": [s.model_dump() for s in summaries], "total": total})
    ttl = TTL_LIST if (not name and not category) else TTL_LIST // 2
    cache_service.cache_set(cache_key, payload, ttl)

    return summaries, total


def get_product_by_id(product_id: str) -> Optional[ProductDetail]:
    cache_key = f"ecom:product:{product_id}"
    cached = cache_service.cache_get(cache_key)
    if cached:
        return ProductDetail(**json.loads(cached))

    products = _load_products()
    match = next((p for p in products if p["id"] == product_id), None)
    if match is None:
        return None

    detail = ProductDetail(**match)
    cache_service.cache_set(cache_key, detail.model_dump_json(), TTL_DETAIL)
    return detail
