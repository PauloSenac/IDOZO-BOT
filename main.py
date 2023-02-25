import discord
import openai
from datetime import datetime
import locale
import os
import requests

# Configuração da API do OpenAI
openai.api_key = "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"
model_engine = "text-davinci-002"

client = discord.Client()


@client.event
async def on_ready():
    print('O Bot está operando patrão 😎')


# Notificações de atts e upload de arquivos
@client.event
async def on_message(message):
    if message.channel.name == 'arquivos-texto':
        channel = discord.utils.get(message.guild.channels, name='anúncios')
        await channel.send(f'Foi postada uma atualização de nosso trabalho teórico no canal "{message.channel.name}", muito obrigado(a) "{message.author.mention}"! 💕')
    elif message.channel.name == 'arquivos-powerpoint':
        channel = discord.utils.get(message.guild.channels, name='anúncios')
        await channel.send(
            f'Há uma nova versão do PowerPoint disponível no canal "{message.channel.name}", o(a) "{message.author.mention}" fez algumas alterações, dê uma olhada lá! 😉')
    elif message.channel.name == 'site-configs':
        channel = discord.utils.get(message.guild.channels, name='anúncios')
        # Define o idioma e a região como português - Brasil
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        data_atual = datetime.now().strftime('%A, %d de %B de %Y, %H:%M:%S')
        await channel.send(
            f'Opaaa! Parece que houve uma atualização em nosso site 😎, dê uma conferida no canal "{message.channel.name}", a atualização foi realizada pelo(a) "{message.author.mention}" às {data_atual}! Se acaso encontrar algum bug/erro favor comunicar! ')

    # Comando "/site-status", confere em https, se retornar 200+, retorna online e vice-versa
    elif message.content.startswith('/site-status'):
        site_url = 'https://idozo.com.br/'
        try:
            response = requests.get(site_url)
            if response.status_code == 200:
                await message.channel.send(f'O site {site_url} está online!')
            else:
                await message.channel.send(f'O site {site_url} está offline.')
        except requests.exceptions.RequestException as e:
            await message.channel.send(f'Houve um erro ao acessar o site {site_url}. Detalhes: {e}')

    # Comando "/pesquisa"
    elif message.content.startswith('/pesquisa'):
        # Obtém a pesquisa a ser feita
        search_query = message.content[10:]

        # Usa a API do ChatGPT para gerar uma resposta
        response = openai.Completion.create(
            engine=model_engine,
            prompt=search_query,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Obtém a resposta gerada pelo ChatGPT
        answer = response.choices[0].text

        # Envia a resposta para o canal onde a mensagem foi enviada
        await message.channel.send(answer)
    # Comando "/ping",, retorna a latência entre o bot e o servidor do Discord
    elif message.content.startswith('/ping'):
        start_time = datetime.now()
        message_ping = await message.channel.send("Pong!")
        end_time = datetime.now()
        await message_ping.edit(content=f"Pong! Latência: {end_time - start_time}")


   # Comando "/comandos", exibe todos os comandos disponíveis
    elif message.content.startswith('/comandos'):
        command_list = ["/site-status", "/ping"]
        commands = "\n".join(command_list)
        await message.channel.send(f"Comandos disponíveis:\n{commands}")



# Boas Vindas Function
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='boas-vindas')
    await channel.send(f'Bem-vindo(a) ao servidor, {member.mention}! Esperamos que você tenha uma ótima experiência aqui! 🎉')


client.run("MTA3ODA0MDYxOTY0MzA2MDI3NA.GJuG9n.cfY08XOvLcxABjG7jgXf0T8nxAtVwhKelTn_-s")

