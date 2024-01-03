import pprint
from datetime import datetime

import pymongo as pyM

# conectando ao MongoDB
cliente = pyM.MongoClient("mongodb+srv://<usuario>:<senha>@cluster0.mihql7t.mongodb.net/?retryWrites=true&w=majority")


db = cliente.bank
collection = db.bank_collection
print(db.bank_collection)

# definição de informações para compor o doc
camila = {
    "id": 1,
    "nome": "Camila das Caramalheiras",
    "cpf": 369258147,
    "endereco": "Rua das primaveras",
    "date": datetime.utcnow()
}

# Bulk Inserts

novos_usuarios = [{

    "id": 2,
    "nome": "Josefa da Silva",
    "cpf": 147258369,
    "endereco": "Rua das auroras",
    "date": datetime.utcnow()

}, {

    "id": 3,
    "nome": "Katarina Avileneve",
    "cpf": 789456123,
    "endereco": "Rua das ortências",
    "date": datetime.utcnow()

}, {

    "id": 4,
    "nome": "Travarilha Avileneve",
    "cpf": 159632874,
    "endereco": "Rua das Trapaças",
    "date": datetime.utcnow()

}]

# preparando para submeter as infos ao Banco de Dados
posts = db.posts

# Submetendo um unico cliente
inserindo_cliente = posts.insert_one(camila).inserted_id
print(inserindo_cliente)

# submetendo vários clientes
inserindo_varios_clientes = posts.insert_many(novos_usuarios).inserted_ids
print(inserindo_varios_clientes)
