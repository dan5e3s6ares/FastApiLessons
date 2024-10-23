from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

description = """
FirstAPILessons API helps you do awesome stuff. 🚀
"""

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
    title="FirstAPILessons",
    description=description,
    summary="Alguns passos iniciais com FastAPI",
    version="0.0.1",
    contact={
        "name": "Daniel Soares Martins",
        "url": "http://www.github.com/dan5e3s6ares",
        "email": "daniel@soaresmartins.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ItemsEnum(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@app.get("/", tags=["items"])
async def root():
    return {"message": "Hello World"}


@app.get("/items_any_type/{item_id}", tags=["items id"])
async def read_item(item_id):
    return {"item_id": item_id}


@app.get("/items_integer/{item_id}", tags=["items id"])
async def read_item_integer(item_id: int):
    return {"item_id": item_id}


@app.get("/items_enum/{items_enum}", tags=["items enum"])
async def get_items_enum(items_enum: ItemsEnum):
    return {"Item Enum": items_enum}


@app.get("/items/", tags=["items"])
async def read_query_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get(
    "/items/{item_id}",
    tags=["items id"],
    description="Get items from fake DB",
)
async def read_item_optional(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.post(
    "/items/",
    tags=["items"],
    response_model=Item,
    summary="Create an Item with payload",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
