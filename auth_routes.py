from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """Esta é a rota padrão de autenticação da API"""
    return {"mensagem":"Você acessou a rota padrão de autenticação", "autenticado" : False}
