import discord
import json
from discord.ext import commands

config = json.load(open('config.json'))

bot = commands.Bot(command_prefix=['--', '––'], description='Need a multitool?!')
bot.remove_command('help')

extensions = ['MultiCommands']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':

    """for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(Exception, error))"""


bot.run(config['token'])