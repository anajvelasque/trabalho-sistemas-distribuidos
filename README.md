# Implementação de um Sistema de Transferência de Arquivos FTP

## Descrição
Este projeto tem como objetivo implementar um sistema básico de transferência de arquivos utilizando o protocolo FTP no modelo cliente-servidor. O sistema permite que um cliente se conecte ao servidor para realizar operações de upload e download de arquivos, oferecendo uma interface simples e funcional.

Inicialmente, o sistema utiliza memória compartilhada para o gerenciamento de dados, mas essa abordagem pode ser adaptada conforme as necessidades do projeto.

---

## Funcionalidades

1. **Listar Arquivos**
   - Exibe os arquivos disponíveis no servidor FTP.

2. **Upload de Arquivos**
   - O usuário pode enviar um arquivo, realizando o upload para o servidor FTP.

3. **Download de Arquivos**
   - O usuário pode selecionar um arquivo para realizar o download do servidor FTP.

---

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para implementar o sistema e as interações cliente-servidor.
- **Biblioteca FTP**: Para gerenciar a comunicação entre o cliente e o servidor FTP.

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

## Como Executar o Projeto

1. Clone este repositório para sua máquina local:
   ```bash
   git clone <url-do-repositorio>
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd <nome-do-diretorio>
   ```

3. Inicie o servidor FTP:
   ```bash
   python servidor_ftp.py
   ```

4. Em outro terminal, inicie o cliente FTP:
   ```bash
   python cliente.py
   ```

5. Utilize o cliente para realizar as operações de upload, download e listagem de arquivos.

---

## Licença
Este projeto é de uso acadêmico e não possui uma licença específica. Entre em contato com o autor para outros usos.

