from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario


order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancel_order(id_pedido : int, session : Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido =session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não pode cancelar este pedido.")
    pedido.status = "CANCELADO"
    session.commit()
    return {"msg":f"Pedido nº {pedido.id} Cancelado com Sucesso",
             "pedido" : pedido}