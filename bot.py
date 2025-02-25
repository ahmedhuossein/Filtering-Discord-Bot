import discord
import pandas as pd
from discord import app_commands
from dotenv import load_dotenv
import os
from test_model import predict_comment


def run_bot2():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

    client = discord.Client(intents=intents) #creates bot and sets intents
    tree = app_commands.CommandTree(client) #allows to work with slash commands
    @client.event
    async def on_ready():
        print('Bot is running')
        await tree.sync()
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        prediction = predict_comment((message.content).strip())
        if prediction == 1:
            message_type = "bad" if prediction == 1 else "good"
            mod_channel = discord.utils.get(message.guild.text_channels, name="mod-channel")
            mod_sent = await mod_channel.send(f"User: {message.author.mention}\nMessage: {message.content}\nPrediction: {message_type}\nIs this prediction correct?")
            await mod_sent.add_reaction("✅")
            await mod_sent.add_reaction("❌") 
        #elif prediction == 0:
            #await message.channel.send("good")

    @client.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        mod_channel = discord.utils.get(reaction.message.guild.text_channels, name="mod-channel")
        original_message = reaction.message.content.partition("Message: ")[2]
        if reaction.message.channel.name == "mod-channel":
            if reaction.emoji == "✅":
                value = 1
                await mod_channel.send(f"{user.mention} has approved the message!")
            elif reaction.emoji == "❌":
                value = 0
                await mod_channel.send(f"{user.mention} has rejected the message!") 
            data = {
                'comment_text': [original_message],
                'bad': [value]
            }
            new_comments = pd.DataFrame(data)
            file_path = 'new_comments.csv'
            new_comments.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False, sep=',', encoding='utf-8')
            await mod_channel.send(file=discord.File('new_comments.csv'))

    @tree.command(name='clear_csv', description='Clear the CSV file')
    async def clear_csv(interaction: discord.Interaction):
        df = pd.read_csv('new_comments.csv')
        df = df.iloc[0:0]
        df.to_csv('new_comments.csv', index=False, sep=',', encoding='utf-8')
        await interaction.response.send_message('The CSV file has been cleared.')

    @tree.command(name='view_csv', description='View the CSV file')
    async def view_csv(interaction: discord.Interaction):
        df = pd.read_csv('new_comments.csv')
        await interaction.response.send_message(file=discord.File('new_comments.csv'))
    client.run(TOKEN)

    


