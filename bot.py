import discord
import os
import random
from dotenv import load_dotenv
import responses
from discord import app_commands

load_dotenv()
intents = intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
token = os.getenv('TOKEN')

async def send_msg(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_bot():
    
    @client.event
    async def on_ready():
        await tree.sync()
        print("Logged in as a bot {0.user}".format(client))
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said: '{user_message}' ({channel})")
        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_msg(message, user_message, is_private=True)
        else:
            await send_msg(message, user_message, is_private=False)
            
    @tree.command(name = "sayhi", description = "My first application Command")     
    async def first_command(interaction):
        await interaction.response.send_message("<@"+str(interaction.user.id)+">")
        
    client.run(token)