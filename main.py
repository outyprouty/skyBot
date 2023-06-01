import discord
from discord.ext import commands
import dotenv, os
from weatherCompiler import WeatherCompiler

dotenv.load_dotenv()




class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'skyBot summary':
            wc = WeatherCompiler()
            await message.channel.send(wc.getSummary())
        if message.content == 'skyBot details':
            wc = WeatherCompiler()
            await message.channel.send(wc.getDetails())
        if message.content == 'skyBot help':
            wc = WeatherCompiler()
            await message.channel.send(wc.getHelp())

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.getenv("discordToken"))


