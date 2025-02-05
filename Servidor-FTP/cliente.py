from ftplib import FTP, error_perm
import os
import discord
from discord.ext import commands

# Configurações do servidor FTP
ip_servidor = "127.0.0.1"  # Endereço IP do servidor FTP
usuario_ftp = "usuario"
senha_ftp = "senha123"

# Função para enviar erro com tratamento diferenciado
async def enviar_erro(erro, ctx=None):
    """Envia erros tanto para o console (CMD) quanto para o Discord."""
    # Envia para o console (CMD)
    print(f"Erro (CMD): {erro}")
    
    # Envia para o Discord, caso o contexto (ctx) seja fornecido
    if ctx:
        if isinstance(erro, ConnectionError):
            mensagem_discord = f"**Erro de Conexão**: Não foi possível conectar ao servidor FTP. Verifique o endereço IP ou suas credenciais."
        elif isinstance(erro, FileNotFoundError):
            mensagem_discord = f"**Arquivo Não Encontrado**: O arquivo que você está tentando acessar não foi encontrado no servidor FTP."
        elif isinstance(erro, PermissionError):
            mensagem_discord = f"**Permissão Negada**: Não foi possível realizar a operação devido a falta de permissões."
        elif isinstance(erro, ValueError):
            mensagem_discord = f"**Argumento Inválido**: {erro}"
        elif isinstance(erro, error_perm):
            mensagem_discord = f"**Erro de Permissão FTP**: Problema ao acessar o arquivo no servidor FTP. Verifique as permissões."
        else:
            mensagem_discord = f"**Erro desconhecido**: {erro}"
        await ctx.send(mensagem_discord)

# Configurações do servidor FTP
def conectar_ftp():
    """Estabelece uma conexão com o servidor FTP."""
    try:
        ftp = FTP(ip_servidor)
        ftp.login(user=usuario_ftp, passwd=senha_ftp)
        print("Conexão com o servidor FTP estabelecida com sucesso.")
        return ftp
    except Exception as e:
        enviar_erro(e)  # Apenas no console
        return None

ftp = conectar_ftp()

def renomear_arquivos(ftp):
    """Renomeia arquivos removendo espaços e underscores do nome."""
    try:
        arquivos = ftp.nlst()
        for arquivo in arquivos:
            novo_nome = arquivo.replace(" ", "").replace("_", "")
            if novo_nome != arquivo:
                ftp.rename(arquivo, novo_nome)
                print(f"Arquivo renomeado: {arquivo} -> {novo_nome}")
    except Exception as e:
        enviar_erro(e)  # Apenas no console

# Função para listar arquivos no servidor FTP
def listar_arquivos_servidor(ftp):
    """Lista arquivos e diretórios no servidor FTP."""
    if ftp is None:
        enviar_erro("Conexão FTP não estabelecida.")
        return []
    try:
        arquivos = ftp.nlst()
        return arquivos
    except Exception as e:
        enviar_erro(e)  # Apenas no console
        return []

# Função para upload de arquivo
def upload_arquivo(ftp, caminho_arquivo):
    """Realiza o upload de um arquivo para o servidor FTP."""
    if ftp is None:
        enviar_erro("Conexão FTP não estabelecida.")
        return
    try:
        nome_arquivo = os.path.basename(caminho_arquivo)
        novo_nome = nome_arquivo.replace(" ", "").replace("_", "")
        with open(caminho_arquivo, 'rb') as arquivo:
            ftp.storbinary(f'STOR {novo_nome}', arquivo)
        print(f"Arquivo '{nome_arquivo}' enviado como '{novo_nome}' para o servidor FTP.")
    except FileNotFoundError as e:
        enviar_erro(f"Arquivo não encontrado: {e}", ftp)  # Envia erro específico para Discord
    except PermissionError as e:
        enviar_erro(f"Permissão negada ao acessar o arquivo: {e}", ftp)  # Envia erro de permissão para Discord
    except Exception as e:
        enviar_erro(e)  # Apenas no console

# Função para download de arquivo
def download_arquivo(ftp, nome_arquivo):
    """Realiza o download de um arquivo do servidor FTP."""
    if ftp is None:
        enviar_erro("Conexão FTP não estabelecida.")
        return None
    try:
        caminho_download = os.path.join(os.path.expanduser("~"), "Downloads", nome_arquivo)
        diretorio_destino = os.path.dirname(caminho_download)
        if not os.path.exists(diretorio_destino):
            os.makedirs(diretorio_destino)
        if not os.access(diretorio_destino, os.W_OK):
            raise PermissionError(f"Sem permissão para gravar no diretório: {diretorio_destino}")
        with open(caminho_download, 'wb') as arquivo_local:
            ftp.retrbinary(f'RETR {nome_arquivo}', arquivo_local.write)
        print(f"Arquivo '{nome_arquivo}' baixado com sucesso para: {caminho_download}")
        return caminho_download
    except FileNotFoundError as e:
        enviar_erro(f"Arquivo não encontrado no servidor: {e}", ftp)  # Envia erro específico para Discord
    except PermissionError as e:
        enviar_erro(f"Permissão negada ao salvar o arquivo: {e}", ftp)  # Envia erro de permissão para Discord
    except Exception as e:
        enviar_erro(e)  # Apenas no console

# Função para apagar arquivo
def apagar_arquivo(ftp, nome_arquivo):
    """Apaga um arquivo do servidor FTP."""
    if ftp is None:
        enviar_erro("Conexão FTP não estabelecida.")
        return
    try:
        # Verifica se o arquivo existe antes de tentar apagar
        arquivos = ftp.nlst()
        if nome_arquivo not in arquivos:
            raise FileNotFoundError(f"O arquivo '{nome_arquivo}' não existe no servidor FTP.")
        
        ftp.delete(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' apagado com sucesso do servidor FTP.")
    except FileNotFoundError as e:
        enviar_erro(f"Arquivo não encontrado para apagar: {e}", ftp)  # Envia erro específico para Discord
    except PermissionError as e:
        enviar_erro(f"Permissão negada para apagar o arquivo: {e}", ftp)  # Envia erro de permissão para Discord
    except error_perm as e:
        enviar_erro(f"Erro de permissão no FTP: {e}", ftp)  # Erro de permissão no servidor FTP
    except Exception as e:
        enviar_erro(e)  # Apenas no console

# Configurações do bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event    
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado. Use `!menu` para ver a lista de comandos disponíveis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"**Erro de Argumento**: Você esqueceu de passar algum argumento. Use `!menu` para ver os comandos corretamente.")
    else:
        await enviar_erro(f"Ocorreu um erro: {error}", ctx)

# Comandos do bot para o Discord
@bot.command(name='listar')
async def listar(ctx):
    if ctx.guild:
        try:
            arquivos = listar_arquivos_servidor(ftp)
            response = "\n".join(arquivos) if arquivos else "Nenhum arquivo encontrado no servidor FTP."
            await ctx.send(response)
        except Exception as e:
            await enviar_erro(f"Erro ao listar arquivos: {e}", ctx)

@bot.command(name='upload')
async def upload(ctx):
    if ctx.guild:
        if ctx.message.attachments:
            try:
                for attachment in ctx.message.attachments:
                    file_path = f"./{attachment.filename}"
                    await attachment.save(file_path)
                    upload_arquivo(ftp, file_path)
                    os.remove(file_path)
                    await ctx.send(f"Arquivo '{attachment.filename}' enviado ao servidor FTP.")
            except Exception as e:
                await enviar_erro(f"Erro ao enviar o arquivo: {e}", ctx)
        else:
            await ctx.send("Por favor, anexe um arquivo para fazer o upload.")

@bot.command(name='download')
async def download(ctx, nome_arquivo: str):
    if ctx.guild:
        try:
            caminho_destino = download_arquivo(ftp, nome_arquivo)
            if caminho_destino:
                await ctx.send(file=discord.File(caminho_destino))
                await ctx.send(f"Arquivo '{nome_arquivo}' baixado com sucesso.")
                os.remove(caminho_destino)
            else:
                await ctx.send(f"Erro ao baixar o arquivo '{nome_arquivo}'.")
        except Exception as e:
            await enviar_erro(f"Erro ao baixar o arquivo: {e}", ctx)

@bot.command(name='apagar')
async def apagar(ctx, nome_arquivo: str = None):
    """Função para apagar arquivos no servidor FTP com verificação de erro para argumento ausente."""
    if ctx.guild:
        if nome_arquivo is None:
            await ctx.send("**Erro**: Você precisa fornecer o nome do arquivo que deseja apagar.")
            return
        try:
            apagar_arquivo(ftp, nome_arquivo)
            await ctx.send(f"Arquivo '{nome_arquivo}' apagado com sucesso.")
        except Exception as e:
            await enviar_erro(f"Erro ao apagar o arquivo: {e}", ctx)

@bot.command(name='desconectar')
async def desconectar(ctx):
    global ftp
    if ftp:
        try:
            ftp.quit()
            ftp = None
            await ctx.send("Conexão com o servidor FTP encerrada.")
        except Exception as e:
            await enviar_erro(f"Erro ao desconectar do servidor FTP: {e}", ctx)
    else:
        await ctx.send("O bot não está conectado ao servidor FTP.")

@bot.command(name='menu')
async def menu(ctx):
    """Mostra todas as opções de comando e o que elas fazem."""
    comandos = (
        "`!listar` - Lista arquivos e diretórios no servidor FTP.",
        "`!upload` - Faz o upload de um arquivo anexado para o servidor FTP.",
        "`!download` <nome_arquivo> - Baixa um arquivo do servidor FTP.",
        "`!apagar` <nome_arquivo> - Apaga um arquivo do servidor FTP.",
        "`!desconectar` - Desconecta o bot do servidor FTP.",
    )
    await ctx.send("\n".join(comandos))

# Inicia o bot do Discord
if __name__ == "__main__":
    TOKEN = 'MTMzMzQ4NDQzMDM1ODIxNjc2NQ.GH_t8e.ACo9vRkdLV7rajsRwwDEZy31HjHqDv3MVjU6O8'
    bot.run(TOKEN)
