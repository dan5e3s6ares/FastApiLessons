# FastApiLessons
Passo a passo de criação de um servidor em FastAPi, os passos estão separados por branch

## Hello World
- Step 1:
    > Create & Activate Python Env
    ```shell
    foo@bar:~$ python3 -m venv .env

    foo@bar:~$ source .env/bin/activate
    ```
    > Install dependencies
    ```bash
    foo@bar:~$ pip install "fastapi[standard]"
    ```
- Step 2:
    > Create main.py file
    ```shell
    touch main.py
    ```
- Step 2:
    > Type your first code with one endpoint
    ```python
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    ```

## Path Parameters
Você pode declarar “parâmetros” ou “variáveis” de caminho com a mesma sintaxe usada pelas strings de formato do Python

- Step 1:
    > Update main.py - add items_any_type endpoint
    ```python
    ...
    @app.get("/items_any_type/{item_id}")
    async def read_item(item_id):
        return {"item_id": item_id}

    ```
- Step 2:
    > Update main.py - add items_integer endpoint
    ```python
    ...
    @app.get("/items_integer/{item_id}")
    async def read_item_integer(item_id : int):
        return {"item_id": item_id}
    ```
- Step 3:
    > Update main.py - add models endpoint with options
    ```python
    from enum import Enum
    ...
    class ItemsEnum(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"
    ...
    @app.get("/items_enum/{items_enum}")
    async def get_items_enum(items_enum: ItemsEnum):
        return {"Item Enum": items_enum}
    ```

## Query Parameters
Quando você declara outros parâmetros de função que não fazem parte dos parâmetros de caminho, eles são automaticamente interpretados como parâmetros de “consulta”.

- Step 1:
    > Update main.py
    ```python
    ...
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    ...
    @app.get("/items/")
    async def read_query_items(skip: int = 0, limit: int = 10):
        return fake_items_db[skip : skip + limit]
    ```
    > [Consulta: http://127.0.0.1:8000/items/?skip=0&limit=1](http://127.0.0.1:8000/items/?skip=0&limit=1)

- Step 2:
    > Update main.py
    ```python
    ...
    @app.get("/items/{item_id}")
    async def read_item_optional(item_id: str, q: str | None = None):
        if q:
            return {"item_id": item_id, "q": q}
        return {"item_id": item_id}
    ```
    > [Consulta: http://127.0.0.1:8000/items/ABC?q=QWERTY](http://127.0.0.1:8000/items/ABC?q=QWERTY)
    > [Consulta: http://127.0.0.1:8000/items/ABC](http://127.0.0.1:8000/items/ABC)

## Request Body & PYDANTIC
Quando você precisa enviar dados de um cliente (digamos, um navegador) para a sua API, você os envia como um payload (request body).
Sua API quase sempre precisa enviar um payload de resposta. Mas os clientes não precisam necessariamente enviar payloads de solicitação o tempo todo, às vezes eles solicitam apenas um caminho, talvez com alguns parâmetros de consulta, mas não enviam um payload.
Para declarar um payload, você usa os modelos Pydantic com todo o seu poder e benefícios.

- Step 1:
    > Update main.py
    ```python
    ...
    from pydantic import BaseModel
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None
    ...
    @app.post("/items/")
    async def create_item(item: Item):
        return item
    ```
    Requisição COM erros
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"abc":"ABC"}'
    ```
    Requisição SEM erros
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "price": 56.1}'
    ```
    Requisição SEM erros com todos os campos
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "description": "Descrição ","price": 56.1, "tax": 6.8}'
    ```
    Requisição COM erro com todos os campos
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "description": "Descrição ","price": 56.1, "tax": "ASD"}'
    ```

## Swagger OpenAPI

### Interactive API docs
Agora, acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Você verá a documentação interativa automática da API (fornecida pela Swagger UI)

### Alternative API docs
E agora, vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Você verá a documentação automática alternativa (fornecida pelo ReDoc)

- Step 1:
    > Update main.py add tags
    ```python
    tags=["items"]
    tags=["items id"]
    tags=["items enum"]
    ```
- Step 2:
    > Update main.py
    ```python
    ...
    tags_metadata = [
        {
            "name": "items id",
            "description": "Operações com Items usando ID.",
        },
        {
            "name": "items",
            "description": "Operações Simples com Items",
        },
        {
            "name": "items enum",
            "description": "Operações com Items usando Enum de opções",
        },
    ]
    app = FastAPI(
        ...
        openapi_tags=tags_metadata,
    )
    ```
- Step 3
    > Update main.py add summary and description
    ```python
    ...
    @app.post(
        "/items/",
        tags=["items"],
        response_model=Item,
        summary="Create an Item",
        description="Create an Item with all the information",
    )
    ```
- Step 5
    > Update main.py add description with docstring
    ```python
    async def create_item(item: Item):
        """
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
        """
        ...
    ```