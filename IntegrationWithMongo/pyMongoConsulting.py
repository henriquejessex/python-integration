import pprint
import textwrap
from datetime import datetime

import pymongo as pyM

# conectando ao MongoDB
cliente = pyM.MongoClient("mongodb+srv://henriquejessex:3691@cluster0.mihql7t.mongodb.net/?retryWrites=true&w=majority")

db = cliente.test
posts = db.posts
c = 1
for post in posts.find():

    print("\nNúmero da ocorrência: ", c)
    print("\t\t", pprint.pprint(post))
    c += 1

print("\nNumero de posts com busca filtrada")
print("\t\t", posts.count_documents({"text": "Mongo is Fun"}))
