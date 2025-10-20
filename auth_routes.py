from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub" : str(id_usuario), "exp" : data_expiracao}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) 
    return encoded_jwt

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first() #Filtra email do usuario(input)
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    
    return usuario



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
    

@auth_router.post("/login")
async def login(login_schema : LoginSchema, session : Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        #email não encontrado
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais invalidas.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token" : access_token, "token_type" : "Bearer",
            "refresh_token" : refresh_token,
            } 

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session : Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        #email não encontrado
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais invalidas.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token" : access_token, "token_type" : "Bearer",
            } 


@auth_router.get("/refresh")
async def use_refresh_token(usuario : Usuario = Depends(verificar_token), ):
    #vericicar token
    access_token = criar_token(usuario.id)
    return {
            "access_token" : access_token,
            "token_type" : "Bearer",
            } 

