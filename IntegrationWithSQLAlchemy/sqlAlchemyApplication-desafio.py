"""
Created on Mar 20, 2022
@author: Jessé Henrique

    Desafios de integração com Python e SqlAlchemy - Trilha Python da DIO
"""
import pprint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    """
    Classe que representa o Cliente
    """
    __tablename__ = 'cliente'

    # attributes
    id = Column(Integer, primary_key=True)
    nome = Column(String(15))
    cpf = Column(String(50))
    endereco = Column(String)

    conta = relationship(
        'Conta', back_populates='cliente', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (f"<Cliente(id= '{self.id}', nome='{self.nome}', cpf='{self.cpf}', "
                f"endereco='{self.endereco}, conta='{self.conta})>")


class Conta(Base):
    """
    Classe que representa a conta
    """
    __tablename__ = 'conta'

    # attributes
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tipo = Column(String(50))
    agencia = Column(String(10))
    numero = Column(Integer)
    saldo = Column(Float)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)

    cliente = relationship(
        'Cliente', back_populates='conta'
    )

    def __repr__(self):
        return (f"<Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, "
                f"numero={self.numero}, saldo={self.saldo})>")


# Verificando os nomes das Tables
pprint.pprint(Cliente.__tablename__)
pprint.pprint(Conta.__tablename__)

# conexão com SQLite
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

check_engine = inspect(engine)

pprint.pprint(check_engine.get_table_names())
pprint.pprint(check_engine.default_schema_name)

with Session(engine) as session:
    '''
    Inserindo dados e persistindo
    '''
    juliana = Cliente(
        nome='juliana',
        cpf='Juliana Mascarenhas',
        endereco='Rua das Ortencias',
        conta=[Conta(id=1, tipo='CONTA CORRENTE')]
    )

    catarina = Cliente(
        nome='catarina',
        cpf='Catarina Tabicurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=2, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    josefa = Cliente(
        nome='joseja',
        cpf='Josefa Tabicurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=3, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    tirulipa = Cliente(
        nome='tirulipa',
        cpf='Tirulipa Tabicurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=4, tipo='CONTA Corrente', agencia='0001', numero='2020', saldo=150)]
    )

    trabuzina = Cliente(
        nome='trabuzina',
        cpf='trabuzina Tabricurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=5, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )
    chulia = Cliente(
        nome='chulia',
        cpf='Chulia Xuranha',
        endereco='Rua das Ortencias',
        conta=[Conta(id=6, tipo='CONTA CORRENTE')]
    )

    xarai = Cliente(
        nome='xarai',
        cpf='Xarai Xarolina',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=7, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    varalituza = Cliente(
        nome='varalituza',
        cpf='Varalitura bitaquara',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=8, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    jozuelson = Cliente(
        nome='jozuelson',
        cpf='Jozuelson Tabicurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=9, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    armelinha = Cliente(
        nome='armelinha',
        cpf='Armelinha Tabicurra',
        endereco='Rua das Rapunzalas',
        conta=[Conta(id=10, tipo='CONTA POLPANÇA', agencia='0001', numero='2020', saldo=150)]
    )

    # Persistência de Dados
    session.add_all([juliana, catarina, josefa, tirulipa, trabuzina, chulia, xarai, varalituza, jozuelson, armelinha])
    session.commit()

# Buscando usuários
stmt = select(Cliente).where(Cliente.nome.in_(["catarina", "juliana", "armelinha"]))
print("\nBuscando usuários com nome")
for user in session.scalars(stmt):
    pprint.pprint(user)

# buscando Conta especifica por nome
stmt_conta = select(Conta).where(Conta.id.in_([2]))
print("\nBuscando Conta por nome de Cliente")
for conta in session.scalars(stmt_conta):
    pprint.pprint(conta)

# Buscando usuarios de forma descendente7
print("\nBuscando usuarios de forma ordenada:")
stmt_order = select(Cliente).order_by(Cliente.nome.desc())
for result in session.scalars(stmt_order):
    pprint.pprint(result)

# Juntando buscas com Join
print("\nBuscando infos com join_from:")
stmt_join = select(Cliente.nome, Conta.agencia).join_from(Conta, Cliente)
for result in session.scalars(stmt_join):
    pprint.pprint(result)

# conectando join para exibir match
print("\nBuscando com connection")
connection = engine.connect()
connection_results = connection.execute(stmt_join)
for result in connection_results:
    pprint.pprint(result)

# conectando join para exibir match COM FATCHALL()
print("\nBuscando com connection fatch all")
connection = engine.connect()
connection_results = connection.execute(stmt_join).fetchall()
for result in connection_results:
    pprint.pprint(result)

# Contando ocorrencias no Bancos de Dados
print("\nTotal de instâncias em Cliente:")
stmt_contador = select(func.count('*')).select_from(Cliente)
for result in session.scalars(stmt_contador):
    pprint.pprint(result)
