from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.sql.ddl import CreateSchema

engine = create_engine('sqlite://')

metadata_obj = MetaData()

user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(40)),
    Column('nickname', String(40), nullable=False)

)

user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))

)

metadata_obj.create_all(engine)

# Persistindo Dados - inserindo dados
sql_insert = text("insert into user values(2, 'juliana', 'juliana@gmail.com', 'ju')")

engine.execute(sql_insert)

print("\nExecutando Statement SQL")
sql = text("select * from user")
result = engine.execute(sql)
for row in result:
    print(row)
