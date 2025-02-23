import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from testModel import predict_comment


def run_bot2():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents) #creates bot and sets intents
    tree = app_commands.CommandTree(client) #allows to work with slash

    
    @client.event
    async def on_ready():
        print('Bot is running')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        prediction = predict_comment((message.content).strip())
        print(f"Message content: {repr(message.content)}")
        print(f"Prediction: {prediction}")  # Debugging output
        
        if prediction == 1:
            await message.channel.send("bad")
        elif prediction == 0:
            await message.channel.send("good")

    
    client.run(TOKEN)
    


