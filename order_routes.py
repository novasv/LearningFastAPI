from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario, ItemPedido


order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def orders():
    """Esta é a rota padrão de pedidos da API. Todas as rotas dos pedidos precisam de autenticação"""
    return {"mensagem":"Você acessou a rota padrão de orders"}

@order_router.post("/pedido")
async def create_order(pedido_schema : PedidoSchema, session : Session = Depends(pegar_sessao)):
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
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar este tópico.")
    pedido.status = "CANCELADO"
    session.commit()
    return {"msg":f"Pedido nº {pedido.id} Cancelado com Sucesso",
             "pedido" : pedido}

@order_router.get("/list")
async def list_orders( session: Session = Depends(pegar_sessao), usuario:Usuario=Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar este tópico.")
    else:
        pedidos = session.query(Pedido).all()
        return {"pedidos":pedidos}
    

@order_router.post("pedido/adicionar_item/{id_pedido}")
async def add_item_order(id_pedido:int, item_pedido_schema: ItemPedidoSchema, session:Session = Depends(pegar_sessao), usuario: Usuario= Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        return HTTPException(status_code=400, detail="Pedido Inexistente.")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar este tópico.")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido) 
    session.add(item_pedido) 
    pedido.calcular_preco()
    session.commit()
    return {"msg": "Item adicionado ao pedido.",
            "item_id": item_pedido.id,
            "preco_pedido": pedido.preco}
        

