from ftplib import FTP, error_perm
import os
import discord
from discord.ext import commands

# Configuração dos servidores FTP
servidores_ftp = [
    {"ip": "25.58.38.220", "usuario": "usuario1", "senha": "senha1"},
    {"ip": "25.23.12.169", "usuario": "usuario2", "senha": "senha2"},
]

# Função para conectar a um servidor FTP
def conectar_ftp(servidor):
    try:
        ftp = FTP(servidor["ip"])
        ftp.login(user=servidor["usuario"], passwd=servidor["senha"])
        print(f"Conectado ao FTP: {servidor['ip']}")
        return ftp
    except Exception as e:
        print(f"Erro ao conectar em {servidor['ip']}: {e}")
        return None

# Criar conexões com os servidores disponíveis
def conectar_todos_os_servidores():
    return {srv["ip"]: conectar_ftp(srv) for srv in servidores_ftp if conectar_ftp(srv)}

conexoes_ftp = conectar_todos_os_servidores()

# Função para reconectar servidores offline
def reconectar_servidores():
    global conexoes_ftp
    for ip, ftp in conexoes_ftp.items():
        if ftp is None:
            conexoes_ftp[ip] = conectar_ftp(next(srv for srv in servidores_ftp if srv["ip"] == ip))

# Função para escolher o melhor servidor para upload
def escolher_melhor_servidor():
    menor_servidor = None
    menor_qtd_arquivos = float('inf')
    for ip, ftp in conexoes_ftp.items():
        if ftp:
            try:
                qtd_arquivos = len(ftp.nlst())
                if qtd_arquivos < menor_qtd_arquivos:
                    menor_qtd_arquivos = qtd_arquivos
                    menor_servidor = ftp
            except Exception:
                pass
    return menor_servidor

# Função para listar todos os arquivos nos servidores
def listar_todos_os_arquivos():
    arquivos_unificados = set()
    for ftp in conexoes_ftp.values():
        if ftp:
            try:
                arquivos_unificados.update(ftp.nlst())
            except Exception:
                pass
    return list(arquivos_unificados)

# Função para upload de arquivo
def upload_arquivo(ftp, caminho_arquivo):
    if ftp is None:
        print("Nenhum servidor FTP disponível para upload.")
        return
    try:
        nome_arquivo = os.path.basename(caminho_arquivo)
        with open(caminho_arquivo, 'rb') as arquivo:
            ftp.storbinary(f'STOR {nome_arquivo}', arquivo)
        print(f"Arquivo '{nome_arquivo}' enviado para {ftp.host}")
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

# Função para download de arquivo
def download_arquivo(nome_arquivo):
    for ftp in conexoes_ftp.values():
        if ftp:
            try:
                caminho_download = os.path.join(os.path.expanduser("~"), "Downloads", nome_arquivo)
                with open(caminho_download, 'wb') as arquivo_local:
                    ftp.retrbinary(f'RETR {nome_arquivo}', arquivo_local.write)
                print(f"Arquivo '{nome_arquivo}' baixado para {caminho_download}")
                return caminho_download
            except Exception:
                pass
    print("Arquivo não encontrado em nenhum servidor.")
    return None

# Função para apagar arquivo
def apagar_arquivo(nome_arquivo):
    for ftp in conexoes_ftp.values():
        if ftp:
            try:
                ftp.delete(nome_arquivo)
                print(f"Arquivo '{nome_arquivo}' apagado com sucesso.")
                return True
            except Exception:
                pass
    print("Erro ao apagar arquivo ou arquivo não encontrado.")
    return False

# Configuração do bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event    
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='listar')
async def listar(ctx):
    arquivos = listar_todos_os_arquivos()
    response = "\n".join(arquivos) if arquivos else "Nenhum arquivo encontrado nos servidores FTP."
    await ctx.send(response)

@bot.command(name='upload')
async def upload(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_path = f"./{attachment.filename}"
            await attachment.save(file_path)
            ftp = escolher_melhor_servidor()
            if ftp:
                upload_arquivo(ftp, file_path)
                os.remove(file_path)
                await ctx.send(f"Arquivo '{attachment.filename}' enviado para o servidor FTP.")
            else:
                await ctx.send("Nenhum servidor disponível para upload.")
    else:
        await ctx.send("Por favor, anexe um arquivo para fazer o upload.")

@bot.command(name='download')
async def download(ctx, nome_arquivo: str):
    caminho = download_arquivo(nome_arquivo)
    if caminho:
        await ctx.send(file=discord.File(caminho))
        os.remove(caminho)
    else:
        await ctx.send("Arquivo não encontrado nos servidores FTP.")

@bot.command(name='apagar')
async def apagar(ctx, nome_arquivo: str):
    if apagar_arquivo(nome_arquivo):
        await ctx.send(f"Arquivo '{nome_arquivo}' apagado com sucesso.")
    else:
        await ctx.send("Erro ao apagar o arquivo ou arquivo não encontrado.")

@bot.command(name='desconectar')
async def desconectar(ctx):
    global conexoes_ftp
    for ftp in conexoes_ftp.values():
        if ftp:
            try:
                ftp.quit()
            except Exception:
                pass
    conexoes_ftp = {}
    await ctx.send("Conexão com os servidores FTP encerrada.")

@bot.command(name='reconectar')
async def reconectar(ctx):
    reconectar_servidores()
    await ctx.send("Servidores FTP reconectados.")

@bot.command(name='menu')
async def menu(ctx):
    comandos = (
        "`!listar` - Lista arquivos dos servidores FTP.",
        "`!upload` - Envia um arquivo anexado para o FTP.",
        "`!download <nome_arquivo>` - Baixa um arquivo do FTP.",
        "`!apagar <nome_arquivo>` - Apaga um arquivo do FTP.",
        "`!desconectar` - Encerra conexão com os servidores FTP.",
        "`!reconectar` - Tenta reconectar servidores FTP offline.",
    )
    await ctx.send("\n".join(comandos))

# Inicia o bot do Discord
if __name__ == "__main__":
    TOKEN = 'ADD_TOKEN_HERE'
    bot.run(TOKEN)
