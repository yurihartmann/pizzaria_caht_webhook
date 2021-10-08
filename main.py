import os

import pymongo
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client['pizzaria']
pedidos = db['pedidos']

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    path='/webhook'
)
async def webhook(request: Request):
    json = await request.json()

    if json.get('order_id'):
        pedido = pedidos.find_one({'_id': int(json.get('order_id'))})
        return pedido if pedido else {
            "_id": "-",
            "cep": "-",
            "borda": "-",
            "bebida": "-",
            "tipo_massa": "-",
            "sabor_pizza": "-",
            "tamanho_pizza": "-"
        }

    else:
        a = pedidos.find().sort("_id", -1)[0]
        json['_id'] = a['_id'] + 1
        pedidos.insert_one(json)
        return json
