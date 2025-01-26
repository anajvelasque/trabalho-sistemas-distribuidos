from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def iniciar_servidor_ftp():
    # Configuração do servidor FTP
    authorizer = DummyAuthorizer()
    
    # Adiciona um usuário com permissões de leitura, escrita e listagem
    authorizer.add_user('usuario', 'senha123', 'C:/Users/anajv/Documents/trabalho-sistemas-distribuidos/Servidor-FTP/FTP-Compartilhamento', perm='elradfmw')
    
    # Configura o manipulador de requisições FTP
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Define o IP e a porta do servidor FTP
    endereco_servidor = ('0.0.0.0', 21)  # Ou use '127.0.0.1' para localhost
    servidor = FTPServer(endereco_servidor, handler)
    
    print("Servidor FTP está em execução...")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor_ftp()