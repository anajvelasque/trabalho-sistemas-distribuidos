from ftplib import FTP
import os
import discord
from discord.ext import commands

# Configurações do servidor FTP
ip_servidor = "127.0.0.1"  # Endereço IP do servidor FTP
usuario_ftp = "usuario"
senha_ftp = "senha123"

# Conecta ao servidor FTP
def conectar_ftp():
    """Estabelece uma conexão com o servidor FTP."""
    try:
        ftp = FTP(ip_servidor)
        ftp.login(user=usuario_ftp, passwd=senha_ftp)
        print("Conexão com o servidor FTP estabelecida com sucesso.")
        return ftp
    except Exception as e:
        print(f"Erro ao conectar ao servidor FTP: {e}")
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
        print(f"Erro ao renomear arquivos: {e}")

# Executa a renomeação ao iniciar
renomear_arquivos(ftp)

def listar_arquivos_servidor(ftp):
    """Lista arquivos e diretórios no servidor FTP."""
    if ftp is None:
        print("Conexão FTP não estabelecida.")
        return []
    try:
        arquivos = ftp.nlst()
        return arquivos
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return []

def upload_arquivo(ftp, caminho_arquivo):
    """Realiza o upload de um arquivo para o servidor FTP."""
    if ftp is None:
        print("Conexão FTP não estabelecida.")
        return
    try:
        nome_arquivo = os.path.basename(caminho_arquivo)
        novo_nome = nome_arquivo.replace(" ", "").replace("_", "")
        with open(caminho_arquivo, 'rb') as arquivo:
            ftp.storbinary(f'STOR {novo_nome}', arquivo)
        print(f"Arquivo '{nome_arquivo}' enviado como '{novo_nome}' para o servidor FTP.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")

def download_arquivo(ftp, nome_arquivo):
    """Realiza o download de um arquivo do servidor FTP."""
    if ftp is None:
        print("Conexão FTP não estabelecida.")
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
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return None

def apagar_arquivo(ftp, nome_arquivo):
    """Apaga um arquivo do servidor FTP."""
    if ftp is None:
        print("Conexão FTP não estabelecida.")
        return
    try:
        ftp.delete(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' apagado com sucesso do servidor FTP.")
    except Exception as e:
        print(f"Erro ao apagar o arquivo: {e}")

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
    else:
        await ctx.send(f"Ocorreu um erro: {error}")

@bot.command(name='listar')
async def listar(ctx):
    if ctx.guild:
        try:
            arquivos = listar_arquivos_servidor(ftp)
            response = "\n".join(arquivos) if arquivos else "Nenhum arquivo encontrado no servidor FTP."
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Erro ao listar arquivos: {e}")

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
                    await ctx.send(f"Arquivo '{attachment.filename}' enviado e renomeado automaticamente no servidor FTP.")
            except Exception as e:
                await ctx.send(f"Erro ao enviar o arquivo: {e}")
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
            await ctx.send(f"Erro ao baixar o arquivo: {e}")

@bot.command(name='apagar')
async def apagar(ctx, nome_arquivo: str):
    if ctx.guild:
        try:
            apagar_arquivo(ftp, nome_arquivo)
            await ctx.send(f"Arquivo '{nome_arquivo}' apagado com sucesso.")
        except Exception as e:
            await ctx.send(f"Erro ao apagar o arquivo: {e}")

@bot.command(name='desconectar')
async def desconectar(ctx):
    global ftp
    if ftp:
        try:
            ftp.quit()
            ftp = None
            await ctx.send("Conexão com o servidor FTP encerrada.")
        except Exception as e:
            await ctx.send(f"Erro ao desconectar do servidor FTP: {e}")
    else:
        await ctx.send("O bot não está conectado ao servidor FTP.")

if __name__ == "__main__":
    TOKEN = 'MTMzMzQ4NDQzMDM1ODIxNjc2NQ.GH_t8e.ACo9vRkdLV7rajsRwwDEZy31HjHqDv3MVjU6O8'
    bot.run(TOKEN)
