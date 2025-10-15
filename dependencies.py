from sqlalchemy.orm import sessionmaker
from models import db 


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)#cria conexão com o db sem sobrecarregar os acessos(IMPORTANTE!)
        session = Session() #Abre uma sessão no db
        yield session
    finally: #independente de erro ou positivo a sessão será fechada
        session.close()