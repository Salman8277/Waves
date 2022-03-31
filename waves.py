
from nextcord.ext import commands
import nextcord
import wavelink

bot = commands.Bot(command_prefix='.')

# Events so I know that the bot is running and Wavelink node is connected.

@bot.event
async def on_ready():
    print("Bot is up and running!")
    bot.loop.create_task(node_connect())

@bot.event
async def on_wavelink_node_ready(node : wavelink.Node):
    print(f"Node {node.identifier} is ready!")

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='lavalink.oops.wtf', port=443, password='www.freelavalink.ga', https=True)

@bot.event
async def on_wavelink_track_end(player : wavelink.Player, track : wavelink.Track, reason):
    ctx = player.ctx
    vc : player = ctx.voice_client
    if vc.loop:
        return await vc.play(track)
    
    next_song = vc.queue.get()
    await vc.play(next_song)
    await ctx.send(f"Now Playing: {next_song.title}")

# Commands
# Play Command

@bot.command()
async def play(ctx : commands.Context,*,query : wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc : wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and vc.is_playing:
        await vc.play(query)
        embed = nextcord.Embed(title="Song Information", description=f"**Now Playing**: {query.title}\n**Duration**: {query.duration}\n**Artist**:  {query.author}", color=nextcord.Colour.random())
        embed.set_footer(text=f"Requested by: {ctx.author}")
        await ctx.send(embed=embed)

    else:
        await vc.queue.put_wait(query)
        await ctx.send(f"Added `{query.title}` to the queue!")
    vc.ctx = ctx
    setattr(vc, "loop", False)

# Pause Command

@bot.command()
async def pause(ctx : commands.Context):
    if not ctx.voice_client:
        embed = nextcord.Embed(title="Where's The Music?", description="You're not playing any music, dummy!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice,"channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    await vc.pause()
    pause_embed = nextcord.Embed(description="Paused your music!", color=nextcord.Colour.random())
    await ctx.send(embed=pause_embed)

# Resume Command

@bot.command()
async def resume(ctx : commands.Context):
    if not ctx.voice_client:
        embed = nextcord.Embed(title="Where's The Music?", description="You're not playing any music, dummy!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    await vc.resume()
    resume_embed = nextcord.Embed(description="Resumed your music!", color=nextcord.Colour.random())
    await ctx.send(embed=resume_embed)

# Stop Command

@bot.command()
async def stop(ctx : commands.Context):
    if not ctx.voice_client:
       embed = nextcord.Embed(title="Where's The Music?", description="You're not playing any music, dummy!", color=nextcord.Colour.random())
       return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    await vc.stop()
    stop_embed = nextcord.Embed(description="Stopped your music!", color=nextcord.Colour.random())
    await ctx.send(embed=stop_embed)

# Disconnect Command

@bot.command()
async def dc(ctx : commands.Context):
    if not ctx.voice_client:
        embed = nextcord.Embed(title="Wait, what?", description="I'm not even connected, dummy!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    await vc.disconnect()
    dc_embed = nextcord.Embed(description="Bot successfully disconnected! See ya later.", color=nextcord.Colour.random())
    await ctx.send(embed=dc_embed)

# Loop Command

@bot.command()
async def loop(ctx : commands.Context):
    if not ctx.voice_client:
       embed = nextcord.Embed(title="Where's The Music?", description="You're not playing any music, dummy!", color=nextcord.Colour.random())
       return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    try:
        vc.loop ^= True
    except Exception:
        setattr(vc,"loop", False)

    if vc.loop:
        loop_embed = nextcord.Embed(description="Loop is now enabled!", color=nextcord.Colour.random())
        return await ctx.send(embed=loop_embed)
    else:
        loop_embed = nextcord.Embed(description="Loop is now disabled!", color=nextcord.Colour.random())
        return await ctx.send(embed=loop_embed)

# Queue Command

@bot.command()
async def queue(ctx : commands.Context):
    if not ctx.voice_client:
       embed = nextcord.Embed(title="Where's The Music?", description="You're not playing any music, dummy!", color=nextcord.Colour.random())
       return await ctx.send(embed=embed)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(title="You are not in a Voice Channel", description="Please join a Voice Channel first!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    else:
        vc : wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        embed = nextcord.Embed(description="Queue is empty!", color=nextcord.Colour.random())
        return await ctx.send(embed=embed)
    em = nextcord.Embed(title="Queue", color=nextcord.Colour.random())
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        em.add_field(name=f"Song# {song_count}", value=f"{song.title}")
    return await ctx.send(embed=em)

bot.run('OTUyOTcxMjc4MjUwMjk1Mjk3.Yi9xqg.XhaRhmfV2zJkFVfeG0aI8Ch3C6s')