import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import get
import youtube_dl
import os
import time

client = commands.Bot(command_prefix='ADD YOUR COMMAND PREFIX HERE')
TOKEN = 'ADD YOUR TOKEN BOT HERE'
client.remove_command('help')

#bot ready command
@client.event
async def on_ready():
    print('Login sebagai {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('Mencari Prestasi'))

#error handling command not found
#@client.event
#async def on_command_error(ctx, error):
#	if isinstance(error, CommandNotFound):
#		await ctx.send('maaf command ga nemu')

#check ping command
@client.command(pass_context=True)
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**Pong!**  `{int(ping)}ms`")

#help menu command
@client.command(aliases=['h', 'he', 'hel'])
async def help(ctx):
	embedHelp = discord.Embed(title='**Help Menu**', 
    description='**Information**\n`$helps info`\n\n**Music**\n`$helps music`', 
    colour=5923425)
	await ctx.send(embed=embedHelp)

#helps info command
@client.command()
async def helps(ctx, arg):
    embedHelpsInfo = discord.Embed(title='**Helps Information**', 
    description='`$arrow`\nPenjelasan divisi Arrow\n\n`$asapena`\nPenjelasan divisi Asapena\n\n`$polaris`\nPenjelasan divisi Polaris\n\n`$slogan`\nSlogan KIRSTAL 38', 
    colour=5923425)
    embedHelpsMusic = discord.Embed(title='**Helps Music (BETA)**', 
    description='`$join`\nmasukin bot ke voice channel\n\n`$play`\n$play (link youtube)\n\n`$leave`\nkeluarin bot setelah selesai', 
    colour=5923425)
    embedWrong = discord.Embed(description='Argumen pada `$help` salah')
    if arg == 'info':
        await ctx.send(embed=embedHelpsInfo)
    elif arg == 'music':
        await ctx.send(embed=embedHelpsMusic)
    elif arg != 'info' and 'music':
        await ctx.send(embed=embedWrong)

#helps info Arrow
@client.command(pass_context=True)
async def arrow(ctx):
    embedArrow = discord.Embed(title='**Arrow**',
    description='\n_Divisi yang bergerak di bidang mekanika,elektronika dan programming. Divisi Arrow sering menginovasi kan teknologi juga bekerjasama dengan divisi Asapena untuk perlombaan dan menjalin relasi dengan univ. Gunadarma. Divisi ini juga memiliki agenda seperti merakit robot, pelatihan robotik, dan mengikuti kompetisi bidang robotik ataupun rekayasa teknologi._',
    colour=5923425)
    await ctx.send(embed=embedArrow)

#helps info Asapena
@client.command(pass_context=True)
async def asapena(ctx):
    embedAsapena = discord.Embed(title='**Asapena**',
    description='\n_Divisi yang bergerak untuk melatih penulisan proposal penelitian/karya tulis ilmiah, baik di bidang sosial, sains, dan rekayasa teknologi(yang sangat bisa membantu kalian untuk melatih skill membuat skripsi pada saat kuliah nanti), mengikuti lomba penelitian atau karya tulis ilmiah, serta menjalin relasi dengan KIRJAS (Himunan KIR setiap sekolah di wilayah Jakarta Selatan), LIPI, dan BPPT._',
    colour=5923425)
    await ctx.send(embed=embedAsapena)

#helps info Polaris
@client.command(pass_context=True)
async def polaris(ctx):
    embedPolaris = discord.Embed(title='**Polaris**',
    description='\n_Divisi yang bergerak di bidang astronomi. Dengan tujuan menggali minat dan bakat siswa dalam bidang astronomi, mengikuti lomba olimpiade astronomi, mengikuti program pembelajaran HAAJ (Himpunan Astronomi Amatir Jakarta)._',
    colour=5923425)
    await ctx.send(embed=embedPolaris)

#helps info Slogan
@client.command(pass_context=True)
async def slogan(ctx):
    embedSlogan = discord.Embed(title='**Slogan KIRSTAL 38**',
    description='\n_**KIRSTAL..!** Berfikir dan bersikap ilmiah_',
    colour=5923425)
    await ctx.send(embed=embedSlogan)

#music join command
@client.command(pass_context=True, aliases=['j', 'jo', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Bot masuk ke Voice {channel}\n")

    await ctx.send(f"Bot masuk ke Channel Voice {channel}")

#music leave command
@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot keluar dari Voice {channel}")
        await ctx.send(f"Bot keluar dari Channel Voice {channel}")
    else:
        print("Bot disuruh keluar dari voice, tapi tidak ada")
        await ctx.send("Bot tidak di Channel Voice")

#music play command
@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Ga bisa delete song, lagi playing")
        await ctx.send("ERROR: saat mulai Music")
        return

    await ctx.send("Loading..")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Download audio (mp3) sekarang\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"File ganti nama: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Lagu selesai main!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Mulai musik: {nname[0]}")
    print("Mulai musik\n")

client.run(TOKEN)
