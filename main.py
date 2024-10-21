from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class ItemsEnum(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items_any_type/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.get("/items_integer/{item_id}")
async def read_item_integer(item_id: int):
    return {"item_id": item_id}


@app.get("/items_enum/{items_enum}")
async def get_items_enum(items_enum: ItemsEnum):
    return {"Item Enum": items_enum}


@app.get("/items/")
async def read_query_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item_optional(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
