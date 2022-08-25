from typing import Union
import requests
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from prometheus_client import start_http_server

from fastapi import FastAPI
from pydantic import BaseModel
import time
import random
import string

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch) #Exporting logs to the screen
logger.addHandler(fh) #Exporting logs to a file


logger = logging.getLogger(__name__)

app = FastAPI()



class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


from pydantic import BaseModel



_INF =float('inf')

h = Histogram("Python_request_duration_seconds", "Histogram for the duration in seconds", buckets=(1,2,5,6,10, _INF))

@app.middleware("http")
async def log_requests(request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response
@app.get("/")
async def read_root():
    start = time.time()
    time.sleep(0.600)
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.get(url, {}, timeout=5)
    end = time.time()
    h.observe(end-start)
    return {"items": response.json() }


@app.get("/items")
async def read_root():
    start = time.time()
    time.sleep(0.600)
    end = time.time()
    h.observe(end-start)
    return [{"id": "1"}, {"id": "2"}]


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    start = time.time()
    time.sleep(0.600)
    end = time.time()
    h.observe(end-start)
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def save_item(item: Item):
    start = time.time()
    time.sleep(0.600)
    
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items'
    response = requests.post(url, data=item.json(), timeout=5, headers={'Content-Type': 'application/json'})
    end = time.time()
    h.observe(end-start)
    print(item.json())

    return response.text

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    start = time.time()
    time.sleep(0.600)
    
    url = 'https://62f6642a612c13062b4d71fe.mockapi.io/items/' + str(item_id) + '/'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.put(url, data=item.json(), headers=headers)
    end = time.time()
    h.observe(end-start)
    return response.text

@app.delete("/items/{item_id}")
async def deleteItem(item_id: int):
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