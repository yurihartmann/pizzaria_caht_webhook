import os

import pymongo
from fastapi import FastAPI, Request

app = FastAPI()

client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client['pizzaria']
pedidos = db['pedidos']


@app.post(
    path='/webhook'
)
async def webhook(request: Request):
    json = await request.json()

    if json.get('order_id'):
        return pedidos.find_one({'_id': int(json.get('order_id'))})
    else:
        a = pedidos.find().sort("_id", -1)[0]
        json['_id'] = a['_id'] + 1
        pedidos.insert_one(json)
        return json
