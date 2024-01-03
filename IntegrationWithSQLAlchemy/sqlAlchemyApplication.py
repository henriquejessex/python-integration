from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, inspect, select, func
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'

    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        'Address', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(id= '{self.id}', name='{self.name}', fullname='{self.fullname})>"


class Address(Base):
    __tablename__ = 'email_address'

    # attributes
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)

    user = relationship(
        'User', back_populates='address'
    )

    def __repr__(self):
        return f"<Address(id={self.id}, email_address={self.email_address})>"


print(User.__tablename__)
print(Address.__tablename__)

# conexão com SQLite
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

check_engine = inspect(engine)

print(check_engine.get_table_names())
print(check_engine.default_schema_name)


with Session(engine) as session:
    juliana = User(
        name='juliana',
        fullname='Juliana Mascarenhas',
        address=[Address(email_address='julianam@gmail.com')]
    )

    sandy = User(
        name='sandy',
        fullname='Sandy Junior',
        address=[Address(email_address='sandyjunior@gmail.com')]
    )

    jesse = User(
        name='jesse',
        fullname='Jesse Henrique',
        address=[
            Address(email_address='jessehenrique@gmail.com'),
            Address(email_address='henrique@gmail.com')
        ]
    )

    patrick = User(name='patrick', fullname='patrick cardoso')

    # Persistência de Dados
    session.add_all([juliana, sandy, patrick, jesse])
    session.commit()

# Buscando usuários
stmt = select(User).where(User.name.in_(["juliana", "sandy", "patrick", "jesse"]))
print("\nBuscando usuários com nome")
for user in session.scalars(stmt):
    print(user)

# buscando endereços
stmt_address = select(Address).where(Address.user_id.in_([4]))
print("\nBuscando os endereços de email de jesse")
for address in session.scalars(stmt_address):
    print(address)

# Buscando usuarios de forma descendente7
print("\nBuscando usuarios de forma ordenada:")
stmt_order = select(User).order_by(User.fullname.desc())
for result in session.scalars(stmt_order):
    print(result)

# Juntando buscas com Join
print("\nBuscando infos com join_from:")
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

# conectando join para exibir match
print("\nBuscando com connection")
connection = engine.connect()
connection_results = connection.execute(stmt_join)
for result in connection_results:
    print(result)

# conectando join para exibir match COM FATCHALL()
print("\nBuscando com connection fatch all")
connection = engine.connect()
connection_results = connection.execute(stmt_join).fetchall()
for result in connection_results:
    print(result)

# Contando ocorrencias no Bancos de Dados
print("\nTotal de instâncias em User:")
stmt_contador = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_contador):
    print(result)

session.close()
