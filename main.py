import discord

import dotenv, os
from weatherCompiler import WeatherCompiler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

dotenv.load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

        #initializing scheduler
        scheduler = AsyncIOScheduler()

        scheduler.add_job(self.postSummary, CronTrigger(day_of_week="*", hour="12")) 

        #starting the scheduler
        scheduler.start()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'skyBot ping':
            await message.channel.send("O lord, he runnin on {}".format(os.uname()[1]))
        if message.content == 'skyBot summary':
            wc = WeatherCompiler()
            await message.channel.send(wc.getSummary())
        if message.content == 'skyBot details':
            wc = WeatherCompiler()
            await message.channel.send(wc.getDetails(goodOnly=False))
        if message.content == 'skyBot obstimes':
            wc = WeatherCompiler()
            await message.channel.send(wc.getDetails(goodOnly=True))
        if message.content == 'skyBot help' or message.content == 'skyBot':
            wc = WeatherCompiler()
            await message.channel.send(wc.getHelp())

    async def postSummary(self):
        c = self.get_channel(1022222495559983204)
        wc = WeatherCompiler()
        await c.send(wc.getSummary())


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.getenv("discordToken"))


