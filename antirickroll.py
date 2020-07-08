import discord
import asyncio
from discord.ext import commands
import ast
from numpy import loadtxt
import logging
import datetime
import json
from pathlib import Path

description = '''AntiRickRoll'''
bot = commands.Bot(command_prefix='arr!', description=description)

bot.remove_command('help')

async def status_task():
    global bad_words
    bad_words = []
    badWords = []
    while True:
        with open('data/links.txt') as my_file:
            badWords = my_file.readlines()
            for word in badWords:
                bad_words.append(word[:-1])
        await asyncio.sleep(1200)

def config_load():
    with open('data/config.json', 'r', encoding='utf-8-sig') as doc:
        return json.load(doc)

async def run():
    config = config_load()
    bot = Bot(config=config,
              description=config['description'])
    bot.remove_command("help")

    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="arr!",
            description=kwargs.pop('description')
        )
        self.start_time = None
        self.app_info = None

        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

    async def track_start(self):
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await asyncio.sleep(1) 
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                print(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'failed to load extension {error}')
            print('-' * 10)

    async def on_ready(self):
        print('-' * 10)
        self.app_info = await self.application_info()
        print(f'Logged in as: {self.user.name}\n'
              f'Using discord.py version: {discord.__version__}\n'
              f'Owner: {self.app_info.owner}')
        print('-' * 10)
    
    async def on_guild_join(self, guild):

        embed = discord.Embed(title="AntiRickRoll", description="Thank you for inviting AntiRickRoll!\n\nPlease use `arr!help` for a list of commands", color=16711680)

        await guild.text_channels[0].send(embed=embed)

        print(f'Added to new guild: {guild.name}')
        print('-'*10)

        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '?'

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


