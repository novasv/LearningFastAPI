from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth_home():
    return {"mensagem": "Você acessou a rota de auth"}