import discord
from discord.ext import commands
import src.controller as controller
from static.discord_keys import * 

description = "Tambajna Optimality Theory"
bot_prefix = "!"

file = open("src/tambajna_phonology.txt")
language = controller.makeLanguage(eval(file.read()))

client = commands.Bot(description=description,command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("logged in")
    print("Name : {}".format(client.user.name))
    print('Id : {}'.format(client.user.id))
    
@client.command(pass_context=True)
async def ping(cxt):
    await client.say("Pong!")
    
@client.command(pass_context=True)
async def word(cxt,*args):
    entries = [controller.toString(language.entry(word)) for word in args]
    await client.say(cxt.message.author.mention)
    if entries:
        await client.say("\n".join(entries))
    else:
        await client.say("next time, also write the words you want computed")
        
@client.command(pass_context=True)
async def noun(cxt,*args):
    entries = [controller.toString(language.conjugate('N',word)) for word in args]
    await client.say(cxt.message.author.mention)
    if entries:
        await client.say("\n".join(entries))
    else:
        await client.say("next time, also write the words you want computed")
    
client.run(discord_key)