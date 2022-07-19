import discord
from discord.ext import commands
from discord.utils import get
from mutagen.mp3 import MP3
import time
intents = discord.Intents.default()
intents.members = True
intents.reactions = True



TOKEN = "YOUR_DISCORD_BOT_TOKE_HERE"


BOT_PREFIX = "D"


bot = commands.Bot(command_prefix=BOT_PREFIX)
sb_text = "Shreks Soundboarde:\n😐 for Rickroll"



async def print_sb(ctx):
    global sound_board
    sound_board = await ctx.send(sb_text)
    await sound_board.add_reaction("😐")

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name+"\n")


@bot.command(pass_context=True, aliases=['j', 'sb'])
@commands.has_role("soundboard")
async def soundboard(ctx):


    await print_sb(ctx)
    global voice
    global channel
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
@bot.event
async def on_reaction_add(reaction, user):

    if user == sound_board.author:
        pass
    elif reaction.message.id == sound_board.id :
        voice = get(bot.voice_clients)
        channel = user.voice.channel
        if voice and voice.is_connected():  
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f'The Bot has connected to {channel}\n')
        track_name = str(reaction)
        voice.play(discord.FFmpegPCMAudio(track_name + ".mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.2  # Ist die Lautstärke

        await sound_board.delete()
        await reaction.message.channel.purge(limit =1)
        audio = MP3(f"{track_name}.mp3")
        time.sleep(audio.info.length)
        await voice.disconnect()

bot.run(TOKEN)
