import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def iniciar_servidor_ftp():
    # Configuração do servidor FTP
    authorizer = DummyAuthorizer()
    
    # Adiciona um usuário com permissões de leitura, escrita e listagem
    caminho_diretorio = r'C:\Users\faela\Downloads\ftp sd'
    #caminho_diretorio = r'C:\Users\anajv\Downloads\ftp_sd'

    if not os.path.exists(caminho_diretorio):
        os.makedirs(caminho_diretorio)
    
    authorizer.add_user('usuario', 'senha123', caminho_diretorio, perm='elradfmwMT')
    
    # Configura o manipulador de requisições FTP
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Define o IP e a porta do servidor FTP
    endereco_servidor = ('127.0.0.1', 21)  # Endereço IP local
    servidor = FTPServer(endereco_servidor, handler)
    
    print("Servidor FTP está em execução...")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor_ftp()