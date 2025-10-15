from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido


order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def orders():
    """Esta é a rota padrão de pedidos da API. Todas as rotas dos pedidos precisam de autenticação"""
    return {"mensagem":"Você acessou a rota padrão de orders"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema : PedidoSchema, session : Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"msg" : f"Pedido criado com sucesso! Pedido nº {novo_pedido.id}"}