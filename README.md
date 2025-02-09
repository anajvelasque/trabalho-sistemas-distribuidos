# Implementação de um Sistema de Transferência de Arquivos FTP

## Descrição
Este projeto tem como objetivo implementar um sistema distribuído baseado em coordenação básico de transferência de arquivos, utilizando o protocolo FTP no modelo cliente-servidor. O sistema permite que um cliente se conecte ao servidor para realizar operações de upload, listagem, download e remoção de arquivos através do Discord, oferecendo uma abordagem simples e funcional.

Inicialmente, o sistema utiliza o Hamachi para criar uma rede virtual privada, um servidor FTP, um bot do Discord e a ferramenta HaProxy que é utilizada para balanceamento de carga.

---

## Funcionalidades

1. **Listar Arquivos**
   - Exibe os arquivos disponíveis no servidor FTP.

2. **Upload de Arquivos**
   - O usuário pode enviar um arquivo, realizando o upload para o servidor FTP.

3. **Download de Arquivos**
   - O usuário pode selecionar um arquivo para realizar o download do servidor FTP.
     
4. **Apagar Arquivos**
   - O usuário pode selecionar um arquivo para realizar a remoção do servidor FTP.

---

## Tecnologias Utilizadas

 - **Python**: Linguagem principal para desenvolvimento do sistema.
 - **ftplib**: Biblioteca padrão do Python usada para conexão e manipulação de servidores FTP.
 - **os**: Biblioteca padrão do Python usada para manipulação de arquivos e diretórios.
 - **discord.py**: Biblioteca utilizada para criar o bot do Discord que interage com os servidores FTP.
 - **pyftpdlib**: Biblioteca usada para criar e gerenciar servidores FTP locais.
 - **Sistema de Balanceamento de Carga**: Implementado no código para distribuir uploads entre servidores FTP disponíveis, escolhendo o menos carregado.
 - **Gerenciamento de Conexões FTP**: Código implementa reconexão automática e listagem de arquivos de múltiplos servidores.
 - **Automação com Bot do Discord**: Comandos como !upload, !download, !listar e !apagar permitem interação direta pelo Discord.

---

## Desenvolvedores

- Ana Julia Velasque Rodrigues
- Rafael Augusto de Souza 
- Yasmim Augusta Gomes Teixeira

---

## Estrutura do Projeto

- `cliente.py`: Implementação do cliente FTP, responsável por interagir com o servidor.
- `servidor_ftp.py`: Implementação do servidor FTP, que gerencia as operações de upload, download e listagem de arquivos.
- `README.md`: Este documento, que descreve o projeto.

---


## Requisitos 

**Antes de iniciar, certifique-se de ter os seguintes componentes:** 

 - Hamachi (para criar uma rede privada virtual entre as máquinas) 

 - HaProxy (para balanceamento de carga, necessário Linux ou WSL no Windows) 

 - Python 3.8 ou superior
   
 - Conta no Discord e acesso a ao servidor do Discord

## Configuração da Rede com Hamachi 

1. Baixar e instalar o Hamachi em todas as máquinas pelo site: https://vpn.net/ . 

2. Criar uma rede:  
    a. Um dos computadores deve criar uma rede no Hamachi, definindo um ID e senha. 

3. Entrar na rede:  
    b. As demais máquinas devem ingressar na rede utilizando o mesmo ID e senha. 

4. Verifique a conexão entre as máquinas após a entrada na rede. 

5. O Hamachi irá gerar um IP para cada máquina da rede, eles serão importantes pois eles serão utilizados para conectar com o servidor FTP.

## Instalação e Configuração do HaProxy 

- No computador responsável pelo balanceamento: 

1. Se estiver no Windows, instale o WSL: 

```
wsl --install 
```  

 - Reinicie o computador e instale o Ubuntu pela Microsoft Store. 

2. Instalar o HaProxy no Linux (Ubuntu via WSL ou nativo): 
```
sudo apt update 
sudo apt install haproxy 
```

3. Editar a configuração do HaProxy: 

    a. Abra o arquivo de configuração localizado em /etc/haproxy/haproxy.cfg e substitua ele por: 
```
global 
    log /dev/log local0 
    log /dev/log local1 notice 
    chroot /var/lib/haproxy 
    stats socket /run/haproxy/admin.sock mode 660 level admin 
    stats timeout 30s 
    user haproxy 
    group haproxy 
    daemon 
 
defaults 
    log global 
    mode tcp  # Usar o modo TCP para o FTP 
    option dontlognull 
    timeout connect 5000ms 
    timeout client 50000ms 
    timeout server 50000ms 
 
frontend ftp_front 
    bind *:21 
    mode tcp  # Usar o modo TCP para o FTP 
    default_backend ftp_back 
 
backend ftp_back 
    balance roundrobin 
    option tcp-check  # Verificação de conectividade TCP 
    stick-table type ip size 200k expire 30m 
    stick on src  # Mantém a persistência por IP do cliente 
    server ftp1 25.58.38.220:21 check inter 5s fall 3 rise 2 
    server ftp2 25.23.12.169:21 check inter 5s fall 3 rise 2 
  
```
   b. Importante: substitua os IPs pelos IPs das máquinas conectadas à rede, mas mantenha a porta 21. 
   
 4. Iniciar o HaProxy e verificar o status: 
```
sudo systemctl start haproxy  
sudo service haproxy status 
```  

Aqui pode-se perceber que primeiro ele inicialmente não conseguiu conectar (DOWN) mas após um tempo ele consegue (UP) significando que ele conseguiu conectar nas duas redes do Hamachi. 

## Como Executar o Projeto

1. Clone este repositório para sua máquina local:
   ```bash
   git clone <url-do-repositorio>
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd <nome-do-diretorio>
   ```
3. Instale essas bibliotecas se necessário:
   ```bash
   pip install discord.py pyftpdlib
   ou
   python3 -m pip install discord.py pyftpdlib
   ```
4. Inicie o servidor FTP:
   ```bash
   python servidor_ftp.py
   ```

5. Em outro terminal, inicie o cliente FTP:
   ```bash
   python cliente.py
   ```

## Configuração do Cliente 

No computador com HaProxy, edite cliente.py e configure os IPs dos servidores trocando as linhas abaixo pelos IPs correspondentes aos das máquinas que irão participar da rede e com respectivos usuário e senha desejados: 

```
servidores_ftp = [ 
    {"ip": "25.58.38.220", "usuario": "usuario1", "senha": "senha1"}, 
    {"ip": "25.23.12.169", "usuario": "usuario2", "senha": "senha2"}, 
] 
```

## Configuração do Servidor FTP 

Cada máquina que atuará como servidor FTP deve seguir os passos: 

1. Editar o código do servidor FTP (servidor_ftp.py): 

    a. Altere o diretório onde os arquivos serão armazenados: caminho_diretorio = r'C:\\Users\\SEU_USUARIO\\Downloads\\ftp_sd'

    b. Atualize as credenciais e o IP do servidor para o IP respectivo de cada máquina que vai executar o código:  
````
authorizer.add_user('usuario1', 'senha1', caminho_diretorio, perm='elradfmwMT') 
````

   c. Atualize o IP do servidor em cada máquina também no trecho: 
   
````
   # Define o IP e a porta do servidor FTP 

    endereco_servidor = ('25.58.38.220', 21)   

    servidor = FTPServer(endereco_servidor, handler) 
````
 
  - Observação: A porta 21 foi utilizada para o HaProxy 

  - Código do servidor com as linhas que precisam ser modificadas em negrito: 
````
import os from pyftpdlib.authorizers import DummyAuthorizer from pyftpdlib.handlers import FTPHandler from pyftpdlib.servers import FTPServer 

def iniciar_servidor_ftp(): # Configuração do servidor FTP authorizer = DummyAuthorizer() 

# Adiciona um usuário com permissões de leitura, escrita e listagem 
#caminho_diretorio = r'C:\Users\faela\Downloads\ftp sd' 
caminho_diretorio = r'C:\Users\anajv\Downloads\ftp_sd' 
 
if not os.path.exists(caminho_diretorio): 
    os.makedirs(caminho_diretorio) 
 
authorizer.add_user('usuario1', 'senha1', caminho_diretorio, perm='elradfmwMT') 
 
# Configura o manipulador de requisições FTP 
handler = FTPHandler 
handler.authorizer = authorizer 
 
# Define o IP e a porta do servidor FTP 
endereco_servidor = ('25.58.38.220', 21)   
servidor = FTPServer(endereco_servidor, handler) 
 
print("Servidor FTP está em execução...") 
servidor.serve_forever() 
  

if name == "main": iniciar_servidor_ftp() 

```` 

## Execução do Projeto 

1. Iniciar o HaProxy (se ainda não estiver rodando): 
````
sudo systemctl start haproxy 
````
2. Rodar os servidores FTP nas máquinas responsáveis, cada um em um terminal separado: 

   a. No terminal, execute o comando: 

python servidor_ftp.py 

   b. Se a execução for bem-sucedida, uma mensagem de confirmação de conexão será exibida. 

3. Executar o Bot do Discord somente na máquina que está executando o HaProxy 

   a. Em outro terminal, execute: 
````
python cliente.py 
````
   b. Após a mensagem de conexão bem-sucedida, o bot estará online. 

4. Acessar o Servidor Discord e Utilizar os Comandos 

   a. Entre no servidor do Discord através do seguinte link: https://discord.gg/yrDtdGTn 

5. Utilize os seguintes comandos no chat para interagir com o servidor FTP: 

  - a. `!menu` - Exibe o menu de comandos disponíveis. 

  - b. `!listar` - Lista os arquivos armazenados no servidor FTP. 

  - c. `!upload` - Envie um arquivo anexado para armazená-lo no servidor FTP. 

  - d. `!download <nome_arquivo>` - Baixa um arquivo específico do servidor FTP. 

  - e. `!apagar <nome_arquivo>` - Remove um arquivo do servidor FTP. 

  - f. `!desconectar` - Finaliza a conexão do bot com o servidor FTP. 

---

## Licença
Este projeto é de uso acadêmico e não possui uma licença específica. Entre em contato com o autor para outros usos.

