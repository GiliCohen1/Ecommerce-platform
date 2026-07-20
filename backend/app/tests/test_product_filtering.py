from fastapi.testclient import TestClient


def test_filter_by_name_case_insensitive(client: TestClient):
    r = client.get("/products?name=python")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    assert all("python" in p["name"].lower() for p in data["data"])

    r2 = client.get("/products?name=PYTHON")
    assert r2.json()["total"] == data["total"]


def test_filter_by_category(client: TestClient):
    r = client.get("/products?category=ebook")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert all(p["category"] == "ebook" for p in data["data"])


def test_combined_filter(client: TestClient):
    r = client.get("/products?name=system&category=ebook")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["data"][0]["id"] == "prod-003"


def test_sort_by_price_asc(client: TestClient):
    r = client.get("/products?sort_by=price&order=asc")
    assert r.status_code == 200
    prices = [p["price"] for p in r.json()["data"]]
    assert prices == sorted(prices)


def test_sort_by_price_desc(client: TestClient):
    r = client.get("/products?sort_by=price&order=desc")
    assert r.status_code == 200
    prices = [p["price"] for p in r.json()["data"]]
    assert prices == sorted(prices, reverse=True)


def test_sort_by_name_asc(client: TestClient):
    r = client.get("/products?sort_by=name&order=asc")
    assert r.status_code == 200
    names = [p["name"].lower() for p in r.json()["data"]]
    assert names == sorted(names)


def test_filter_no_results(client: TestClient):
    r = client.get("/products?category=nonexistent-category")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["data"] == []


def test_get_product_by_id_found(client: TestClient):
    r = client.get("/products/prod-001")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "prod-001"
    assert "longDescription" in data
    assert isinstance(data["reviews"], list)
    assert len(data["reviews"]) > 0


def test_get_product_by_id_not_found(client: TestClient):
    r = client.get("/products/prod-999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()
