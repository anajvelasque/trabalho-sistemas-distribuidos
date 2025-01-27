from ftplib import FTP

def listar_arquivos_servidor(ftp):
    """Lista arquivos e diretórios no servidor FTP de forma tabulada e recursiva."""
    try:
        # Lista os arquivos e diretórios no diretório atual
        arquivos = ftp.nlst()  
        print("\nArquivos e diretórios disponíveis no servidor:\n")
        
        if not arquivos:
            print("Não há arquivos ou diretórios no servidor.")
        
        for nome_item in arquivos:
            # Verifica se é um diretório
            if verificar_diretorio(ftp, nome_item):
                print(f"[DIR] {nome_item}")
                listar_arquivos_subdiretorio(ftp, nome_item, nivel=1)  # Chama recursivamente para listar o conteúdo do diretório
            else:
                print(f"{nome_item}")
        
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

def verificar_diretorio(ftp, nome_item):
    """Verifica se o item é um diretório acessível."""
    try:
        ftp.cwd(nome_item)  # Tenta acessar como diretório
        ftp.cwd('..')  # Volta ao diretório anterior
        return True  # Se não der erro, é um diretório
    except Exception:
        return False  # Se ocorrer erro, não é um diretório

def listar_arquivos_subdiretorio(ftp, caminho_diretorio, nivel):
    """Lista os arquivos e diretórios dentro de um subdiretório de forma recursiva e tabulada."""
    try:
        # Acessa o subdiretório
        ftp.cwd(caminho_diretorio)
        arquivos_subdiretorio = ftp.nlst()  # Lista arquivos e diretórios no subdiretório
        
        if not arquivos_subdiretorio:
            print(f"{'    ' * nivel}Não há arquivos ou subdiretórios em '{caminho_diretorio}'.")

        # Indenta os arquivos e diretórios para mostrar a hierarquia
        for nome_item in arquivos_subdiretorio:
            # Verifica se é um diretório
            if verificar_diretorio(ftp, nome_item):
                print(f"{'    ' * nivel}[DIR] {nome_item}")  # Indenta os diretórios
                listar_arquivos_subdiretorio(ftp, nome_item, nivel + 1)  # Chama recursivamente para listar o conteúdo
            else:
                print(f"{'    ' * nivel}{nome_item}")  # Indenta os arquivos
        
        ftp.cwd('..')  # Volta ao diretório anterior após a listagem do subdiretório

    except Exception as e:
        print(f"Erro ao acessar o diretório {caminho_diretorio}: {e}")
        ftp.cwd('..')  # Certifica-se de voltar ao diretório anterior após erro
