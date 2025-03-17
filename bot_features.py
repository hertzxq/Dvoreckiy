# commands.py
import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

def setup_commands(bot):
    @bot.command(name='delete')
    async def delete_messages(ctx, amount: int):
        if not ctx.channel.permissions_for(ctx.author).manage_messages:
            await ctx.send('У вас нет прав на удаление сообщений!')
            return

        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.send('У меня нет прав на удаление сообщений!')
            return

        if amount <= 0 or amount > 100:
            await ctx.send('Пожалуйста, укажите число от 1 до 100.')
            return

        try:
            deleted_messages = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'Удалено: {len(deleted_messages) - 1} сообщений!', delete_after=5)
        except discord.Forbidden:
            await ctx.send('У меня нет прав для удаления сообщений!')
        except Exception as e:
            await ctx.send(f'Произошла ошибка: {e}')

    @bot.command(name='add')
    async def add_music(ctx, *, url):
        if not ctx.author.voice:
            await ctx.send('Нужно находиться в голосовом канале, чтобы использовать эту функцию!')
            return

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']
                title = info.get('title', 'Неизвестный трек')
            except Exception as e:
                await ctx.send(f"Ошибка загрузки: {e}")
                return

        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS))
        await ctx.send(f'Играет: **{title}**')

    @bot.command(name='stop')
    async def stop_music(ctx):
        if ctx.voice_client is None:
            await ctx.send('Я не подключён к голосовому каналу!')
            return
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send('идите нахуй, я по сьебам')

def setup(bot):
    setup_commands(bot)