from ftplib import FTP

def listar_arquivos_servidor(ftp):
    """Lista arquivos e diretórios no servidor FTP de forma tabulada e interativa, com opção de deletar."""
    try:
        arquivos_para_deletar = []  # Lista para armazenar os arquivos e diretórios numerados
        print("\nArquivos e diretórios disponíveis no servidor:\n")
        
        listar_arquivos_completa(ftp, arquivos_para_deletar)

        # Opção de deletar arquivo
        print("\nSelecione 'D' para deletar um arquivo ou diretório.")
        
        # Solicita ao usuário a opção de deletar um arquivo ou diretório
        deletar = input("\nDigite 'D' para deletar ou qualquer outra tecla para sair: ").strip().lower()
        
        if deletar == 'd':
            # Exibe a lista de arquivos e diretórios para deletar
            try:
                escolha = int(input("\nDigite o número correspondente ao item que deseja deletar: "))
                if 1 <= escolha <= len(arquivos_para_deletar):
                    item_escolhido = arquivos_para_deletar[escolha - 1]
                    confirmar = input(f"Você tem certeza que deseja deletar '{item_escolhido}'? (s/n): ").strip().lower()
                    if confirmar == 's':
                        deletar_item(ftp, item_escolhido)
            except ValueError:
                print("Opção inválida. Nenhum item foi deletado.")
        else:
            print("Nenhum item será deletado.")
        
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

def listar_arquivos_completa(ftp, arquivos_para_deletar, caminho_atual="", nivel=0, caminho_parent=""):
    """Função recursiva para listar todos os arquivos e subdiretórios no servidor FTP com numeração contínua e estrutura hierárquica."""
    try:
        arquivos = ftp.nlst(caminho_atual)  # Lista os arquivos e diretórios no caminho atual
        
        if not arquivos:
            return
        
        for i, nome_item in enumerate(arquivos):
            # Monta o caminho completo
            caminho_completo = f"{caminho_atual}/{nome_item}" if caminho_atual else nome_item
            caminho_exibicao = f"{caminho_parent}/{nome_item}" if caminho_parent else nome_item
            
            # Verifica se é um diretório
            if verificar_diretorio(ftp, caminho_completo):
                print(f"{len(arquivos_para_deletar) + 1}. [sub]{caminho_exibicao}")  # Indenta e marca como subdiretório
                arquivos_para_deletar.append(caminho_completo)  # Adiciona o diretório à lista para deletar
                listar_arquivos_completa(ftp, arquivos_para_deletar, caminho_completo, nivel + 1, caminho_exibicao)  # Chama recursivamente para listar o conteúdo
            else:
                print(f"{len(arquivos_para_deletar) + 1}. {caminho_exibicao}")  # Exibe o arquivo
                arquivos_para_deletar.append(caminho_completo)  # Adiciona o arquivo à lista para deletar
        
    except Exception as e:
        print(f"Erro ao acessar o diretório {caminho_atual}: {e}")

def verificar_diretorio(ftp, caminho_item):
    """Verifica se o item é um diretório acessível."""
    try:
        ftp.cwd(caminho_item)  # Tenta acessar como diretório
        ftp.cwd('..')  # Volta ao diretório anterior
        return True  # Se não der erro, é um diretório
    except Exception:
        return False  # Se ocorrer erro, não é um diretório

def deletar_item(ftp, item):
    """Deleta um arquivo ou diretório no servidor FTP."""
    try:
        # Tenta verificar se o diretório está acessível antes de tentar deletá-lo
        if verificar_diretorio(ftp, item):
            # Se for um diretório, deletamos seu conteúdo recursivamente
            deletar_diretorio(ftp, item)
        else:
            ftp.delete(item)  # Deleta o arquivo
            print(f"Arquivo '{item}' deletado com sucesso.")
    except Exception as e:
        # Se ocorrer erro na exclusão, exibe uma mensagem de erro
        print(f"Erro ao deletar '{item}': {e}")

def deletar_diretorio(ftp, diretório):
    """Deleta um diretório no FTP e seu conteúdo de forma recursiva, com verificação adequada."""
    try:
        # Verifica se o diretório existe e está acessível
        ftp.cwd(diretório)
        arquivos = ftp.nlst()  # Lista os arquivos e subdiretórios no diretório
        
        if arquivos:
            # Se o diretório não estiver vazio, deleta seus arquivos e subdiretórios
            for arquivo in arquivos:
                caminho_item = f"{diretório}/{arquivo}"
                if verificar_diretorio(ftp, caminho_item):  # Se for diretório, chama recursão
                    deletar_diretorio(ftp, caminho_item)
                else:
                    ftp.delete(caminho_item)  # Deleta o arquivo
        
        # Agora o diretório está vazio, então podemos tentar deletá-lo
        ftp.cwd('..')  # Volta ao diretório anterior após deletar o conteúdo
        ftp.rmd(diretório)  # Deleta o diretório vazio
        print(f"Diretório '{diretório}' deletado com sucesso.")
    except Exception as e:
        # Se o diretório não for encontrado ou houver outro erro, exibe a mensagem
        print(f"Erro ao deletar diretório '{diretório}': {e}")

# Exemplo de uso
if __name__ == "__main__":
    ftp = FTP()
    ftp.connect('ftp.servidor.com')  # Altere para o endereço do seu servidor FTP
    ftp.login('usuario', 'senha')  # Altere para suas credenciais
    
    listar_arquivos_servidor(ftp)

    ftp.quit()
