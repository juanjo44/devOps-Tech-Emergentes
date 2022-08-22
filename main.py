from typing import Union
import requests

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.get(url, {}, timeout=5)
    return {"items": response.json() }

@app.get("/items")
def read_root():
    return [{"id": "1"}, {"id": "2"}]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def save_item(item: Item):
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.post(url, data=item.json(), timeout=5, headers={'Content-Type': 'application/json'})
    print(item.json())

    return response.text

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items/' + str(item_id) + '/'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.put(url, data=item.json(), headers=headers)
    return response.text

@app.delete("/items/{item_id}")
def deleteItem(item_id: int):
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items/' + str(item_id)
    response = requests.delete(url, timeout=5)
    return response.text