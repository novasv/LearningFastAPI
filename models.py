from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

#cria conexão do db
db = create_engine("sqlite:///banco.db")

#cria base do db
Base = declarative_base()

#criar as classes (todas são subclasses do declarative_base)
class Usuario(Base):
    __tablename__ = "usuarios"
    #nullable se refere a este valor não poder entrar nulo no db 
    #primary_key se refere a necessidade de toda tabela necessitar de um identificador
    #autoincrement se refere a autodefinição do valor do id
    #default se refere ao padrão do atributo
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)
    
    def __init__(self, nome, email, senha, ativo=True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin




class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDO = (
     #   ("PENDENTE", "PENDENTE"),
     #  ("CANCELADO", "CANCELADO"),
     #  ("ENTREGUE", "ENTREGUE") )

    id = id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, default="PENDENTE")
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    #itens =
    def __init__(self, usuario, status = "PENDENTE", preco = 0):
        self.usuario = usuario
        self.status = status
        self.preco = preco 

        
class ItemPedido(Base):
    __tablename__ = "pedido_itens"


    id = id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido",ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido


#cria a execução dos metadados do db(efetivamente cria o db)