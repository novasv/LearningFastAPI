from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """Esta é a rota padrão de autenticação da API"""
    return {"mensagem":"Você acessou a rota padrão de autenticação", "autenticado" : False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema : UsuarioSchema, session : Session = Depends(pegar_sessao)): #informar o formato dos dados que entrarão na função
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()  #Filtra emails repetidos
    if usuario:
        #já existe usuário com esse email
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"msg" : f" {usuario_schema.nome} cadastrado com sucesso."}
