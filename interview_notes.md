# Topic 1: Django project structure and MVT pattern

## 1. What is MVT?

MVT Stands for Model View Template
where,
Model - Database structure and buisness data
View - Handles requests and responses
Template - Displays HTML to users

#### Think of it like a restaurant

**Model:**
Model = Kitchen Storage

- Contains all the ingredients and data
  Ex from the project:

```
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(...)
```

This defines how product data is stored in PostgerSQL.

**View**
View = Waiter
Receives customer requests and brings back responses.
Ex:

```
class ProductSearchView(APIView):
    def get(self, request):
        ...
```

Here,
_ProductSearchView_ is a view (an API endpoint)
_APIView_ is the DRF base class for handling HTTP requests
_get()_ is the method that runs when a client sends a GET request to that endpoint
_request_ contains information sent by the client (query params, headers, user, etc)

The view:

- Receives HTTP request
- Calls models/querysets
- Returns response

**Template**
Template = Menu Card
Shows infomation to users.
Ex:

```
<h1>{{ product.title }}</h1>
```

they are mostly used in traditional django websites

Since I have built a REST API
Using DRF
The flow is:

```
Request
   ↓
View
   ↓
Serializer
   ↓
Model
   ↓
Database
```

So barely used Templates

## 2. How is MVT different from MVC?

**MVC** stands for
Model
View
Controller,

Where _Controller_, handles business logic and user requests
The Controller acts as the middleman between the View and the Model

```
User Request
     ↓
 Controller
     ↓
   Model
     ↓
 Controller
     ↓
    View
     ↓
User Response
```

What a Controller does?

1. Recieves the user's request.
2. Validates/processes input
3. Calls the Model to read or update data
4. Chooses which View to render
5. Returns the response

Ex:
User clicks: GET/prodcucts/1
Controller:

```
def get_product(request, id):
    product = Product.objects.get(id=id)  # Model
    return render(request, "product.html", {"product": product})  # View
```

_Django uses **MVT** instead of MVC:_
the files **views.py** actually contains the logic that a Controller would handle in a traditional MVC

Django follows the MVT pattern. It is similar to MVC, but Django Views perform the role that Controllers usually perform in MVC. Templates are responsible for presentation, Models handle data, and View process requests and responses.

## 3. Role of Models

Models define database tables
Ex:

```
class Store(models.Model):
    name = models.CharField(...)
    location = models.CharField(...)
```

This becomes:

```
</> SQL
CREATE TABLE store (
    id,
    name,
    location
);
```

In this repo project
Models:

- Category
- Product
- Store
- Inventory
- Order
- OrderItem
  Each model corresponds to a database table

#### What is Django Model

A Django model is a **Python Class** _that defines the structure of a database table_.
_Django_ automatically _converts_ the _model_ in*to SQL tables through* **migrations.**

## 4. Role of Views

Views handle incoming requests.

Ex: GET/stores/1/orders/

The View:

1. Recives Request
2. Queries database
3. Retuens response

Ex:

```
class StoreOrdersView(APIView):
    def get(self, request):
        store = Order.objects.filter(...)
        return Response(...)
```

In this project
Views power:

- POST /orders/
- GET /stores/<id>/orders/
- GET /stores/<id>/inventory
- GET /api/search/products/
- GET /api/search/suggest/

#### What is the responsibility of a View?

A View recieves HTTP requests, executes business logic, interacts with models, and returns an HTTP response.

## 5. Role of Serializers

DRF Specific Topic

**Problem:**
Database objects look like:

```
Product(
    id=1,
    title="iPhone",
    price=70000
)
```

APIs need JSON:

```
{
  "id": 1,
  "title": "iPhone",
  "price": 70000
}
```

**Serializers performs this conversion.**
Ex:

```
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

Serializers does two things:
**Serialization**
Python -> JSON

```
Product
 ↓
JSON
```

**Deserialization**
JSON -> Python object

```
Request JSON
    ↓
Serializer
    ↓
Model instance
```

In this project, serializers used when;
Creating orders
Returning inventory
Returning products
Returning order lists

#### Why do we need serializers

Serializers convert Django model instances into JSON responses and validate incoming JSON data before creating or updating database records.

## 6. Role of URLs

URLs decide which View should handle a request

Ex:

```
urlpatterns = [
    path("orders/", OrderCreateView.as_view())
]
```

Flow:

```
POST /orders/
    ↓
URL Router
    ↓
OrderCreateView
    ↓
Response
```

In this project,
Ex:
/orders/
/stores/<id>/orders/
/stores/<id>/inventory/
/api/search/products/
api/search/suggest/

Each URL maps to a view

#### What is URL routing?

URL routing maps incoming URLs to the appropriate Django View so that the correct business logic is executed

## 7. Why split code into Apps?

Structure of this repo:

- products/
- stores/
- orders/
- search/

If didn't split into multiple apps, and everything goes for all apps in one folder then,
like only _one files of,_
_models.py_
_views.py_
_serializers.py_
Eventually:
it becomes 50000+ lines of code
Very difficult to maintain.

Instead:

- products/
  Handles: Product and Category
- stores/
  Handles: Store and Inventory
- orders/
  Handles: Order and OrderItem
- search/
  Handles: Search and Autocomplete

**Benefits:**

- Sepeation of concerns
  Each app has one responsibility
- Reusability
  Can move apps to another project
- Easier maintenance
  Developers know exactly where code belongs
- Better teamwork
  One developer works on Orders
  Another works on Search
  No conflicts

#### Why did you split your project into products, stores, orders, and search apps?

I separated the project into apps based on business domains. Products handles product-related logic, stores manage inventory and store data, order handles order processing, and search contains funcitonality. This improves maintainability, scalability, and team collaboratio.

**How entire project request flows**
When someone callsL:
POST /orders/

```
URL
 ↓
View
 ↓
Serializer Validation
 ↓
Order Model
 ↓
Inventory Model
 ↓
PostgreSQL
 ↓
Response
```

For successful order:

```
Order Created
 ↓
Celery Task Triggered
 ↓
Redis Broker
 ↓
Celery Worker
```

#### Walk me through an order creation request in your project

The request hits the URL router, which forwards it to the order creation view. The serializer validates the request data. Inside a database transaction, inventory is checked and deducted, the order and order items are created, and a response is returned. A Celery task is then triggered asynchronously for order confirmation processing.

##### Topic 1 drill

1. What is the difference between a Model and a Serializer?
2. Why doesn't a DRF API use Template much?
3. How does a request reach a View?
4. Why is your _orders_ logic in a separate app?
5. In MVC, which components is closest to a Django View?

---

# Topic 2: ORM, QuerySets, N+1 problems

project uses _select_related_ and optimized queries,

## 1. What is an ORM?

ORM is Object Relational Mapper
It is a layer that lets you interact with the database using Python objects instead of writing SQL manually

Suppose we want all products
Without ORM:
we would have required to write a SQL query

```
SELECT * FROM product;
```

With Django ORM

```
Product.objects.all()
```

Django converts this above query into SQL behid the scenes

### Why use ORM?

Easier to write
Instead of:

```
SELECT * FROM product
WHERE price > 1000;
```

You write:

```
Product.objects.filter(price__gt=1000)
```

**Database independent**
we can switch between:

- PostgreSQL
- MySQL
- SQLite

without rewriting queries
**Safer**
ORM protects against many SQL injection mistakes

In THIS project

```
###
Product.objects.filter(category=category)
###
Inventory.objects.filter(store=store)
###
Order.objects.filter(store=store)
```

Every one of these uses the ORM

#### WHat is an ORM

ORM stands for Object Relational Mapper. It allows us to interact with database tables using Python objects instead of writing raw SQL. Django ORM automatically converts Python Queries into SQL

## 2. What is a QuerySet?

A QuerySet is a collection of database records returned by the ORM.
Think of it as:
_Database Query Result_
Ex:

```
products = Product.objects.all()
```

_products_ is a QuerySet
Ex:

```
products = Product.objects.filter(price__gt=1000)
```

Again, a QuerySet

**QuerySets are lazy**
When we write:

```
products = Product.objects.all()
```

Django DOES NOT hit the database yet

Only when we actually use the data:

```
for p in products:
    print(p.title)
```

after this/using only does the Django exceute SQL

**Why?** does this happen/why lazy?
_Performance_
Django waits until data is actually needed

#### What is a QuerySet?

A QuerySet represents a collection of database records. It is generated by Django ORM and is lazily evaluated, meaning the SQL query is executed only when the data is actually needed

## 3. The N+1 Query Problem

This is one of the most common backed interview question

Imagine:

```
orders = Order.objects.all()

for order in orders:
    print(order.store.name)
```

Suppose there are 100 orders.

What happens?
**Query 1**

```
SELECT * FROM orders;
```

Gets all orders

Then for each order:

```
SELECT * FROM store WHERE id=...'
```

runs again.
100 times.

Total:

```
1 + 100
=
101 Queries
```

This is called:
**N+1 Query Problem**

Why is it bad?
More database round trips.
Ex:
**1000 orders**
becomes
**1001 SQL queries**
Very slow

In this project, most probably

```
orders = Order.objects.all()

for order in orders:
    order.store.name

# or

inventory.product.title
```

inside loops.

Without optimization/optimizing this: Huge number of queries

#### What is the N+1 query problem?

The N+1 query problem occurs when one query fethces a list of objects and then additional queries are executed for each object to retrieve related data. This results in many unnecessary database queries and poor performance

## 4. select_related() --Doubt (watch a yt vid)

It performs an **INNER JOIN** or **LEFT OUTER JOIN**
Used for:
**ForeignKey**: A Foreign Key is a column in one table that references the Primary key of the another table, creating a relationship between two tables
or
**OneToOne**
relationships.

Suppose:

```
class Order(models.Model):
    store = models.ForeignKey(Store)
```

Instead of:

```
orders = Order.objects.all()
```

Use:

```
orders = Order.objects.select_related("store")
```

Django now performs a SQL JOIN
It uses,
One Query:

```
SELECT *
FROM order
JOIN store
...
```

Instead of:
101 queries
We get:
1 query

**Visual**
Without:

```
Order
 ↓
Store
 ↓
Store
 ↓
Store
 ↓
Store
```

With:

```
Order + Store
```

Single Query

**When to use select_related?**
Use when accessing:

```
#for store
order.store

#for category
product.category

#for inventory store
inventory.store

#for inventory product
inventory.product
```

In this Project
Inventory endpoint:

```
Inventory.objects.select_related(
    "product",
    "category"
)
```

Order listing:

```
Order.objects.select_related(
    "store"
)
```

#### When should we use select_related?

We use select_related for ForeignKey and OneToOne relationships when we know we will access related objects. It performs a SQL JOIN and prevents N+1 query issues.

## 5. prefetch_related() --Doubt (watch a yt vid)

Used for:
**Reverse ForeignKey**
and
**ManyToMany**
relationships.

Ex:
_Order_
has many:
_OrderItems_

Suppose:

```
orders = Order.objects.all()

for order in orders:
    print(order.items.all())
```

**Problem**

```
1 query for orders
+
1 query per order for items
```

**N+1 again**.

Solution:

```
orders = Order.objects.prefecth_related(
  "items"
)
```

Django performs:
Query 1:

```
SELECT * FROM orders;
```

Query 2:

```
SELECT * FROM order_items;
```

Then joins in Python memory
Much faster

**When to use prefetch_related?**
Used for:

```
order.orderitem_set
#
category.products
#
many-to-many relationships
```

**In THIS Project**
Order -> Orderline

```
order = Order.objects.prefetch_related(
  "items"
)
or
order = Order.objects.prefetch_related(
  "order_items"
)
```

depending on related_name.

#### When should we use prefetch_related?

We use prefetch_related for reverse ForeignKey and ManyToMany relationships. Django performs separate queries and combines the results efficiently, reducing database hits.

## 6. select_related vs prefetch_related

```
| Feature      | select_related        | prefetch_related           |
| ------------ | --------------------- | -------------------------- |
| Relationship | ForeignKey, OneToOne  | Reverse FK, ManyToMany     |
| Uses JOIN    | Yes                   | No                         |
| Queries      | Single query          | Multiple optimized queries |
| Faster for   | Single related object | Collections of objects     |
```

**Easy memory trick**

1. One Object?
   Use
   _select_related()_
   Ex:
   _order.store_
   One Store.

2. Many Object?
   Use:
   _prefetch_related()_
   Ex:
   _order.items_
   Many Items.

## 7. How did YOU fix N+1?

**Order Listing API**
_GET /stores/<store_id>/orders_

Without optimization:

```
orders = Order.objects.filter(...)
```

Then serializer accesses:
_order.store_
_order.order_items_
Many extra queries

Better:

```
Order.objects.select_related(
  "store"
).prefetch_related(
  "items"
)
```

Now:
_Store loaded efficiently_
_OrderItems loaded efficiently_
No N+1

**Inventory API**
Endpoint:
_GET /stores/<store_id>/inventory/_

Without optimization:

```
inventory.product.title
inventory.product.category.name
```

Inside loop.
Each inventory row triggers extra queries.

Better:

```
Inventory.objects.select_related(
  "product",
  "product__category"
)
```

Now Django fetches:

```
Inventory
+
Product
+
Category
```

in one optimized query.

## Interview Questions

1. What is Django ORM?
   Django ORM allows developers to interact with the database tables using Python objects instead of writing SQL manually.

2. What is a QuerySet?
   A QuerySet is a collection of database returned by Django ORM. It is lazily evaluated and executes SQL only when data is needed

3. Explain the N+1 query problem.
   N+1 occurs when one query retrieves a list of objects and then additional queries are executed for each object to fetch related data. This creates unnecessary database load and slows down the application

4. What is select_related?
   select_related performs SQL JOINs and is used for ForeignKey and OneToOne relationships to reduce database queries

5. What is prefetch_related?
   prefetch_related is used for reverse ForeignKey and ManyToMany relationships.
   Django executes seperate queries and combines the results efficiently

6. How did you optimize queries in your project?
   I used select_related on inventory and order queries to fetch related Product Category, and Store data in a single query. For collections such as OrderItems, I used prefetch_related to avoid N+1 query and impre improve performance.

#### Tell me howyou optimized database performance in your progress.

My APIs used Django ORM with optimized QuerySets. To avoid N+1 query problems, I used select_related for ForeignKey relationships such as Inventory -> Product and Product -> Category, and prefetch_related for collections like Order -> OrderItems. This reduced unnecessary database queries and improved response times.

##### Quick Drill

1. Why is ORM better than writing raw SQL everywhere?
2. What does "QuerySets are lazy" mean?
3. What causes an N+1 query problem?
4. When would you use _select_related_?
5. When would you use _prefetch_related_?
6. For _Order -> Store_, which one would you use and why?
7. For _Order -> OrderItems_, which one would you use and why?
