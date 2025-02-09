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
- 
- `README.md`: Este documento, que descreve o projeto.

---

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

6. Utilize o cliente para realizar as operações de upload, download e listagem de arquivos.

---

## Licença
Este projeto é de uso acadêmico e não possui uma licença específica. Entre em contato com o autor para outros usos.

