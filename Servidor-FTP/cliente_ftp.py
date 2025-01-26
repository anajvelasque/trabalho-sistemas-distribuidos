from ftplib import FTP
import os
import sys

# Conecta ao servidor FTP
ip_servidor = "127.0.0.1" # Endereço IP local *ALTERAR PARA O IP DO SERVIDOR*
usuario_ftp = "usuario"
senha_ftp = "senha123"

ftp = FTP(ip_servidor)
ftp.login(user=usuario_ftp, passwd=senha_ftp)

# Função para listar arquivos no servidor FTP
def listar_arquivos_servidor():
    try:
        arquivos = ftp.nlst()
        print("\nArquivos disponíveis no servidor:\n")
        for idx, nome_arquivo in enumerate(arquivos):
            print(f"{idx + 1} - {nome_arquivo}")
        return arquivos
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return []

# Função principal do cliente FTP
def cliente_ftp():
    continuar = True
    while continuar:
        print("\n=== Menu FTP ===")
        print("1 - Listar arquivos no servidor")
        print("2 - Encerrar conexão")
        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            listar_arquivos_servidor()
        elif escolha == "2":
            ftp.quit()
            print("Conexão com o servidor FTP foi encerrada.")
            continuar = False
            sys.exit()
        else:
            print("Opção inválida. Por favor, tente novamente.")
        input("\nPressione Enter para retornar ao menu...")

if __name__ == "__main__":
    cliente_ftp()