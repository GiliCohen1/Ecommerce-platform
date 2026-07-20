# Mini E-Commerce Platform

A full-stack mini e-commerce application for digital products (e-books, software licenses, online courses).

**Stack:** Vue 3 + TypeScript + Pinia + Tailwind CSS + PrimeVue | Python FastAPI + Redis

---

## Quick Start (Docker)

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Frontend Setup (without Docker)

**Prerequisites:** Node.js 18+

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The app runs at http://localhost:5173.

**Run frontend tests:**
```bash
npm run test
```

---

## Backend Setup (without Docker)

**Prerequisites:** Python 3.12+, Redis (optional — app degrades gracefully without it)

```bash
cd backend
cp .env.example .env        # edit REDIS_URL if needed
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Swagger UI is at http://localhost:8000/docs.

**Run backend tests:**
```bash
py -m pytest app/tests/ -v
```

---

## API Documentation

### GET /products

Returns a filtered and sorted list of product summaries.

| Query param | Type | Default | Description |
|---|---|---|---|
| `name` | string | — | Case-insensitive substring match on product name |
| `category` | `online-course` \| `ebook` \| `software-license` | — | Exact category filter |
| `sort_by` | `name` \| `price` | `name` | Sort field |
| `order` | `asc` \| `desc` | `asc` | Sort direction |

**Response 200:**
```json
{
  "data": [
    {
      "id": "prod-001",
      "name": "Python Mastery Course",
      "price": 49.99,
      "shortDescription": "Go from beginner to advanced Python developer in 40 hours.",
      "thumbnailUrl": "https://picsum.photos/seed/prod001/400/300",
      "category": "online-course"
    }
  ],
  "total": 1,
  "filters": { "name": "python", "category": null, "sort_by": "price", "order": "asc" }
}
```

---

### GET /products/{id}

Returns full product details including long description and reviews.

**Response 200:**
```json
{
  "id": "prod-001",
  "name": "Python Mastery Course",
  "price": 49.99,
  "shortDescription": "...",
  "thumbnailUrl": "...",
  "category": "online-course",
  "longDescription": "A comprehensive 40-hour video course...",
  "reviews": [
    { "id": "rev-001", "author": "Alice K.", "rating": 5, "comment": "Best Python course!", "date": "2025-11-15" }
  ]
}
```

**Response 404:**
```json
{ "detail": "Product with id 'xyz' not found." }
```

---

### GET /health

```json
{ "status": "ok", "redis": "connected" }
```

---

## Architecture Decisions

### Cart: client-side only (Pinia)

The shopping cart is managed entirely in the Vue frontend via a Pinia store. No server-side cart endpoints exist. This decision was made because:

- The spec involves digital products with no user accounts or session persistence requirements
- The assignment explicitly permits this: *"handle cart client-side via Pinia if cart is not meant to persist server-side"*
- It keeps the backend focused on its core concern (product data) and makes the cart store trivially testable with Vitest

### Redis caching

Product list and detail responses are cached in Redis with TTL values:
- Filtered product lists: 120–300 seconds
- Single product details: 600 seconds

If Redis is unavailable, the backend degrades gracefully — all requests are served directly from the JSON data file with a warning logged. Redis is a performance layer, not a hard dependency.

### FastAPI over Flask

FastAPI was chosen for its auto-generated Swagger UI (`/docs`), built-in request validation via Pydantic, and native async support.

---

## Project Structure

```
ecommerce-platform/
├── frontend/               # Vue 3 + TypeScript
│   └── src/
│       ├── types/          # TypeScript interfaces (Product, CartItem, etc.)
│       ├── api/            # Axios HTTP layer
│       ├── stores/         # Pinia cart store
│       ├── router/         # Vue Router routes
│       ├── components/     # Reusable UI components
│       ├── views/          # Page-level components
│       └── tests/          # Vitest unit tests
└── backend/                # Python FastAPI
    └── app/
        ├── data/           # products.json mock database
        ├── models/         # Pydantic response models
        ├── services/       # Business logic + Redis cache
        ├── routers/        # HTTP route handlers
        └── tests/          # pytest unit tests
```
