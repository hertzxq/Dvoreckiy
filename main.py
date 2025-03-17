import discord
from discord.ext import commands

import config, bot_features

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')


bot_features.setup_commands(bot=bot)

bot.run(token=config.TOKEN)
