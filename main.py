from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class ItemsEnum(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items_any_type/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.get("/items_integer/{item_id}")
async def read_item_integer(item_id: int):
    return {"item_id": item_id}


@app.get("/modeitems_enum/{items_enum}")
async def get_model(items_enum: ItemsEnum):
    return {"Item Enum": items_enum}
