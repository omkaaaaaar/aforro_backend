# DAY 1

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

---

# Topic 3: Database Design Basics

This topic is extremely important because it covers the models and then database around them
Since we have already built:
Category
Product
Store
Inventory
Order
OrderItem
This is a good position cause every database concept can be explained using this project

## 1. What are Tables, Rows, and Columns?

Think of a database like an Excel workbook

### Table

A table stores data about one type of thing
Ex:

```
Product Table
| id | title       | price |
| -- | ----------- | ----- |
| 1  | iPhone      | 70000 |
| 2  | Samsung S24 | 65000 |

```

The whole structure is a table

### Row

A row is one record
Ex:

```
id=1
title=iPhone
price=70000
```

This is one row

### Column

A column is one attribute
Ex:

```
title
price
category_id
```

Each column stores one type of information

**In this project:**
Tables:

```
Category
Product
Store
Inventory
Order
OrderItem
```

Each Django model becomes one database table

#### What is the difference between a table, row and column?

A table stores data for a specific entity, such as Product. A row represents a single record in that table, and a column represents an attribute of that record, such as title or price.

## 2. Primary Key

A primary key uniquely identifies each row
Ex:
Product

```
| id | title   |
| -- | ------- |
| 1  | iPhone  |
| 2  | Samsung |
```

Here:
**id**
is the primary key
No two rows can have the same primary key

**Django Example**

```
class Product(models.Model):
    title = models.CharField(...)
```

Django automatically creates:

```
id = AutoField(primary_key=True)
```

unless you specify you own

_Why Primary Keys are important?_
Imagine finding:
Product #3
Without a unique identifier, Django wouldn't know which row to update or delete.

#### What is a primary key?

A primary key is a column that uniquely identifies each row in a table. Django automatically creates an id field as the primpary key unless we define one ourselves.

## 3. Foreign Key

A foreign key creates a relationship between tables.

Ex:
Products belongs to a Category

```
class Product(models.Model):
    category = models.ForeignKey(Category)
```

Database
_Category_

```
| id | name   |
| -- | ------ |
| 1  | Phones |
```

_Product_

```
| id | title  | category_id |
| -- | ------ | ----------- |
| 1  | iPhone | 1           |
```

The Value: category_id = 1
points to: Category(id=1)

**Why Use Foreign Keys?**
Avoids duplicate data

Bad:
iPhone | Phones
Samsung | Phones
Pixel | Phones
Category repeated many times

Better:
Category Table
stores "Phone" once.

**In this project**
Product -> Category
Inventory -> Product
Inventory -> Store
Order -> Store
OrderItem -> Order
OrderItem -> Product
All are foreign key relationships

#### What is a foreign key?

A foreign key is a column that references the primary key of another table and creates a relationship between the two tables.

## 4. unique_together

This is directly from the project

Problem
Suppose Inventory table contains:

```
| store | product | quantity |
| ----- | ------- | -------- |
| 1     | 5       | 10       |
| 1     | 5       | 15       |
```

Same product and store twice
Now:
Actual Inventory?
10 or 15
Cofusing.

**Solution**
Only allows one inventory row per:
(store, product)
pair.

Django:

```
class Meta:
    unique_together = (
        "store",
        "product"
    )
```

Now after using this above query,
This gets invalid
_Store 1_
_Product 5_
appearing twice.

#### Why did you use unique_together in Inventory?

Each store should have only one inventory record for a product. The unique constraint on store and product prevents duplicate inventory rows and maintains data consistency.

## 5. Indexing

Imagine:
1 million products
You search:

```
Product.objects.get(id=999999)
```

Without index:
Check row 1
Check row 2
Check row 3
...
Very Slow

**Index = Book Index**
Instead of reading entire book:
"Django" → Page 125
Jumps directly

Database indexes work similarly

Example:

```
title = models.CharField(
    max_length=255,
    db_index=True
)
```

Now searches on title become faster

**Tradeoff**
Indexes improve:

```
SELECT
```

speed.
But slightly slow down:

```
INSERT
UPDATE
DELETE
```

because index must be maintained

In this project
Good candidates for indexes are:
Product.title
Product.category
Inventory.store
Inventory.product
Order.store
created_at
because they're frequently filtered

#### What is an Index?

An index is a database structure that helps locate rows faster. It improves read performance but adds some overhead to writes because the index must also be updated.

## 6. Normalization

Normalization means
Avoid duplicate data
Organize tables properly

Bad design:

```
| product | category |
| ------- | -------- |
| iPhone  | Phones   |
| Samsung | Phones   |
| Pixel   | Phones   |
```

Category repeated many times

Better:

```
Category
| id | name   |
| -- | ------ |
| 1  | Phones |

Product
| id | title  | category_id |
| -- | ------ | ----------- |
| 1  | iPhone | 1           |
```

Benefits:

- Less duplication
- Smaller storage
- Easier updates
- Better consistency

In this project
Category separate
Product separate
Store separate
Inventory separate
Orders separate

#### What is normalization?

Normalization is the process of organizing database tables to reduce redundancy and improve data consistency. Related information is stored in seperate tables and connected through keys.

## 7. Relationships

1. One-to-One
   One record maps to one record.
   Ex:
   User <-> Profile
   One profile per user
   Django:
   _OneToOneField_

2. One-to-Many
   Most common
   Ex:
   Category -> Many products
   One Category. Many products
   In this project:
   Category -> Product
   Store -> Inventory
   Store -> Order
   Order -> OrderItem
   All are one-to-many
   Django:
   _ForeignKey_

3. Many-to-Many
   Ex:
   Student <-> Course
   One student can join many courses
   One course can have many students
   Django:
   _ManyToManyField_

#### Difference between one-to-many and many-to-many?

In one-to-many, one record can have many related records, but each related record belongs to only one parent. In many-to-many, both sides can have multiple related records.

## 8. How Do the Models Relate?

Complete model relationship diagram:

```
Category
    |
    |
    v
 Product
    |
    |
    v
 Inventory
 ^        ^
 |        |
 |        |
Store     |
          |
          |
Order ----|
   |
   |
   v
OrderItem
   |
   |
   v
Product
```

Lets describe each relationship.

1. Category -> Product
   One Category
   Many Products
   Ex:
   Phones
   ├─ iPhone
   ├─ Samsung
   └─ Pixel

2. Store -> Inventory
   One Store
   Many Inventory Rows
   Ex:
   Mumbai Store
   ├─ iPhone: 10
   ├─ Pixel: 5
   └─ Samsung: 7

3. Product -> Inventory
   One Product
   Many Inventory Rows
   because same product exists in many stores

4. Store -> Order
   One Store
   Many Orders

5. Order -> OrderItem
   One Order
   Many OrderItems
   Ex:
   Order #101
   ├─ iPhone x2
   ├─ Charger x1

6. Product -> OrderItem
   One Product
   Many OrderItems

#### Explain the database design.

I designed seperated tables for Category, Product, Store, Inventory, Order, and OrderItem. Products belong to categories, inventory links products and stores, order belongs to stores, and order items connect products to orders. I used foreign keys to model one-to-many relationships and a unique consttraint on inventory to ensure only one inventory record exists per store-product pair.

## Imp Questions from Topic 3

1. What is a primary key?
   A unique identifier for each row in a table

2. What is a foreign key?
   A column that references other table's primary key and creates relationships

3. Why did you use unique_together?
   To ensure only one inventory record exists for each store-product combination

4. What is an index?
   A structure that speeds up database lookups and filtering

5. What is normalization?
   Organizing tables to reduce duplicate data and improve consistency

6. Explain relationships in your project.
   Category -> Product, Store -> Inventory, Product -> Inventory, Store -> Order, Order -> OrderItem, Product -> OrderItem

### Explain your database schema

My application has six main tables: Category, Product, Store, Inventory, Order, and OrderItem. Products belong to categories. Inventory acts as a bridge between stores and products and tracks stock quantity. Orders belong to stores, and OrderItems store the product inside each order. I used foreign keys for relationships and a unique constraint on Inventory to ensure one inventory record per store-product pair. The schema is normalized to avoid duplicare data and maintain consistency.

#### Quick Drill

1. Why do we need a primary key?
2. What problem does a foreign key solve?
3. WHy is _(store, product)_ unique in inventory?
4. What is benifit of indexing?
5. What is normalization?
6. Is _Category -> Product_ one-to-many or many-to-many?
7. Why did you create an _OrderItem_ table instead of storing products directly inside Order?

---

# Topic 4: Django Migrations

This topic is asked in almost all Django interviews because migrations are how DJango keeps the python models and the database schema in sync

## 1, What is Migration?

A migration is a file that tells Django:
_Here is what changed in my models. Update the database accordingly._

**Example:**
Initially:

```
class Product(models.Model):
    title = models.CharField(max_length=256)
```

Later you add:

```
class Poduct(models.Model):
    title = models.CharField(max_length=256)
    price = models.DecimalField(...)
```

The Python code is changed now, because of the addition
But PostgreSQL still has the old table.
Django needs a way to update the database.
That's what Migrations do.

**Real-Life Analogy**
Think of:
_models.py_
as a blueprint.
And:
_PostgreSQL_
as the actual building.
When the blueprint changes, we need construction instructions to update the building.
Migration files are those instructions.

#### What is migration?

A migration is a version-controlled file that records database schema changes and allows Django to apply these changes to the database safely.

## 2. makemigrations vs migrate

This is probably the most asked migration question

**Step 1**
You modify mode

```
class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.DecimalField(...)
```

**Step 2**
Run:

```
python manage.py makemigrations
```

Django compares:
_Current Models vs Preview Migration State_
and generate a migration file.
Ex:
_products/migrations/0002_add_price.py_

**Important**
At this point
_Database NOT changed yet_
Only a migration file is created.

**Step 3**
Run:

```
python manage.py migrate
```

Now Django executes SQL against PostgreSQK
Database is updated

EASY MEMORY TRICK
makemigrations -> _Create migratiion files_
migrate -> _Execute migration files_

#### Difference between makemigrations and migrate>

makemigrations create migration files based on model changes. migrate applies those migration files to the database and updates the schema

## 3. What Do Migrations Files Actually Contain?

Example migration:

```
class Migration(migrations.Migration):

    dependencies = [
      ("products","0001_initial),
    ]

    operations = [
      migrations.AddField(
         model_name="product",
         name="price",
         field=models.DecimalField(...)
      )
    ]
```

Django later converts this into SQL.

Something like
_ALTER TABLE product_
_ADD COLUMN price NUMERIC;_

**Key Idea**
Migration files are Python instructions describing database changes.
Not actual SQL
Django generate SQL from them.

Common Operations

1. Create Table
   migrations.CreateModel(...)

2. Add column
   migrations.AddField(...)

3. Remove column
   migrations.RemoveField(...)

4. Create Index
   migrations.AddIndex(...)

5. Add constraint
   migrations.AddConstraint(...)

#### What is stored inside a migration file?

Migration files contain Python operations that desribe schema changes such as creating tables, adding fields, removing fields, creating indexes, or adding constraints.

## 4. Common Migration Mistakes

**Mistake 1**
Changing models but forgetting migrations
Ex:
_price = models.DecimalField(...)_
But never running
_python manage.py makemigrations_
_python manage.py migrate_
Result:
Model and Database out of sync

**Mistake 2**
Deleting migration files manually
Bad:
_products/migrations_
_0001_initial.py_
_0002_add_price.py_
(delete them)
Now migration history becomes broken.

**Mistake 3**
Editing old migrations after deployment
Suppose:
_0001_initial.py_
already exists in production.
Never modify it.
Create a new migration instead.

**Mistake 4**
Not commiting migration files on Git.
Bad:
git add model.py
git commit
but forgot
migrations/
Now teammates can't update their database.

**Mistake 5**
Merge conflicts in migrations
Developer A:
0005*add_price.py
Developer B:
0005_add_status.py
Both create migration 0005
Conflict happens.
Need:
\_python manage.py makemigrations*
to generate a merge migration.

#### What migration problems have you seen?

Common issues include forgetting to run migrations, not committing migration files, deleting migration files manually, and migration conflicts when multiple developers modify models simultaneously

## 5. Why Migratipns Matter in a Team

Migrations provide a consistent and version-contolled way to manage database schema changes. They ensure developer and environment has the same database structure.

#### Questions might ask base on prj

1. How did you create your database tables?
   I defined Django models and used migrations. Django generate migration files, and I applied them using _python manage.py migrate_ which created the PostgreSQL tables.

2. What happens when you add a field to Product?
   After updating the model, I run _makemigrations_ to generate a migration file and then _migrate_ to apply the schema changes to the database

3. Why do migration files belong in Git?
   Migration files describe database changes. If they are not committed, other developers cannot reproduce the same database schema.

4. Can Django create SQL automatically?
   Yes. Django migrations generate the appropriate SQL statements and execute them when we run _migrate_

5. What is the difference between schema and data?
   Schema refers to the database structure such as tables, columns, indexes, and constraints. Data refers to the actual records stored inside those tables.

## Walk me through your Django Project

I built a Django REST API for inventory and order management. The project is divided into apps such as products, stores, orders, and search. Django models define the database scehma, serializers handles JSON conversion and validation, views process requests, and URL routes map endpoints to views. I used PostgreSQL as the database, optimized queries using _select_related_ and _prefetch_related_, enforced data consistency through foreign keys and unique constraints, and managed schema changes using Django migrations. Order creation is wrapped in _transaction.atomic()_ to ensure inventory updates remain consistent

#### Final Day-1 Quiz

1. What is the difference between MVT and MVC?

2. What is the role of serializers in DRF?

3. What is an ORM and why is it useful?

4. What is a QuerySet and what does "lazy evaluation" mean?

5. Explain the N+1 query problem

6. When would you use _select_related()_?

7. Why did you use a unique constraint on _(store, product)_ in inventory?

8. What is the difference between a primary key and a foreign key?

9. What is the difference between _makemigrations_ and _migrate_?

10. Why should migration files be committed to Git?

---

---

# DAY 2

---

# Topic 1: HTTP Methods & Status Codes

APIs are fundamentally built on HTTP.

Interviewrs often start with:
"Tell me what happens when someone calls your POST /orders endpoint."
To answer that well, you need to understand HTTP methods and status codes.

## 1. What is HTTP?

HTTP(HyperText Transfer Protocol) is the language that clients and servers use to communicate.
Ex:

```
Frontend
   ↓
POST /orders/
   ↓
Django API
   ↓
Response
```

Every API request contains:
_Method_
_URL_
_Headers_
_Body (optional)_

Ex:

```
POST /orders/
Content-Type: application/json

{
   "store_id": 1,
   "items": [...]
}
```

## 2. Types of Request

1. **GET**
   Used to: _Retrieve data_
   Should not change anything in the database.
   Ex: _GET /stores/1/orders/_

2. **POST**
   Used to: _Create a new resource_
   Ex: _POST /orders/_
   Request:
   {
   "store_id": 1,
   "items": [...]
   }
   Creates:
   Order
   OrderItems
   Inventory changes
   Database state changes, So POST is appropriate.
   Q. Whys is order creation a POST request?
   Because a new order is being created and database state changes. POST is used for resoure creation.

3. **PUT**
   Used to: _Replace an entire resource_
   Suppose product:
   {
   "title": "iPhone",
   "price": 70000
   }
   PUT:
   _PUT /products/1_
   Body:
   {
   "title": "iphone 15",
   "price": 80000
   }
   Entire object gets replaced.

4. **PATCH**
   Used to: _Update only specific fields_
   Ex:
   _PATCH /products/1/_
   Body:
   {
   "price": 80000
   }
   Only price changes.
   Everything else remains unchanged.

5. **DELETE**
   Used to:_Remove a resource_
   Ex:
   _DELETE /products/1/_
   Product removed.

**Requests used in this Project**

1. GET
   Used for:
   GET /stores/<store_id>/orders/
   GET /stores/<store_id>/inventory/
   GET /api/search/products/
   GET /api/search/suggest/
   Because they only retrieve data

2. POST
   Used for:
   POST /orders/
   Because it creates an order.

## 3. What is Idempotency

An operation is idempotent if performing it multiple times produce the same final result.

Ex:
**DELETE**
Delete product:
_DELETE /product/1/_
Run once:
_Product deleted_
Run again:
_Still deleted_
Final state unchanged
Idempotent.

**PUT**
_PUT /products/1/_
{
"price": 100
}
Run 10 times:
Final result:
_Price = 100_
Same outcome.
Idempotent.

**POST**
_POST /orders/_
Run Twice:
_Order #101_
_Order #102_
Two orders created.
Not idempotent.

**Which Methods Are Idempotent**

```
| Method | Idempotent?           |
| ------ | --------------------- |
| GET    | Yes                   |
| PUT    | Yes                   |
| PATCH  | Usually treated as No |
| DELETE | Yes                   |
| POST   | No                    |

```

#### Why Post is not idempotent?

Because sending the same POST request multiple times can create multiple resources and produce different results.

## 4. What are Safe Methods?

Safe Method: Do not modify server data.

Safe:
GET
HEAD
OPTIONS

Not safe:
POST
PUT
PATCH
DELETE
Because they change data.

#### What is different between safe and idempotent?

Safe methods do not modify data,. Idempotent methods may modify data, but repeated requests result in the same final state.
Ex: DELETE, is idempotent but not safe.

## 5. Important Status Codes

1. **200 OK**
   Request succeeded.
   Ex:
   _GET /stores/1/orders_
   returns:
   _200 Ok_

2. **201 Created**
   New resource successfully created
   Ex:
   _POST /orders/_
   Order created successfully
   Return:
   _201 Created_

3. **400 Bad Request**
   Client sent invalid data.
   Ex:
   {
   "store*id": null
   }
   Return:
   \_400 Bad Request*

4. **404 Not Found**
   Request resource doesn't exist
   Ex:
   _GET /stores/9999/orders_
   Store doesn't exist.
   Return:
   _404 Not Found_

5. **422 Unprocessable Entity**
   Request format is valid.
   But business rule fails.
   Ex:
   {
   "store_id": 1,
   "items": [
   {
   "product_id": 1,
   "quantity_request": 999
   }
   ]
   }
   JSON is valid.
   But inventory insufficient
   Business logic rejects order.
   Return:
   422 Unprocessable Entity

6. **500 Internal Server Error**
   Server crashed
   Ex:
   _Database down_
   _Unexpected exception_
   _Bug in code_
   Return:
   _500 Internal Server Error_

#### What would you return for a rejected order?

There are two possible designs. If rejected orders are still stored as Order records, I would return 201 Created with status=REJECTED because the resource was created successfully. If no order record is created and the request fails business validation, I would return 422 Unprocessable Entity.

1. Difference between GET and POST?
   GET retrieve data. POST creates resources and changes the server state

2. What is idempotency?
   An idempotent operation produces the final result even if it is executed multiple times.

3. Which HTTP methods are idempotent?
   GET, PUT, and DELETE are idempotent. POST is not.

4. What is a safe method?
   A safe method does not modify server data. GET is the most common safe method.

5. What status code should successful order creation return?
   201 Created

6. What status code should inventory storage return?
   Either 422 if the order is rejected before creation, or 201 if a rejected order resource is still created and stored.

#### Quick drill

- Why is GET /api/search/products/ a GET and not a POST?
- Why is POST not idempotent?
- What's the difference between 400 and 422?
- If a store doesn't exist, what status code should be returned?
- If an order is successfully created, what status code should be returned?
- What is the difference between safe and idempotent methods?
- Why might a team choose to return 201 for a rejected order?

---

# Topic 2: DRF Serializers & Views

This entire project is built using Django REST Framework(DRF).

A common interview sequence is:
"How does a request reach your API?"
"Where is validation performed?"
"What does a serializer do?"
"Why did you choose APIView"

## 1. What is Serializer?

A Serializer is DRF's way of:

1. Converting Python/Django objects -> JSON
2. Validating incoming JSON -> Python Objects

**Ex 1: Serialization**
Database object:

```
#Python
product = Product(
   id=1,
   title="iPhone",
   price=70000
)
```

Serializer converts it into:

```
#JSON
{
   "id": 1,
   "title": "iPhone",
   "price": 70000
}
This is what the frontednd recieves.
```

**Ex 2: Deserialization**
Incoming request:

```
#json
{
   "store_id": 1,
   "items": [
      {
         "product_id": 5,
         "quantity_requested": 2
      }
   ]
}
```

Serializer

- Validates fields
- Checks required fields
- Converts data into Python objects

In this Projext
For:
_POST /orders/_
Flow:

```
Request JSON
      ↓
OrderSerializer
      ↓
Validation
      ↓
Create Order
      ↓
Response JSON
```

#### Why do we need serializer?

Serializers convert Django model instances into JSON response and validate incoming request data before creating or updating records.

## 2. How DRF Validation Works

Suppose request:
{
"store_id": null
}
Serialzer:

```
serializer = OrderSerializer(data=request.data)
serializer.is_valid()
```

Validation runs.

If Invalid:

```
{
   "store_id":[
      "This field is required."
   ]
}
```

Return:
_400 Bad request_

**Validation Layers**

1. Field Validation
   Ex:
   _quantity_requested = serializers.IntegerField(min_value=1)_
   Rejects:
   {
   "quantity_requested": -5
   }

2. Custom Field Validation

```
def validate_quantity_requested(self, value):
    if value <= 0:
        raise serializers.ValidationError(...)
```

3. Object-Level Validation
   _def validate(self, data):_
   ...
   Used when validating multiple fields together.

In this project,
Examples:
store_id must exist
product_id must exist
quantity_requested > 0

#### Where does validation happen in DRF?

Validation is usually performed inside serializers using built-in field validation, custom field validators, and object-level validation methods.

## 3. APIView vs ViewSet

**APIView**
We manually define methods here
Ex:

```
class OrderCreateView(APIView):
    def post(self, request):
    ...
```

We decide here:
_get()_
_post()_
_put()_
_delete()_
ourselves

Advantage: More control, Good for custom business logic
In this project
_POST /orders/_
_GET /stores/<id>/orders_
_GET /stores/<id>/inventory_
were implemented with APIview most likely

**ViewSet**
DRF automatically provides common CRUD operations
Ex:

```
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
```

Automatically gives:
_GET_
_POST_
_PUT_
_PATCH_
_DELETE_
Less code.
More convention-based

**APIView**: More Control, More Code
**ViewSet**: Less Code, More Automation

#### Why did you use APIView instead of ViewSet?

My APIs contained custom business logic such as inventory validation, order, confirmation, stock deduction, and custom search behaviour. APIView gave me more control over request handling and response generation.

## 4. Authentication vs Permissions

**Authentication**
Authentication answers: Who are you?
Ex:
_Omkar logs in_
System identfies
_User = Omkar_

Common DRF authentication methods:
_SessionAuthentication_
_TokenAuthentication_
_JWT Authentication_

**Permissions**
Permissions answer: What are you allowed to do?
Ex:
User Identified
Now Check:
Can create orders?
Can delete products?
Can view inventory?

**Ex:**
Authentication: You're Omkar
Permission: You're Allowed to enter the room

## 5. Path Params vs Query Params vs Request Body

**Path Parameters**
Part of URL path
Ex:
_Get /stores/5/orders/_
Here:
_5_
is a path parameter

Purpose: Identify a specific resource

**Query Parameters**
Appear after:
_?_
Ex:
_GET /api/search/products/?category=2&min_price=1000_

Used for:

- Filtering
- Sorting
- Searching
- Pagination

**Request Body**
Data sent inside request
Usually in:
POST
PUT
PATCH

Ex:
_POST /orders/_
Body:
{
"store_id": 1
"items": [...]
}

Easy memory trick,
Path params: Identify resource
Query params: Filter resource
Body: Create/Update resource

#### Why is store_id in the path but cateory in query params?

store_id identifies the resource being accessed, while category is used to filter search results. Resource identifiers belong in the path, while filters belong in query parameters.

## 6. Pagination

Imagine:
1200 Products
from the seed data

**Without Pagination**:
_GET /api/search/products/_
returns:
1200 products
Huge response.
Slow.
Wasteful.

**With Pagination**:
Request:
_GET /api/search/products/?page=1_
Returns:

```
{
  "count": 1200,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

Only a subset is returned.

**Benefits of using Pagination**

1. Faster API
   Less data transferred

2. Less Memory
   Backend uses less RAM

3. Better UX
   Frontend loads quickly

#### Why does your search API need pagination?

The product table contains many records. Pagination limits the number of results returned per request, improving response time, reducing bandwidth usage, and providing a better user experience.

**Full Request Lifecycle in This Project**

Suppose:
_POST /orders/_

Request:
{
"store_id": 1,
"items": [...]
}

Flow:

```
URL
 ↓
APIView
 ↓
Serializer
 ↓
Validation
 ↓
Order Service Logic
 ↓
transaction.atomic()
 ↓
Database
 ↓
Serializer
 ↓
JSON Response
```

## Most Important Questions from this topic

1. What does serializer do?
   Converts Django objects to JSON and validates incoming JSON

2. Where does DRF validation happen
   Inside serializers through field validation and custom validation methods.

3. APIView vs ViewSet?
   APIView provides more control, while ViewSet automatically provides CRUD behavior.

4. Difference between authentication and permission?
   Authentication identifies the user. Permissions determine what actions they can perform.

5. Path parameter vs query parameter?
   Path parameters identify resources. Query parameter filters or modify how data is returned

6. Why use pagination?
   To reduce response size, improve performance, and handle large datasets efficiently.

#### Quick Drill

- why does DRF needs serializers?
- where should business validation happen: view or serializer?
- why might APIView be a better choice than ViewSet for you order API?
- is _store_id_ in /stores/5/orders/ a path param or query param?
- is ?category=1 a path param or a query param?
- Why would returning 1200 products in one response be a bad idea?
- What's the difference between authentication and permissions?

---

# Topic 3: Search & Autocomplete APIs
