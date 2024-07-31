import traceback
from enum import Enum
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    price: Union[float, None] = None
    currency: Union[str, None] = "INR"
    tax: Union[int, None] = 18
    is_offer: Union[bool, None] = False


class ModelName(str, Enum):
    alexnet = "Alexnet"
    resnet = "Resnet"
    lenet = "Lenet"


@app.get("/")
async def get_invite(name: Union[str, None] = None):
    return {"invite": "Hello {user_name}".format(user_name=name if name else "World")}


@app.put("/item/update/{item_id}")
async def update_item(item_id: int, item: Item):
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "currency": item.currency,
        "tax_to_pay": item.price + item.tax,
        "is_offer": item.is_offer,
    }


@app.get("/models/{model_name}")
async def get_model_name(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "messgae": "Deep Learning FTW!"}
    elif model_name.value == "Lenet":
        return {"model_name": model_name, "messgae": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/")
async def greeting(name: Union[str, None] = "Deepak"):
    return {"greeting": f"Hello {name}"}


# Example Of Path Parameter and Query Paramete as Optional
@app.get("/item/{item_id}")
async def get_item(item_id: Union[int, None] = 0, skip: Union[bool, None] = False):
    try:
        if item_id == 0:
            return {"id": item_id, "skip": skip, "message": "No Item Exists"}
        elif item_id > 0 and item_id <= 10:
            return {"id": item_id, "skip": skip, "message": "Item Found"}
        elif item_id > 10:
            return {"id": item_id, "skip": skip, "message": "Item Out Stock"}
    except Exception as e:
        print(e, traceback.format_exc())
        return {"error": "Smomething Went Wrong"}


# Example Of Path Parameter
@app.get("/item/{item_id}/{user_id}")
async def get_item(item_id: int, user_id: int):
    try:
        if item_id == 0:
            return {"id": item_id, "user_id": user_id}
        elif item_id > 0 and item_id <= 10:
            return {"id": item_id, "user_id": user_id}
        elif item_id > 10:
            return {"id": item_id, "user_id": user_id}
    except Exception as e:
        print(e, traceback.format_exc())
        return {"error": "Smomething Went Wrong"}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/")
async def read_items(q: Annotated[Union[str, None], Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
