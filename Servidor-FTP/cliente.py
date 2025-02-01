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

    # Verificar se é um arquivo ou diretório
    if os.path.isfile(caminho_arquivo):
        # Se for um arquivo, realiza o upload do arquivo
        upload_arquivo(ftp, caminho_arquivo)
    elif os.path.isdir(caminho_arquivo):
        # Se for um diretório, realiza o upload de todos os arquivos dentro do diretório
        upload_diretorio(ftp, caminho_arquivo)
    else:
        print(f"Erro: O caminho fornecido não é válido ou não existe. Verifique o caminho e tente novamente.")

def upload_arquivo(ftp, caminho_arquivo):
    """Realiza o upload de um arquivo para o servidor FTP."""
    try:
        # Listar os diretórios disponíveis no servidor
        diretorios = ftp.nlst()
        diretorios = [d for d in diretorios if verificar_diretorio(ftp, d)]

        if not diretorios:
            print("Não há diretórios disponíveis no servidor.")
            criar_diretorio = input("\nDeseja criar um novo diretório no servidor? (s/n): ").strip().lower()
            if criar_diretorio == "s":
                caminho_destino = criar_diretorio_no_servidor(ftp, '/')
            else:
                print("O upload não pode ser feito sem um diretório disponível. Tente novamente mais tarde.")
                return
        else:
            print("Diretórios disponíveis no servidor:")
            for i, dir_nome in enumerate(diretorios, 1):
                print(f"{i} - {dir_nome}")
            escolha = input("\nEscolha o diretório onde deseja salvar o arquivo (digite o número ou pressione Enter para escolher o diretório atual): ").strip()
            if escolha:
                try:
                    escolha = int(escolha) - 1
                    caminho_destino = diretorios[escolha]
                except (ValueError, IndexError):
                    print("Opção inválida. O upload será feito no diretório raiz.")
                    caminho_destino = '/'
            else:
                caminho_destino = '/'

        # Perguntar se o usuário deseja criar um diretório antes de enviar o arquivo
        criar_diretorio = input("\nDeseja criar um novo diretório no servidor? (s/n): ").strip().lower()
        if criar_diretorio == "s":
            caminho_destino = criar_diretorio_no_servidor(ftp, caminho_destino)

        # Realizar o upload do arquivo
        nome_arquivo = os.path.basename(caminho_arquivo)
        print(f"Tentando fazer upload do arquivo: {caminho_arquivo}")
        
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                tamanho_total = os.path.getsize(caminho_arquivo)
                with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=nome_arquivo) as barra:
                    ftp.storbinary(f'STOR {caminho_destino}/{nome_arquivo}', arquivo, callback=lambda data: barra.update(len(data)))
            print(f"Arquivo '{nome_arquivo}' enviado com sucesso para o servidor FTP.")
        except Exception as e:
            print(f"Erro ao enviar o arquivo: {e}")
    except Exception as e:
        print(f"Erro ao acessar diretórios no servidor FTP: {e}")

def upload_diretorio(ftp, caminho_diretorio):
    """Realiza o upload de todos os arquivos dentro de um diretório para o servidor FTP."""
    try:
        # Listar os diretórios disponíveis no servidor
        diretorios = ftp.nlst()
        diretorios = [d for d in diretorios if verificar_diretorio(ftp, d)]

        if not diretorios:
            print("Não há diretórios disponíveis no servidor.")
            criar_diretorio = input("\nDeseja criar um novo diretório no servidor? (s/n): ").strip().lower()
            if criar_diretorio == "s":
                caminho_destino = criar_diretorio_no_servidor(ftp, '/')
            else:
                print("O upload não pode ser feito sem um diretório disponível. Tente novamente mais tarde.")
                return
        else:
            print("Diretórios disponíveis no servidor:")
            for i, dir_nome in enumerate(diretorios, 1):
                print(f"{i} - {dir_nome}")
            escolha = input("\nEscolha o diretório onde deseja salvar os arquivos (digite o número ou pressione Enter para escolher o diretório atual): ").strip()
            if escolha:
                try:
                    escolha = int(escolha) - 1
                    caminho_destino = diretorios[escolha]
                except (ValueError, IndexError):
                    print("Opção inválida. O upload será feito no diretório raiz.")
                    caminho_destino = '/'
            else:
                caminho_destino = '/'

        # Perguntar se o usuário deseja criar um diretório antes de enviar os arquivos
        criar_diretorio = input("\nDeseja criar um novo diretório no servidor? (s/n): ").strip().lower()
        if criar_diretorio == "s":
            caminho_destino = criar_diretorio_no_servidor(ftp, caminho_destino)

        # Enviar todos os arquivos do diretório
        for root, dirs, files in os.walk(caminho_diretorio):
            for arquivo in files:
                caminho_completo = os.path.join(root, arquivo)
                print(f"Enviando arquivo: {caminho_completo}")
                nome_arquivo = os.path.basename(caminho_completo)
                with open(caminho_completo, 'rb') as file:
                    tamanho_total = os.path.getsize(caminho_completo)
                    with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=nome_arquivo) as barra:
                        ftp.storbinary(f'STOR {caminho_destino}/{nome_arquivo}', file, callback=lambda data: barra.update(len(data)))

        print(f"Todos os arquivos no diretório '{caminho_diretorio}' foram enviados com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar o diretório: {e}")

def criar_diretorio_no_servidor(ftp, caminho_destino):
    """Cria um diretório no servidor FTP dentro de um diretório existente."""
    nome_diretorio = input("\nDigite o nome do diretório que deseja criar: ").strip()
    try:
        caminho_completo = f"{caminho_destino}/{nome_diretorio}".replace(os.sep, '/')
        ftp.mkd(caminho_completo)
        print(f"Diretório '{nome_diretorio}' criado com sucesso.")
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

def listar_arquivos_ftp(ftp):
    """Lista arquivos e diretórios no servidor FTP, mostrando se é arquivo ou diretório."""
    try:
        arquivos = ftp.nlst()
        arquivos_diretorios = []
        
        # Verificar se os itens são arquivos ou diretórios
        for item in arquivos:
            if verificar_diretorio(ftp, item):
                arquivos_diretorios.append((item, 'diretório'))
            else:
                arquivos_diretorios.append((item, 'arquivo'))
        
        return arquivos_diretorios
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return []

def fazer_download(ftp):
    """Realiza o download de um arquivo ou diretório do servidor FTP para o computador local."""
    try:
        # Listar os arquivos e diretórios no servidor
        arquivos = listar_arquivos_ftp(ftp)
        if not arquivos:
            print("Não há arquivos disponíveis no servidor para download.")
            return

        # Mostrar arquivos e diretórios
        print("Arquivos disponíveis no servidor:")
        for i, arquivo in enumerate(arquivos, 1):
            print(f"{i} - {arquivo}")
        
        # O usuário escolhe o arquivo ou diretório a ser baixado
        escolha = input("\nEscolha o arquivo ou diretório que deseja baixar (digite o número ou pressione Enter para baixar o primeiro item): ").strip()
        
        if escolha:
            try:
                escolha = int(escolha) - 1
                item_escolhido = arquivos[escolha]
            except (ValueError, IndexError):
                print("Opção inválida. O download será realizado do primeiro arquivo da lista.")
                item_escolhido = arquivos[0]
        else:
            item_escolhido = arquivos[0]

        # Verificar se o item é um diretório
        print(f"Você escolheu: {item_escolhido}")

        # Mudar para modo binário
        ftp.voidcmd('TYPE I')

        # Verificar se o item é um diretório
        if verificar_diretorio(ftp, item_escolhido):
            print(f"Iniciando o download de todos os arquivos do diretório: {item_escolhido}")
            caminho_local = input("Digite o caminho local onde deseja salvar o diretório (por exemplo, C:/Users/faela/Desktop ou deixe em branco para o diretório atual): ").strip()
            if not caminho_local:
                caminho_local = os.getcwd()

            # Substituir barras invertidas por barras normais no Windows
            caminho_local = caminho_local.replace("\\", "/")

            # Verificar se o diretório existe, se não, criá-lo
            if not os.path.exists(caminho_local):
                print(f"Criando diretório: {caminho_local}")
                os.makedirs(caminho_local)  # Cria o diretório se não existir
            else:
                print(f"Usando diretório existente: {caminho_local}")

            # Listar arquivos dentro do diretório escolhido e realizar o download de cada um
            ftp.cwd(item_escolhido)  # Entrar no diretório remoto
            arquivos_no_diretorio = listar_arquivos_ftp(ftp)  # Listar arquivos dentro do diretório
            if arquivos_no_diretorio:
                for arquivo in arquivos_no_diretorio:
                    caminho_arquivo_local = os.path.join(caminho_local, arquivo)
                    with open(caminho_arquivo_local, 'wb') as arquivo_local:
                        tamanho_total = ftp.size(arquivo)
                        with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=arquivo) as barra:
                            ftp.retrbinary(f"RETR {arquivo}", arquivo_local.write, 1024, callback=lambda data: barra.update(len(data)))
                print(f"Todos os arquivos do diretório '{item_escolhido}' foram baixados com sucesso para: {caminho_local}")
            else:
                print(f"O diretório '{item_escolhido}' está vazio.")

            ftp.cwd('..')  # Voltar para o diretório anterior após o download

        else:
            # Se não for diretório, baixar arquivo único
            caminho_destino = input(f"Digite o caminho local onde deseja salvar o arquivo '{item_escolhido}' (deixe em branco para o diretório atual): ").strip()
            if not caminho_destino:
                caminho_destino = os.path.join(os.getcwd(), item_escolhido)

            # Substituir barras invertidas por barras normais no Windows
            #caminho_destino = caminho_destino.replace("\\", "/")

            # Criar diretório se não existir
            diretorio_destino = os.path.dirname(caminho_destino)
            if not os.path.exists(diretorio_destino):
                print(f"Criando diretório: {diretorio_destino}")
                os.makedirs(diretorio_destino)

            try:
                with open(caminho_destino, 'wb') as arquivo_local:
                    tamanho_total = ftp.size(item_escolhido)
                    with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=item_escolhido) as barra:
                        ftp.retrbinary(f"RETR {item_escolhido}", arquivo_local.write, 1024, callback=lambda data: barra.update(len(data)))
                print(f"Arquivo '{item_escolhido}' baixado com sucesso para: {caminho_destino}")
            except PermissionError:
                print(f"Erro: Permissão negada para salvar o arquivo em '{caminho_destino}'. Tente escolher um diretório diferente.")
                novo_caminho_destino = input("Digite um novo caminho local onde deseja salvar o arquivo: ").strip()
                if novo_caminho_destino:
                    caminho_destino = novo_caminho_destino
                    with open(caminho_destino, 'wb') as arquivo_local:
                        tamanho_total = ftp.size(item_escolhido)
                        with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=item_escolhido) as barra:
                            ftp.retrbinary(f"RETR {item_escolhido}", arquivo_local.write, 1024, callback=lambda data: barra.update(len(data)))
                    print(f"Arquivo '{item_escolhido}' baixado com sucesso para: {caminho_destino}")
                else:
                    print("Download cancelado.")

    except Exception as e:
        print(f"Erro ao tentar baixar o arquivo ou diretório: {e}")

def download_diretorio(ftp, diretorio):
    """Baixa todos os arquivos de um diretório do servidor FTP."""
    try:
        # Listar todos os arquivos dentro do diretório
        arquivos = ftp.nlst(diretorio)
        if not arquivos:
            print(f"O diretório '{diretorio}' está vazio ou não contém arquivos.")
            return

        print(f"Iniciando o download de todos os arquivos do diretório: {diretorio}")
        
        # Fazer o download de cada arquivo do diretório
        for arquivo in arquivos:
            caminho_destino = input(f"Digite o caminho local onde deseja salvar o arquivo '{arquivo}' (deixe em branco para o diretório atual): ").strip()
            if not caminho_destino:
                caminho_destino = os.path.join(os.getcwd(), arquivo)
            
            # Garantir que o diretório local existe
            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

            # Fazer o download do arquivo
            with open(caminho_destino, 'wb') as arquivo_local:
                tamanho_total = ftp.size(arquivo)
                with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc=arquivo) as barra:
                    ftp.retrbinary(f"RETR {arquivo}", arquivo_local.write, 1024, callback=lambda data: barra.update(len(data)))
        
        print(f"Todos os arquivos do diretório '{diretorio}' foram baixados com sucesso.")
    
    except Exception as e:
        print(f"Erro ao tentar baixar o diretório: {e}")

def verificar_diretorio(ftp, nome_item):
    """Verifica se o item é um diretório acessível no servidor FTP."""
    try:
        ftp.cwd(nome_item)  # Tenta acessar como diretório
        ftp.cwd('..')  # Volta ao diretório anterior
        return True  # Se não der erro, é um diretório
    except Exception:
        return False  # Se ocorrer erro, não é um diretório

def menu_principal(ip_servidor, usuario_ftp, senha_ftp):
    """Função principal que gerencia o menu e as opções do FTP."""
    ftp = conectar_ftp(ip_servidor, usuario_ftp, senha_ftp)
    
    while True:
        print("\n=== Menu FTP ===")
        print("1 - Listar arquivos no servidor")
        print("2 - FAZER UPLOAD DE ARQUIVO OU DIRETÓRIO")
        print("3 - FAZER DOWNLOAD DE ARQUIVO")
        print("4 - Encerrar conexão e sair")
        
        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            listar_arquivos_servidor(ftp)
        elif escolha == "2":
            fazer_upload(ftp)
        elif escolha == "3":
            fazer_download(ftp)
        elif escolha == "4":
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
