from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    return {"mensagem": "Você acessou a rota de orders"}

