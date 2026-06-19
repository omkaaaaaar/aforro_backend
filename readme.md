# Aforro Backend Assignment

A Django REST API backend for managing products, inventory, and store orders. The project focuses on inventory-aware order processing, product discovery, asynchronous task execution, and production-style backend engineering practices using PostgreSQL, Redis, Celery, Docker, and Django REST Framework.

---

## Features

### Inventory Management

- Category, Product, Store, Inventory, Order, and OrderItem models
- Inventory tracked per store-product combination
- One inventory record per store and product pair

### Order Processing

- Atomic order creation using database transactions
- Stock validation before confirmation
- Automatic inventory deduction for successful orders
- Order rejection when stock is insufficient
- Consistent inventory state even under concurrent requests

### Product Discovery

- Keyword search across:
  - Product title
  - Product description
  - Category name
- Filters:
  - Category
  - Minimum price
  - Maximum price
  - Store inventory
  - In-stock products
- Sorting:
  - Price (ascending)
  - Price (descending)
  - Newest products
- Pagination support
- Inventory quantity included when searching within a specific store

### Product Suggestions

- Lightweight autocomplete endpoint
- Minimum query length validation
- Prefix matches prioritized
- Limited to 10 suggestions per request

### Performance & Engineering

- Optimized querysets using `select_related`
- Pagination for large result sets
- Redis-backed API throttling
- Celery background task processing
- PostgreSQL as primary datastore
- Fully containerized with Docker Compose

---

## Tech Stack

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Faker
- drf-spectacular
- Docker & Docker Compose

---

## Project Structure

```text
aforro_backend/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
│
├── products/
├── stores/
├── orders/
├── search/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## Data Model

### Category

| Field | Type      |
| ----- | --------- |
| name  | CharField |

### Product

| Field       | Type         |
| ----------- | ------------ |
| title       | CharField    |
| description | TextField    |
| price       | DecimalField |
| category    | ForeignKey   |

### Store

| Field    | Type      |
| -------- | --------- |
| name     | CharField |
| location | CharField |

### Inventory

| Field    | Type         |
| -------- | ------------ |
| store    | ForeignKey   |
| product  | ForeignKey   |
| quantity | IntegerField |

Unique constraint:

```text
(store, product)
```

### Order

| Field      | Type                           |
| ---------- | ------------------------------ |
| store      | ForeignKey                     |
| status     | PENDING / CONFIRMED / REJECTED |
| created_at | DateTimeField                  |

### OrderItem

| Field              | Type         |
| ------------------ | ------------ |
| order              | ForeignKey   |
| product            | ForeignKey   |
| quantity_requested | IntegerField |

---

## API Endpoints

### Create Order

```http
POST /orders/
```

Request:

```json
{
  "store_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity_requested": 2
    }
  ]
}
```

Behavior:

- Validates inventory
- Confirms order if all items are available
- Deducts inventory
- Rejects order if any item lacks sufficient stock

---

### Store Orders

```http
GET /stores/<store_id>/orders/
```

Returns all orders for a store ordered by newest first.

---

### Store Inventory

```http
GET /stores/<store_id>/inventory/
```

Returns:

- Product title
- Price
- Category
- Available quantity

Sorted alphabetically by product title.

---

### Product Search

```http
GET /api/search/products/
```

Query Parameters:

| Parameter | Description           |
| --------- | --------------------- |
| q         | Search keyword        |
| category  | Category ID           |
| min_price | Minimum price         |
| max_price | Maximum price         |
| store_id  | Store ID              |
| in_stock  | true/false            |
| sort      | price, -price, newest |

Example:

```http
GET /api/search/products/?q=iphone&store_id=1&in_stock=true
```

---

### Product Suggestions

```http
GET /api/search/suggest/?q=iph
```

Features:

- Minimum 3 characters required
- Returns maximum 10 suggestions
- Prefix matches ranked first

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

## Redis Integration

Redis is used for API throttling on the product suggestion endpoint.

Policy:

```text
20 requests per minute per IP
```

This prevents abuse of the autocomplete endpoint while maintaining low response times.

---

## Celery Integration

A background task is triggered whenever an order is successfully created.

Current task:

```text
Order Confirmation Task
```

Flow:

```text
Order Created
      ↓
Celery Task Triggered
      ↓
Redis Broker
      ↓
Celery Worker
      ↓
Task Processed
```

This architecture allows non-blocking background processing and can be extended for emails, notifications, reporting, or analytics jobs.

---

## Seed Data

Generate sample data:

```bash
python manage.py seed_data
```

Creates:

- 12 Categories
- 1200 Products
- 25 Stores
- Inventory for 300 products per store

Useful for testing search, pagination, inventory, and order workflows.

---

## Running Locally

### 1. Clone Repository

```bash
git clone <repository-url>
cd aforro_backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
DB_NAME=aforro_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run Server

```bash
python manage.py runserver
```

---

## Running with Docker

Build containers:

```bash
docker compose build
```

Start services:

```bash
docker compose up
```

Services started:

- Django
- PostgreSQL
- Redis
- Celery Worker

---

## Running Tests

Execute all tests:

```bash
python manage.py test
```

Current test coverage includes:

- Successful order creation
- Order rejection on insufficient inventory
- Store inventory retrieval
- Product search
- Product suggestions

---

## Design Decisions

### Atomic Order Processing

Order creation is wrapped inside a database transaction to ensure:

- No partial inventory deductions
- No inconsistent order states
- Reliable stock management

### Query Optimization

Store inventory and order listing endpoints use optimized query patterns to avoid unnecessary database queries and improve scalability.

### Redis-backed Throttling

Autocomplete endpoints are often high-frequency endpoints. Redis-based throttling provides a lightweight way to prevent abuse while maintaining performance.

### Asynchronous Processing

Order-related background work is handled through Celery to keep API response times fast and enable future extensibility.
