"""
Tests covering response schema, category counts, sort edge cases,
health endpoint, and input validation.
"""
from fastapi.testclient import TestClient

REQUIRED_SUMMARY_FIELDS = {"id", "name", "price", "shortDescription", "thumbnailUrl", "category"}
REQUIRED_DETAIL_FIELDS = REQUIRED_SUMMARY_FIELDS | {"longDescription", "reviews"}
REQUIRED_REVIEW_FIELDS = {"id", "author", "rating", "comment", "date"}


def test_all_products_returned_without_filters(client: TestClient):
    r = client.get("/products")
    assert r.status_code == 200
    assert r.json()["total"] == 9


def test_online_course_category_count(client: TestClient):
    r = client.get("/products?category=online-course")
    assert r.json()["total"] == 3


def test_software_license_category_count(client: TestClient):
    r = client.get("/products?category=software-license")
    assert r.json()["total"] == 3


def test_sort_by_name_desc(client: TestClient):
    r = client.get("/products?sort_by=name&order=desc")
    assert r.status_code == 200
    names = [p["name"].lower() for p in r.json()["data"]]
    assert names == sorted(names, reverse=True)


def test_filter_by_partial_name_multiple_matches(client: TestClient):
    r = client.get("/products?name=e")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 1
    assert all("e" in p["name"].lower() for p in data["data"])


def test_list_response_envelope_fields(client: TestClient):
    r = client.get("/products")
    body = r.json()
    assert "data" in body
    assert "total" in body
    assert "filters" in body
    assert isinstance(body["data"], list)
    assert isinstance(body["total"], int)


def test_product_summary_required_fields(client: TestClient):
    r = client.get("/products")
    for product in r.json()["data"]:
        assert REQUIRED_SUMMARY_FIELDS.issubset(product.keys()), (
            f"Missing fields in product {product.get('id')}"
        )


def test_product_detail_required_fields(client: TestClient):
    r = client.get("/products/prod-001")
    data = r.json()
    assert REQUIRED_DETAIL_FIELDS.issubset(data.keys())
    assert isinstance(data["reviews"], list)


def test_review_schema(client: TestClient):
    r = client.get("/products/prod-001")
    reviews = r.json()["reviews"]
    assert len(reviews) > 0
    for review in reviews:
        assert REQUIRED_REVIEW_FIELDS.issubset(review.keys())


def test_review_rating_in_valid_range(client: TestClient):
    r = client.get("/products/prod-001")
    for review in r.json()["reviews"]:
        assert 1 <= review["rating"] <= 5


def test_all_prices_are_positive(client: TestClient):
    r = client.get("/products")
    for product in r.json()["data"]:
        assert product["price"] > 0


def test_health_endpoint(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "redis" in body


def test_invalid_sort_by_param_returns_422(client: TestClient):
    r = client.get("/products?sort_by=invalid")
    assert r.status_code == 422


def test_invalid_order_param_returns_422(client: TestClient):
    r = client.get("/products?order=sideways")
    assert r.status_code == 422
