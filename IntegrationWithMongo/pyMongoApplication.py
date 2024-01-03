import pprint
from datetime import datetime

import pymongo as pyM

# conectando ao MongoDB
cliente = pyM.MongoClient("mongodb+srv://henriquejessex:3691@cluster0.mihql7t.mongodb.net/?retryWrites=true&w=majority")


db = cliente.test
collection = db.test_collection
print(db.test_collection)

# definição de informações para compor o doc
post = {
    "author": "Camila",
    "text": "My first mongodb python",
    "tags": ["python", "mongodb", "mongodb+srv", "pymongo"],
    "date": datetime.utcnow()
}

# Bulk Inserts

new_posts = [{

    "author": "Tamara",
    "text": "New post",
    "tags": ["mongodb+srv", "pymongo", "bulk"],
    "date": datetime.utcnow()

}, {

    "author": "Katiane",
    "text": "Mongo is Fun",
    "tags": ["pymongo", "bulk"],
    "date": datetime.utcnow()

}]

# preparando para submeter as infos ao Banco de Dados
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

# recuperando dados
pprint.pprint(db.posts.find_one({"author": "Juliana"}))

# inserindo Bulk Post
result = posts.insert_many(new_posts).inserted_ids
print(result)


