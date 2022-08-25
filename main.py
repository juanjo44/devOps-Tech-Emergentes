from typing import Union
import requests
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from prometheus_client import start_http_server

from fastapi import FastAPI
from pydantic import BaseModel
import random
import time

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

_INF =float('inf')

h = Histogram("Python_request_duration_seconds", "Histogram for the duration in seconds", buckets=(1,2,5,6,10, _INF))


@app.get("/")
def read_root():
    start = time.time()
    time.sleep(0.600)
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.get(url, {}, timeout=5)
    end = time.time()
    h.observe(end-start)
    return {"items": response.json() }

@app.get("/items")
def read_root():
    start = time.time()
    time.sleep(0.600)
    end = time.time()
    h.observe(end-start)
    return [{"id": "1"}, {"id": "2"}]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    start = time.time()
    time.sleep(0.600)
    end = time.time()
    h.observe(end-start)
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def save_item(item: Item):
    start = time.time()
    time.sleep(0.600)
    
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.post(url, data=item.json(), timeout=5, headers={'Content-Type': 'application/json'})
    end = time.time()
    h.observe(end-start)
    print(item.json())

    return response.text

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    start = time.time()
    time.sleep(0.600)
    
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items/' + str(item_id) + '/'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.put(url, data=item.json(), headers=headers)
    end = time.time()
    h.observe(end-start)
    return response.text

@app.delete("/items/{item_id}")
def deleteItem(item_id: int):
    start = time.time()
    time.sleep(0.600)
    
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items/' + str(item_id)
    response = requests.delete(url, timeout=5)
    end = time.time()
    h.observe(end-start)
    return response.text


@h.time()
def f():
  pass

with h.time():
  start_http_server(4000)