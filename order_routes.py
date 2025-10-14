from fastapi import APIRouter


order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def orders():
    """Esta é a rota padrão de pedidos da API. Todas as rotas dos pedidos precisam de autenticação"""
    return {"mensagem":"Você acessou a rota padrão de orders"}