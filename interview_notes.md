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

```mermaid
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
