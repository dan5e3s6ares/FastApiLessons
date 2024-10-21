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
