from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)#cria conexão com o db sem sobrecarregar os acessos(IMPORTANTE!)
        session = Session() #Abre uma sessão no db
        yield session
    finally: #independente de erro ou positivo a sessão será fechada
        session.close()


def verificar_token(token : str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        raise HTTPException(status_code=401,detail="Acesso negado. Verifique a validade do Token de acesso.")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido.")
    return usuario