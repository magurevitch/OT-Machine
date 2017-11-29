import discord
from discord.ext import commands
import src.controller as controller
from static.discord_keys import * 
import json

description = "Tambajna Optimality Theory"
bot_prefix = "!"

file = open("static/tambajna_phonology.txt")
language = controller.makeLanguage(json.loads(file.read()))

client = commands.Bot(description=description,command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("logged in")
    print("Name : {}".format(client.user.name))
    print('Id : {}'.format(client.user.id))
    
@client.command(pass_context=True)
async def ping(cxt):
    await client.say("Pong!")
                     
@client.command(pass_context=True,
                brief="gives the phonology of Tambajna",
                help="gives the phonology of Tambajna\nwhen a phoneme has <brackets> after it, the left is the default orthography, and the right is the one-letter orthography")
async def phonology(cxt):
    await client.say(cxt.message.author.mention)
    await client.say("Consonants")
    await client.say('''```
+------------+-----------+-----------+------------------------+
|            |  labial   |  coronal  |          velar         |
|            |           |           |   plain    | labialzd. |
+------------+-----------+-----------+------------+-----------+
| nasal      | m         | n         | ŋ <ng N>   | ŋʷ <nw W> |
+------------+-----------+-----------+------------+-----------+
| s  plain   | p         | t         | k          | kʷ <kw q> |
| t ---------+-----------+-----------+------------+-----------+
| o  prenas. | ᵐb <mb b> | ⁿd <nd d> | ᵑɡ <ngg g> |           |
| p ---------+-----------+-----------+------------+-----------+
|    eject.  |           | t’ <t' T> | k’ <k' K>  |           |
+------------+-----------+-----------+------------+-----------+
| fricative  | f         | s         | x          | xʷ <xw Q> |
+------------+-----------+-----------+------------+-----------+
| approx.    |           | ɾ <r>     |            |           |
+------------+-----------+-----------+------------+-----------+
```''')
    await client.say("Vowels")
    await client.say('''```
       Front   Cent.   Back
------+--------------------+
 High  \ i             u   |
  ------+------------------+
   Mid   \       ə <e>     |
    ------+----------------+
     Low   \      a        |
     -------+--------------+
```''')
    await client.say("Diphthongs and multiphoneme sequences")
    await client.say('''```
+-----------------+
|        aj       |
+-----------------+
|        aw       |
+-----------------+
|        ja       |
+-----------------+
|        wa       |
+-----------------+
|  iə̯ |    <iy>   |
+-----+-----------+
|  uə̯ |    <uy>   |
+-----+-----------+
|  r  |    <rr>   |
+-----+-----------+
|  ŋŋ |  <nng NN> |
+-----+-----------+
|  ŋg | <nngg Ng> |
+-----+-----------+
| ŋŋʷ | <nngw NW> |
+-----+-----------+
```''')
    await client.say("Marginal phonemes")
    await client.say("h, r <rr>, j, w")
    
inputHelp = '''
\njust seperate multiple words by spaces
Here are a few flags you can use
 -p Shows the prosody (stress, syllable boundaries)
 -s Use the single letter orthography
 -x Output in XML format
 -v Output a verbose string
 -b Borrow a word
'''

@client.command(pass_context=True,
                brief="computes the surface form a word, or words",
                help="computes the surface form a word, or words" + inputHelp)
async def word(cxt,*args):
    flags = " ".join([arg.replace("-","") for arg in args if arg[0] == '-'])
    words = [word for word in args if word[0] != '-']
    orthography = False if 's' in flags else 'typing'
    prosody = 'p' not in flags
    form = "String"
    if 'v' in flags:
        form = "Verbose String"
    if 'x' in flags:
        form = "XML"
    borrow = 'b' in flags
    entries = [controller.toForm[form](language.entry(word,orthography,prosody,borrow)) for word in words]
    await client.say(cxt.message.author.mention)
    if entries:
        await client.say("\n".join(entries))
    else:
        await client.say("next time, also write the words you want computed")
        
@client.command(pass_context=True,
                brief="computes the noun declension of a word, or words",
                help="computes the noun declension of a word, or words" + inputHelp)
async def noun(cxt,*args):
    flags = " ".join([arg.replace("-","") for arg in args if arg[0] == '-'])
    words = [word for word in args if word[0] != '-']
    orthography = False if 's' in flags else 'typing'
    prosody = 'p' not in flags
    form = "String"
    if 'v' in flags:
        form = "Verbose String"
    if 'x' in flags:
        form = "XML"
    if 'b' in flags:
        entries = [controller.toForm[form](entry) for word in words for entry in language.bestConjugation('N',word,orthography,prosody)]
    else:
        entries = [controller.toForm[form](language.conjugate('N',word,orthography,prosody)) for word in words]
    await client.say(cxt.message.author.mention)
    if entries:
        entries = "\n\n".join(entries)
        for i in range(0,len(entries),1800):
            await client.say(entries[:1800])
            entries = entries[1800:]
        if entries:
            await client.say(entries)
    else:
        await client.say("next time, also write the words you want computed")
    
client.run(discord_key)