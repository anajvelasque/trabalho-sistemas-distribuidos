from ftplib import FTP
import os
from tqdm import tqdm

from listar_arquivos_ftp import listar_arquivos_servidor

def conectar_ftp(ip_servidor, usuario_ftp, senha_ftp):
    """Estabelece uma conexão com o servidor FTP."""
    try:
        ftp = FTP(ip_servidor)
        ftp.login(user=usuario_ftp, passwd=senha_ftp)
        print("Conexão com o servidor FTP estabelecida com sucesso.")
        return ftp
    except Exception as e:
        print(f"Erro ao conectar ao servidor FTP: {e}")
        return None

def fazer_upload(ftp):
    """Realiza o upload de um arquivo ou diretório para o servidor FTP."""
    caminho_arquivo = input("\nDigite o caminho completo do arquivo ou diretório que deseja enviar: ").strip().strip('"')

    if not os.path.exists(caminho_arquivo):
        print("Arquivo ou diretório não encontrado. Verifique o caminho e tente novamente.")
        return

    # Pergunta onde deseja salvar o arquivo ou diretório no servidor FTP
    caminho_destino = escolher_destino(ftp, caminho_arquivo)

    if os.path.isdir(caminho_arquivo):
        # Se for um diretório, faz o upload de todos os arquivos dentro dele
        upload_diretorio(ftp, caminho_arquivo, caminho_destino)
    elif os.path.isfile(caminho_arquivo):
        # Se for um arquivo, faz o upload normalmente
        nome_arquivo = os.path.basename(caminho_arquivo)
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                tamanho_total = os.path.getsize(caminho_arquivo)
                with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=nome_arquivo) as barra:
                    ftp.storbinary(f'STOR {caminho_destino}/{nome_arquivo}', arquivo, callback=lambda data: barra.update(len(data)))
            print(f"Arquivo '{nome_arquivo}' enviado com sucesso para o servidor FTP.")
        except Exception as e:
            print(f"Erro ao enviar o arquivo: {e}")

def upload_diretorio(ftp, caminho_diretorio, caminho_destino):
    """Realiza o upload de todos os arquivos de um diretório e cria os diretórios no servidor FTP."""
    for raiz, dirs, arquivos in os.walk(caminho_diretorio):
        # Criar diretórios no servidor FTP
        for dir_nome in dirs:
            caminho_ftp = os.path.join(caminho_destino, os.path.relpath(os.path.join(raiz, dir_nome), caminho_diretorio)).replace(os.sep, '/')
            try:
                ftp.mkd(caminho_ftp)
                print(f"Diretório '{caminho_ftp}' criado no servidor.")
            except Exception:
                # Se o diretório já existir, o erro será ignorado
                pass

        # Fazer o upload dos arquivos
        for nome_arquivo in arquivos:
            caminho_arquivo_local = os.path.join(raiz, nome_arquivo)
            caminho_ftp_arquivo = os.path.join(caminho_destino, os.path.relpath(os.path.join(raiz, nome_arquivo), caminho_diretorio)).replace(os.sep, '/')

            try:
                with open(caminho_arquivo_local, 'rb') as arquivo:
                    tamanho_total = os.path.getsize(caminho_arquivo_local)
                    with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=caminho_ftp_arquivo) as barra:
                        ftp.storbinary(f'STOR {caminho_ftp_arquivo}', arquivo, callback=lambda data: barra.update(len(data)))
                print(f"Arquivo '{caminho_ftp_arquivo}' enviado com sucesso para o servidor FTP.")
            except Exception as e:
                print(f"Erro ao enviar o arquivo '{nome_arquivo}': {e}")

def escolher_destino(ftp, caminho_arquivo):
    """Permite ao usuário escolher um diretório no servidor FTP onde deseja salvar o arquivo ou diretório."""
    try:
        diretorios = ftp.nlst()
        diretorios = [d for d in diretorios if verificar_diretorio(ftp, d)]
        
        if not diretorios:
            print("Não há diretórios disponíveis no servidor.")
            return ""

        print("Escolha o diretório onde deseja salvar o arquivo:")

        # Iniciar navegação no diretório raiz
        caminho_destino = navegar_diretorios(ftp, '/')

        return caminho_destino

    except Exception as e:
        print(f"Erro ao acessar diretórios: {e}")
        return ""

def navegar_diretorios(ftp, caminho_atual):
    """Permite ao usuário navegar entre diretórios e subdiretórios para escolher o destino de upload."""
    while True:
        print(f"\nDiretórios em '{caminho_atual}':")
        try:
            # Muda para o diretório atual
            ftp.cwd(caminho_atual)
            conteudo = ftp.nlst()
            subdiretorios = [item for item in conteudo if verificar_diretorio(ftp, item)]
            
            # Exibir subdiretórios
            for subdir in subdiretorios:
                print(f"  [DIR] {subdir}")
            
            # Exibir a opção para criar diretório
            print(f"\nEscolha um diretório ou subdiretório para salvar:")
            print("[Enter] - Escolher este diretório")
            
            # Pedir para o usuário digitar o nome do diretório ou opção desejada
            escolha = input("\nDigite o nome do diretório ou opção desejada: ").strip()
            
            if escolha:
                if escolha in subdiretorios:
                    # Se o nome do diretório escolhido estiver na lista de subdiretórios
                    caminho_atual = f"{caminho_atual}/{escolha}" if caminho_atual != '/' else f"/{escolha}"
                else:
                    print("Diretório não encontrado. Tente novamente.")
            else:
                
                print(f"Você escolheu o diretório '{caminho_atual}'")
                
                # Perguntar se deseja criar um novo diretório
                criar_diretorio = input("\nDeseja criar um novo diretório neste local? (s/n): ").strip().lower()
                
                if criar_diretorio == "s":
                    caminho_atual = criar_diretorio_no_servidor(ftp, caminho_atual)
                    print(f"Diretório '{caminho_atual}' criado com sucesso.")
                
                # Confirmar se deseja salvar o arquivo no diretório selecionado
                confirmacao = input(f"\nDeseja salvar o arquivo neste diretório: '{caminho_atual}'? (s/n): ").strip().lower()
                
                if confirmacao == "s":
                    return caminho_atual  
                else:
                    print("Por favor, escolha um diretório novamente.")
                    continue
        except Exception as e:
            print(f"Erro ao acessar diretório: {e}")
            return caminho_atual

def verificar_diretorio(ftp, nome_item):
    """Verifica se o item é um diretório acessível."""
    try:
        ftp.cwd(nome_item)  # Tenta acessar como diretório
        ftp.cwd('..')  # Volta ao diretório anterior
        return True  # Se não der erro, é um diretório
    except Exception:
        return False  # Se ocorrer erro, não é um diretório

def criar_diretorio_no_servidor(ftp, caminho_destino):
    """Cria um diretório no servidor FTP dentro de um diretório existente."""
    nome_diretorio = input("\nDigite o nome do diretório que deseja criar: ").strip()
    try:
        caminho_completo = f"{caminho_destino}/{nome_diretorio}".replace(os.sep, '/')
        ftp.mkd(caminho_completo)
        return caminho_completo
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")
        return caminho_destino

def desconectar_ftp(ftp):
    """Finaliza a conexão com o servidor FTP."""
    if ftp:
        ftp.quit()
        print("Conexão com o servidor FTP encerrada.")

def reconectar_ftp(ip_servidor, usuario_ftp, senha_ftp):
    """Reconecta ao servidor FTP."""
    return conectar_ftp(ip_servidor, usuario_ftp, senha_ftp)

def menu_principal(ip_servidor, usuario_ftp, senha_ftp):
    """Função principal que gerencia o menu e as opções do FTP."""
    ftp = conectar_ftp(ip_servidor, usuario_ftp, senha_ftp)
    
    while True:
        print("\n=== Menu FTP ===")
        print("1 - Listar arquivos no servidor")
        print("2 - FAZER UPLOAD DE ARQUIVO")
        print("3 - Encerrar conexão e sair")
        
        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            listar_arquivos_servidor(ftp)
        elif escolha == "2":
            fazer_upload(ftp)
        elif escolha == "3":
            desconectar_ftp(ftp)
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        # Reconectar após cada ação, para garantir que a navegação seja limpa
        ftp = reconectar_ftp(ip_servidor, usuario_ftp, senha_ftp)

if __name__ == "__main__":
    ip_servidor = "127.0.0.1"  # Endereço IP do servidor FTP
    usuario_ftp = "usuario"
    senha_ftp = "senha123"
    
    menu_principal(ip_servidor, usuario_ftp, senha_ftp)
