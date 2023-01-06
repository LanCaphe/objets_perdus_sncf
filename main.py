from App import Objet_perdu, Regularite, Weather, prophet
import discord, asyncio
import pandas as pd
from discord.ext import commands, tasks
from datetime import datetime
import pycron
import time
import logging as lg
import os
from table2ascii import table2ascii as t2a, PresetStyle

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

# client = commands.Bot(command_prefix='.')


# @client.command(pass_context=True)
# async def clear(ctx, amount=100):
#     channel = ctx.message.channel
#     messages = []
#     async for message in client.logs_from(channel, limit=int(amount)):
#         messages.append(message)
#     await client.delete_messages(messages)

# @client.command()
# async def predic_day():
#     forecast = prophet.predict_prophet()
#     embed = discord.Embed(
#         title = 'Ma prédiction des objets perdu sur les 5 prochains jours',
#         description ='Description0',
#         colour = discord.Colour.blue()
#     )
#     embed.set_footer(text='pied de la page')
#     embed.add_field(name='Date', value=forecast['ds'])
#     embed.add_field(name='Prediction', value=forecast['y'])
    
#     await client.say(embed=embed)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!dl"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await message.channel.send(f"{now} la suppression et create de la base de donnéee à commencé ")
        app()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await message.channel.send(f"{now} la base de donnée est pret")

    if message.content.startswith("!predict"):
        await message.channel.send(f"Veuillez patientez prédiction en cours")
        forecast = prophet.predict_prophet()
        await message.channel.send(f"Voici la prédiction d'objet perdu sur les 5 prochains jours")
        for i in range(0, len(forecast)):
            await message.channel.send(f"{forecast.iloc[i:i+1]}")
            
    if message.content.startswith("!day"):
        forecast = prophet.predict_prophet()
        output = t2a(
            header=forecast.columns.to_list(),
            body=forecast.values.tolist(),
            first_col_heading=True)
        await message.channel.send(f"```\n{output}\n```")

def cron():
    i=0
    while i > 3:
        if pycron.is_now('*/10 * * * *'):
                app()
                i = i + 1
        time.sleep(60)

def app():
    timenow = time.localtime()
    lg.info('delete et create database for objet perdu', str( time.strftime("%H:%M", timenow)))
    Objet_perdu.init_db()
    print('create objet perdu')
    lg.info('Import Objet perdu')
    Objet_perdu.import_all_objet_perdu()
    print('create weather')
    Weather.import_all_weather("LILLE-LESQUIN")
    print('create regulatie')
    Regularite.import_all_Regularite_gare_depart()
    Regularite.import_all_Regularite_gare_arrivee()
    print('done')


client.run(TOKEN)

    
    
    
