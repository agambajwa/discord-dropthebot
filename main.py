import discord
from discord.ext import commands
import json, random, requests, html
import http.client
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="bot")
client = discord.Client()
client = commands.Bot(command_prefix='d.')

stateDict = {
        'AN': "Andaman and Nicobar Islands",
        'AP': "Andhra Pradesh",
        'AR': "Arunachal Pradesh",
        'AS': "Assam",
        'BR': "Bihar",
        'CH': "Chandigarh",
        'CT': "Chhattisgarh",
        'DL': "Delhi",
        'DN': "Dadra and Nagar Haveli and Daman and Diu",
        'GA': "Goa",
        'GJ': "Gujarat",
        'HP': "Himachal Pradesh",
        'HR': "Haryana",
        'JH': "Jharkhand",
        'JK': "Jammu and Kashmir",
        'KA': "Karnataka",
        'KL': "Kerala",
        'LA': "Ladakh",
        'MH': "Maharashtra",
        'ML': "Meghalaya",
        'MN': "Manipur",
        'MP': "Madhya Pradesh",
        'MZ': "Mizoram",
        'NL': "Nagaland",
        'OR': "Odisha",
        'PB': "Punjab",
        'PY': "Puducherry",
        'RJ': "Rajasthan",
        'SK': "Sikkim",
        'TG': "Telangana",
        'TN': "Tamil Nadu",
        'TR': "Tripura",
        'UP': "Uttar Pradesh",
        'UT': "Uttarakhand",
        'WB': "West Bengal"
    }

codeDict = {
        'anda' : 'AN',
        'andh' : 'AP',
        'arun' : 'AR',
        'assa' : 'AS',
        'biha' : 'BR',
        'chan' : 'CH',
        'chha' : 'CT',
        'delh' : 'DL',
        'dama' : 'DN',
        'dadr' : 'DN',
        'goa' : 'GA',
        'guja' : 'GJ',
        'hima' : 'HP',
        'hary' : 'HR',
        'jhar' : 'JH',
        'jamm' : 'JK',
        'karn' : 'KA',
        'kera' : 'KL',
        'lada' : 'LA',
        'maha' : 'MH',
        'megh' : 'ML',
        'mani' : 'MN',
        'madh' : 'MP',
        'mizo' : 'MZ',
        'naga' : 'NL',
        'odis' : 'OR',
        'punj' : 'PB',
        'pudu' : 'PY',
        'pond' : 'PY',
        'raja' : 'RJ',
        'sikk' : 'SK',
        'tela' : 'TG',
        'tami' : 'TN',
        'trip' : 'TR',
        'uttar p' : 'UP',
        'uttara' : 'UT',
        'west' : 'WB',
        'beng' : 'WB'
    }

defineURL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
connectionCovid = http.client.HTTPSConnection("api.covid19india.org")
chuckURL = "https://api.chucknorris.io/jokes"
insultURL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
oWeatherURL = "https://api.openweathermap.org/data/2.5/onecall"
imageURL = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
complimentURL = "https://complimentr.com/api"
jokeURL = "https://v2.jokeapi.dev/joke/Any?format=text"
dadJokesURL = "https://icanhazdadjoke.com/"

dadJokesHeaders = {
    'Accept' : 'application/json'
    }
imageHeaders = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': ""
    }
defineHeaders = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': ""
    }

client.remove_command('help')

def sendTime(timeStr):
    date = timeStr.split("T")[0]
    time = timeStr.split("T")[1].split("+")[0]
    timeStr = date + " | " + time
    return timeStr

async def sendIndianCovidData(ctx):
    try:
        connectionCovid.request("GET", "/v4/data.json")
        response = connectionCovid.getresponse()
        data = response.read()
        data = json.loads(data.decode())
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.message.add_reaction('😭')
        await ctx.send("Some error occurred on the Discord's end, try again.")
        return
    except:
        await ctx.message.add_reaction('😭')
        await ctx.send("Some unknown error occurred, try again.")
        return 

    # Frustrating checks
    if 'delta' in data['TT']:
        if 'confirmed' in data['TT']['delta']:
            deltaConf = "(+" + str(data['TT']['delta']['confirmed']) + ")"
        else:
            deltaConf = "(+0)"
        
        if 'deceased' in data['TT']['delta']:
            deltaDec = "(+" + str(data['TT']['delta']['deceased']) + ")"
        else: 
            deltaDec = "(+0)"
        
        if 'recovered' in data['TT']['delta']:
            deltaRec = "(+" + str(data['TT']['delta']['recovered']) + ")"
        else:
            deltaRec = "(+0)"
    else:
        deltaConf = "(+0)"
        deltaDec = "(+0)"
        deltaRec = "(+0)"

    embed = discord.Embed(title = f"**COVID-19 Data for India**", description = f"Updated on {sendTime(str(data['TT']['meta']['last_updated']))}", color = 0xffff00)
    embed.add_field(name = "Confirmed", value = str(data['TT']['total']['confirmed']) + " " + deltaConf, inline = False)
    embed.add_field(name = "Deceased", value = str(data['TT']['total']['deceased']) + " " + deltaDec, inline = False)
    embed.add_field(name = "Recovered", value = str(data['TT']['total']['recovered']) + " " + deltaRec, inline = False)
    embed.add_field(name = "Tested", value = str(data['TT']['total']['tested']) + " - _As on " + str(data['TT']['meta']['tested']['last_updated']) + "_", inline = False)

    embed.set_footer(text=f"Data by api.covid19india.org - DropTheBot")
    await ctx.message.add_reaction('✅')
    await ctx.send(embed = embed)
    return

async def sendStateCovidData(ctx, code):
    try:
        connectionCovid.request("GET", "/v4/data.json")
        response = connectionCovid.getresponse()
        data = response.read()
        data = json.loads(data.decode())
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.message.add_reaction('😭')
        await ctx.send("Some error occurred on the Discord's end, try again.")
        return
    except:
        await ctx.message.add_reaction('😭')
        await ctx.send("Some unknown error occurred, try again.")
        return 
    
    await ctx.message.add_reaction('✅')
    stateName = stateDict.get(code, "Invalid")
    stateTotal = data[code]['total']
    embed = discord.Embed(title = f"**COVID-19 Data for {stateName}**", description = f"Updated on {sendTime(str(data[code]['meta']['last_updated']))}", color = 0xffff00)
    
    # Frustrating checks
    if 'confirmed' in stateTotal:
        stateConf = str(stateTotal['confirmed'])
    else:
        stateConf = ""
    if 'deceased' in stateTotal:
        stateDec = str(stateTotal['deceased'])
    else:
        stateDec = ""
    if 'recovered' in stateTotal:
        stateRec = str(stateTotal['recovered'])
    else:
        stateRec = ""
    if 'tested' in stateTotal:
        stateTes = str(stateTotal['tested'])
    else:
        stateTes = ""
    if 'delta' in data[code]:
        stateDelta = data[code]['delta']
        if 'confirmed' in stateDelta:
            stateDConf = " (+" + str(stateDelta['confirmed']) + ")"
        else:
            stateDConf = "(+0)"
        if 'deceased' in stateDelta:
            stateDDec = " (+" + str(stateDelta['deceased']) + ")"
        else:
            stateDDec = "(+0)"
        if 'recovered' in stateDelta:
            stateDRec = " (+" + str(stateDelta['recovered']) + ")"
        else:
            stateDRec = "(+0)"
    else:
        stateDConf = "(+0)"
        stateDDec = "(+0)"
        stateDRec = "(+0)"

    # building embed
    embed = discord.Embed(title = f"**COVID-19 Data for {stateName}**", description = f"Updated on {sendTime(str(data[code]['meta']['last_updated']))}", color = 0xffff00)
    
    if stateConf != "":
        embed.add_field(name = "Confirmed", value = stateConf + " " + stateDConf, inline = False)
    if stateDec != "":
        embed.add_field(name = "Deceased", value = stateDec + " " + stateDDec, inline = False)
    if stateRec != "":
        embed.add_field(name = "Recovered", value = stateRec + " " + stateDRec, inline = False)
    if stateTes != "":
        embed.add_field(name = "Tested", value = stateTes, inline = False)

    embed.set_footer(text=f"Data by api.covid19india.org - DropTheBot")
    await ctx.send(embed = embed)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    statustxt = "d.help | REZ IS BACK v3.2"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)


# Help Command
@client.command()
async def help(ctx, *, query):
    query = str(query).lower()
    if query == 'animals' or query == 'animal':
        embed=discord.Embed(color = 0xffff00,title = f"Animals", description = "")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "bird/birb", value = "Returns a picture of a birb! 🐤")
        embed.add_field(name = "bunny", value = "Returns a GIF of a bunny! 🐇")
        embed.add_field(name = "cat/pussy/meow/kitty/catto", value = "Returns a picture of a cat! 🐈")
        embed.add_field(name = "dog/doggo/woof", value = "Returns a picture of a dog! 🐶")
        embed.add_field(name = "duck/quack", value = "Returns a picture of a duck! 🦆")
        embed.add_field(name = "fox", value = "Returns a picture of a fox! 🦊")
        embed.add_field(name = "owl", value = "Returns a picture of an owl! 🦉")
        embed.add_field(name = "lizard", value = "Returns a picture of a lizard! 🦎")
        embed.add_field(name = "shibe", value = "Returns a picture of a shibe! 🐕")
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'avatar' or query == 'av':
        embed=discord.Embed(color = 0xffff00,title = f"Avatar", description = "`Aliases : av, a`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "avatar", value = "Returns your avatar. 👀", inline = True)
        embed.add_field(name = "avatar [user]", value = "Returns the avatar of the 'user' you mention. 👀", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'ping':
        await ctx.message.add_reaction('🏓')
        await ctx.send("https://tenor.com/view/cats-ping-pong-gif-8942945")
    elif query == 'compliment':
        embed=discord.Embed(color = 0xffff00,title = f"Compliment", description = "")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "compliment", value = "I will compliment you! 😊", inline = True)
        embed.add_field(name = "compliment [user]", value = "I will compliment 'user'! 😊", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'covid':
        embed=discord.Embed(color = 0xffff00,title = f"Indian COVID Data", description = "")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "covid", value = "Returns COVID-19 Data for India.", inline = True)
        embed.add_field(name = "covid [state]", value = "Returns COVID-19 Data for the 'state' (or UT) you mention.", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'rajnikanth' or query == 'rj':
        embed=discord.Embed(color = 0xffff00,title = f"Rajnikanth Facts!", description = "`Aliases : rj, rajni`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "rajnikanth", value = "Returns random Rajnikanth fact.", inline = True)
        embed.add_field(name = "rajnikanth categories", value = "Returns available categories.", inline = True)
        embed.add_field(name = "rajnikanth [category]", value = "Returns random Rajnikanth fact for the 'category' you mentioned.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'define' or query == 'df' or query == 'ud definition':
        embed=discord.Embed(color = 0xffff00,title = f"Urban Dictionary Definitions", description = "`Aliases : def, df, ud, urban`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "define [word]", value = "Returns the Urban Dictionary definiton of the 'word' you mentioned.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'fun':
        embed=discord.Embed(color = 0xffff00,title = f"Fun commands", description = "Useless bunch of shit.")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "bhagwa <user>", value = "Returns Bhagwa percentage. 🧡", inline = True)
        embed.add_field(name = "rajnikanth", value = "Returns random Rajnikanth fact. `d.help rajnikanth` for more", inline = True)
        embed.add_field(name = "compliment <user>", value = "Make me compliment you or a 'user'. `d.help compliment` for more", inline = True)
        embed.add_field(name = "insult <user>", value = "Make me insult you or a 'user'. `d.help insult` for more", inline = True)
        embed.add_field(name = "gif", value = "Fetch GIFs from Giphy.com. `d.help gif` for more", inline = True)
        embed.add_field(name = "pp <user>", value = "Measure pp sizes.", inline = True)
        embed.add_field(name = "simp <user>", value = "Measure SIMP-ness!", inline = True)
        embed.add_field(name = "yoda", value = "Returns Yodish translation of some text you mention. `d.help yoda` for more", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'image' or query == 'img':
        embed=discord.Embed(color = 0xffff00,title = f"Image Search", description = "`Aliases : i, img, photu`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "image [query]", value = "Returns an image for the 'query'", inline = True)
        embed.set_footer(text = f"NSFW Search works only in NSFW channels | {client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'gif' or query == 'giphy':
        embed=discord.Embed(color = 0xffff00,title = f"GIF Search", description = "`Aliases : giphy, g`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "gif", value = "Returns a random GIF from Giphy", inline = True)
        embed.add_field(name = "gif [query]", value = "Returns a GIF for the 'query'", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'insult' or query == 'roast':
        embed=discord.Embed(color = 0xffff00,title = f"Insult.", description = "`Aliases : roast`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "insult", value = "I will insult you! 😊", inline = True)
        embed.add_field(name = "insult [user]", value = "I will insult 'user'! 😊", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'jokes' or query == 'joke':
        embed=discord.Embed(color = 0xffff00,title = f"Jokes", description = "")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "dadjoke", value = "Returns an amazing dad joke.", inline = True)
        embed.add_field(name = "joke/chutkula", value = "Returns a random joke, these could be NSFW. ⚠", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'weather':
        embed=discord.Embed(color = 0xffff00,title = f"Weather", description = "`Aliases : w, mausam`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "weather [place]", value = "Returns weather info for the 'place' you mention.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'yoda' or query == 'yodish':
        embed=discord.Embed(color = 0xffff00,title = f"Yodish Translator", description = "`Aliases : yodish`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "yoda [text]", value = "Returns Yodish translation of the 'text' you mention. Translations may be gibberish or not be any different than what you sent at times.", inline=True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)
    elif query == 'invite':
        await ctx.message.add_reaction('❎')
        await ctx.send("No.")
    else: 
        await ctx.message.add_reaction('❎')
        await ctx.send("I don't know man, I am lost with that one too.")

@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(color = 0xffff00, title = f"Yello! I am DropTheBot 🤗", description = "`Bot Prefix : d.`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "Animals", value = "To get pictures of animals!", inline=True)
        embed.add_field(name = "Avatar", value = "View the avatar of users or your own, for... whatever reasons. 👀", inline = True)
        embed.add_field(name = "COVID", value = "COVID-19 Data for India or Indian states.", inline = True)
        embed.add_field(name = "Fun", value = "Some random useless fun commands. 🤷‍♂️", inline=True)
        embed.add_field(name = "Image search", value = "Search images.", inline=True)
        embed.add_field(name = "GIF Search", value = "Look up GIFs on Giphy.", inline = True)
        embed.add_field(name = "Jokes", value = "Returns jokes. `d.help jokes` for more", inline = True)
        embed.add_field(name = "Ping", value = "Returns pong.", inline = True)
        embed.add_field(name = "Weather", value = "Get weather info for a place.", inline=True)
        embed.add_field(name = "UD Definition", value = "Get the Urban Dictionary definiton of a word.", inline = True)
        embed.add_field(name = "Invite", value = "My invite link if you wish to add me. 👉👈", inline=True)
        embed.add_field(name = "Vote", value = "Links to vote for me. 😳", inline=True)
        embed.set_footer(text = f"d.help [command/category] for more info on a command/category | {client.user.name}", icon_url = client.user.avatar_url)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)


# Fun auto responses
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    if message.content.lower().find('who is') != -1 and message.content.endswith('?'):
        if(random.randint(0,2) == 1):
            await message.channel.send('ur mom')
        elif(random.randint(0,2) == 2):
            await message.channel.send('ur dad')
        return
    if message.content.lower().find('why') != -1 and message.content.endswith('?'):
        if(random.randint(0,2) == 1):
            await message.channel.send('ask ur mom')
        elif(random.randint(0,2) == 2):
            await message.channel.send('ask ur dad')
        return
    if message.content.lower() == 'twss':
        await message.channel.send('https://media.discordapp.net/attachments/737504783937830927/808990223966928906/unknown.png')
        return
    if message.content.lower() == 'toyst':
        await message.channel.send('https://tenor.com/view/brooklyn99-sex-tape-title-gif-16147025')
        return
    if message.content.lower() == 'mcph':
        await message.channel.send('https://tenor.com/view/arey-maa-chudi-padi-hai-gif-19171762')
        return
    if message.content.lower() == 'heavy driver':
        await message.channel.send('https://tenor.com/view/h-eavy-driver-heavy-gif-19884562')
        return
    if message.content.lower() == "that's illegal" or message.content.lower() == "that is illegal" or message.content.lower() == 'wti':
        await message.channel.send('https://tenor.com/view/wait-that-thats-is-illegal-gif-18393263')
        return
    if message.content.lower() == 'bsdk':
        await message.channel.send('https://tenor.com/view/bhosdi-ke-mirzapur-kaaleen-bhaiya-well-gif-17332070')
        return
    if message.content.lower() == 'who asked' or message.content.lower() == 'who fucking asked' or message.content.lower() == 'who tf asked':
        await message.channel.send('https://tenor.com/view/air-force-military-jet-plane-fighter-gif-17096343')
        return
    if message.content.lower() == 'notty notty' or message.content.lower() == 'naughty naughty' or message.content.lower() == 'you notty notty'  or message.content.lower() == 'you naughty naughty':
        await message.channel.send('https://tenor.com/view/u-noty-noty-u-teasing-me-u-noty-noty-you-naughty-naughty-you-teasing-me-you-naughty-naughtyyy-you-naughty-you-naughty-naughty-you-teasing-me-gif-19937565')
        return
    if message.content.lower() == 'nobody cares':
        await message.channel.send('https://tenor.com/view/nobody-cares-nobody-cares-spongebob-imagination-gif-8176136')
        return
    if message.content.lower() == 'rakh':
        await message.channel.send('https://tenor.com/view/akshay-kumar-rakh-teri-maa-ki-rakh-phir-hera-pheri-baburao-bollywood-gif-15735934')
        return
    if message.content.lower() == 'mast joke':
        await message.channel.send('https://tenor.com/view/phir-hera-pheri-mast-joke-mara-baburao-babu-bhaiyaa-raju-gif-17606989')
        return
    if message.content.lower() == 'kehna kya chahte ho'  or message.content.lower() == 'kehna kya':
        await message.channel.send('https://tenor.com/view/wtf-is-going-on-wtf-what-do-you-mean-confused-huh-gif-16986940')
    return

client.add_listener(on_message, 'on_message')


@client.command(aliases = ['chutkula'], pass_context = True)
async def joke(ctx):
    try:
        response = requests.request("GET", jokeURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    if data['type'] == 'single':
        await ctx.message.add_reaction('✅')
        await ctx.send(data['joke'])
    else:
        await ctx.message.add_reaction('✅')
        await ctx.send(data['setup'] + "\n\n" + data['delivery'])


@client.command()
async def dadjoke(ctx):
    try:
        response = requests.request("GET", dadJokesURL, headers= dadJokesHeaders)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['joke'])


# Server count command
@client.command()
async def count(ctx):
    serverCount = len(client.guilds)
    await ctx.send("I am in " + str(serverCount) + " servers!")


# Invite link command
@client.command()
async def invite(ctx):
    embed=discord.Embed(color = 0xffff00,title = f"Click below to add me! 🤗")
    embed.add_field(name = "_ _", value = "[Invite](bot-link)")
    await ctx.message.add_reaction('✅')
    await ctx.send(embed = embed)


# Vote link command
@client.command()
async def vote(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.send('bot-link')
    await ctx.send('bot-link')


# Insult command
@client.command(aliases = ['roast'], pass_context = True)
async def insult(ctx, member : discord.Member):
    try:
        response = requests.request("GET", insultURL)
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The god damn API failed me!')
        return

    await ctx.message.add_reaction('✅')
    data = response.json()
    await ctx.send(member.mention + " - " + html.unescape(data['insult']))
@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        try:
            response = requests.request("GET", insultURL)
        except:
            await ctx.message.add_reaction('😫')
            await ctx.send('The god damn API failed me!')
            return
        await ctx.message.add_reaction('✅')
        data = response.json()
        await ctx.send(ctx.message.author.mention + " - " + html.unescape(data['insult']))
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Hey " + ctx.message.author.mention + "! I need a proper user to insult them, try again, you fuck.")


# Compliment command
@client.command()
async def compliment(ctx, member : discord.Member):
    try:
        response = requests.request("GET", complimentURL)
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('Well, the API failed me.')
        return
    data = response.json()
    compliment = data['compliment']
    compliment = compliment.replace(compliment[0], compliment[0].upper(), 1)
    await ctx.message.add_reaction('✅')
    await ctx.send(member.mention + " : " + compliment + ".")

# Compliment Error
@compliment.error
async def compliment_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        try:
            response = requests.request("GET", complimentURL)
        except:
            await ctx.message.add_reaction('😫')
            await ctx.send('Well, the API failed me.')
            return
        data = response.json()
        compliment = data['compliment']
        compliment = compliment.replace(compliment[0], compliment[0].upper(), 1)
        await ctx.message.add_reaction('✅')
        await ctx.send(ctx.message.author.mention + " : " + compliment + ".")
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('😘')
        await ctx.send("Hey " + ctx.message.author.mention + "! I need a proper user to compliment them, try again boo.")


# PP command
@client.command()
async def pp(ctx, member: discord.Member):
    if(random.randint(0,15) == 10):
        await ctx.message.add_reaction('🤯')
        embed = discord.Embed(title="🤯", description=f"{member.name}'s PP too long! \n 8======================3", colour=discord.Colour(0xffff00))
    else:
        n = random.randint(1,9)
        str = '8'
        for _ in range(n):
            str = str + '='
        str = str + '3'
        await ctx.message.add_reaction('😏')
        embed = discord.Embed(title="😏", description=f"{member.name}'s PP \n" + str, colour=discord.Colour(0xffff00))

    embed.set_footer(text=f"Requested by {ctx.message.author.name}")
    await ctx.send(embed = embed)

# PP Error
@pp.error
async def pp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if(random.randint(0,15) == 10):
            await ctx.message.add_reaction('🤯')
            embed = discord.Embed(title="🤯", description=f"{ctx.message.author.name}'s PP too long! \n 8======================3", colour=discord.Colour(0xffff00))
        else:
            n = random.randint(1,9)
            str = '8'
            for _ in range(n):
                str = str + '='
            str = str + '3'
            await ctx.message.add_reaction('😏')
            embed = discord.Embed(title="😏", description= f"{ctx.message.author.name}'s PP \n" + str, colour=discord.Colour(0xffff00))
        await ctx.send(embed = embed)
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Mention a real user next time, okay? Good.")


# SIMP Command
@client.command(aliases = ['simprate'], pass_context = True)
async def simp(ctx, member : discord.Member):
    n = random.randint(1,100)
    await ctx.message.add_reaction('✅')
    await ctx.send(member.name + " is " + str(n) + "% SIMP.")

# SIMP error
@simp.error
async def simp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        n = random.randint(1,100)
        await ctx.message.add_reaction('✅')
        await ctx.send(ctx.message.author.name + " is " + str(n) + "% SIMP.")
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Mention a real user next time, okay? Good.")


# Bhagwa command
@client.command()
async def bhagwa(ctx, member : discord.Member):
    n = random.randint(1,100)
    await ctx.message.add_reaction('✅')
    await ctx.send(member.name + " is " + str(n) + "% bhagwa.")

# Bhagwa error
@bhagwa.error
async def bhagwa_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        n = random.randint(1,100)
        await ctx.message.add_reaction('✅')
        await ctx.send(ctx.message.author.name + " is " + str(n) + "% bhagwa.")
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Mention a real user next time, okay? Good.")


# Random ping command
@client.command()
async def ping(ctx):
    await ctx.message.add_reaction('🏓')
    await ctx.send('Pong! ' + str(round(client.latency * 1000.0, 1)) + ' ms')


# COVID Command
@client.command()
async def covid(ctx, *, state):
    state = str(state).lower()
    code = ""
    for e in codeDict:
        if state.startswith(e):
            code = codeDict.get(e, "")
            break
    if code != "":
        await sendStateCovidData(ctx = ctx, code = code)
    else:
        await ctx.message.add_reaction('❎')
        await ctx.send("Incorrect state name, please try again.")

@covid.error
async def covid_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendIndianCovidData(ctx = ctx)


# UD Definition Command
@client.command(aliases = ['def', 'df', 'ud', 'urban'], pass_context = True)
async def define(ctx, *, query):
    if(random.randint(0,10) == 6):
        await ctx.message.add_reaction('😝') 
        await ctx.send('https://tenor.com/view/golmaal3-johnny-lever-pappi-bhai-mai-nahi-bataunga-mein-nahi-bataunga-gif-17855218')
        return
    word = str(query)
    try:
        querystring = {"term": word}
        response = requests.request("GET", defineURL, headers=defineHeaders, params=querystring)
        data = response.json()
        first = data['list'][0]

        count = ""
        if(len(data['list'])-1 > 1):
            count = str(len(data['list']) - 1)
        else:
            count = 'no'
        await ctx.message.add_reaction('✅')
        await ctx.send('**Definition - **' + first['definition'])
        await ctx.send('**Example - **_' + first['example'] + "_")
        await ctx.send("(<" + first['permalink'] + ">) There are " + count + " other definitions.")
    except Exception as e:
        await ctx.message.add_reaction('❎')
        await ctx.send("Either there is no definition for the word, or some error occurred. Anyway, I couldn't care less ¯\_(ツ)_/¯")
        print(e)

@define.error
async def define_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction('⁉')
        await ctx.send("I need a damn word to look up, how bout you try again?")


# Avatar Command
@client.command(aliases = ['av', 'a'], pass_context = True)
async def avatar(ctx, member: discord.Member):
    try:
        await ctx.message.add_reaction('👀')
        embed = discord.Embed(title="👀",description=f"Here is {member.mention}'s avatar, ya damn stalker", colour=discord.Colour(0xffff00))
        embed.set_image(url = member.avatar_url)
    except:
        await ctx.message.add_reaction('🤬')
        embed = discord.Embed(title="🤬",description=f"Dumb fookin error occurred!", colour=discord.Colour(0xffff00))
    embed.set_footer(text=f"Requested by {ctx.message.author.name} | {client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed = embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction('🤦‍♂️')
        embed = discord.Embed(title="🤦‍♂️",description=f"Uh, okay, look at yourself, you narcissistic human.", colour=discord.Colour(0xffff00))
        embed.set_image(url=ctx.message.author.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.message.author.name} | {client.user.name}", icon_url=client.user.avatar_url)
        await ctx.send(embed = embed)
    
    if isinstance(error, commands.BadArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Mention a real user next time, okay? Good.")


# Rajni Command
@client.command(aliases = ['rj', 'rajni'], pass_context = True)
async def rajnikanth(ctx, *, text):
    text = str(text).lower()
    try:
        response = requests.get(chuckURL+"/categories")
        categories = response.json()
    except:
        await ctx.message.add_reaction('😭')
        await ctx.send("Welp, an error occurred, try again or go cry to your mommy.")
        return
        
    if text == 'categories':
        string = ""
        for ele in categories:
            string = string + ele.upper() + '\n'
        embed = discord.Embed(title = f"**Rajnikanth Facts Categories**", description = f"**Available categories:** \n {string}", color = 0xffff00)
        await ctx.message.add_reaction('✅')
        await ctx.send(embed = embed)

    elif text in categories:
        if text == 'explicit' and ctx.message.channel.nsfw==False:
            await ctx.message.add_reaction('⁉')
            await ctx.send("Wait a minute, this ain't a NSFW channel! Feck off!")
        else:
            try: 
                response = requests.get(chuckURL+"/random?category="+text)
                data = response.json()
            except:
                await ctx.message.add_reaction('😭')
                await ctx.send("Welp, an error occurred, try again or go cry to your mommy.")
                return
            
            fact = data['value'].replace("Chuck Norris", "Rajnikanth")
            fact = fact.replace("Norris", "Rajni")
            fact = fact.replace("Chuck", "Rajni")
            embed = discord.Embed(title = f"**Rajnikanth Fact**", description = f"**{text.upper()}** : {fact}", color = 0xffff00)
            embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/rmTjGndr2vIm2pDyWBqDJEnW1x8G200ROQE6DA7N6QM/https/i.pinimg.com/originals/f9/a8/e9/f9a8e9c541c8df26cf97160593a78eae.jpg?width=634&height=670")
            embed.set_footer(text=f"Totally legitmate, 100% true and trustworthy, completely reliable and truthful. Don't @ me though, I am a bot, won't respond anyway.")
            await ctx.message.add_reaction('✅')
            await ctx.send(embed = embed)
    else:
        await ctx.message.add_reaction('⁉')
        await ctx.send("I literally have a command to check the available categories, still you send dumb shit to me!")

@rajnikanth.error
async def rajnikanth_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        try:
            response = requests.get(chuckURL+"/random")
            data = response.json()
            fact = data['value'].replace("Chuck Norris", "Rajnikanth")
            fact = fact.replace("Norris", "Rajni")
            fact = fact.replace("Chuck", "Rajni")
            embed = discord.Embed(title = f"**Rajnikanth Fact**", description = fact, color = 0xffff00)
            embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/rmTjGndr2vIm2pDyWBqDJEnW1x8G200ROQE6DA7N6QM/https/i.pinimg.com/originals/f9/a8/e9/f9a8e9c541c8df26cf97160593a78eae.jpg?width=634&height=670")
            embed.set_footer(text=f"Totally legitmate, 100% true and trustworthy, completely reliable and truthful. Don't @ me though, I am a bot, won't respond anyway.")
            await ctx.message.add_reaction('✅')
            await ctx.send(embed = embed)
        except:
            await ctx.message.add_reaction('😭')
            await ctx.send("Welp, an error occurred, try again or go cry to your mommy.")


# Weather Command
@client.command(aliases = ['w', 'mausam'], pass_context = True) 
async def weather(ctx, *, query):
    query = str(query)
    location = geolocator.geocode(query)
    if(location == None):
        await ctx.message.add_reaction('❎')
        await ctx.send("Could not find the location you mentioned, learn some Geography I guess.")
        return
    try:
        response = requests.get(oWeatherURL + '?lat=' + str(location.latitude) + '&lon=' + str(location.longitude) + '&appid=xxxx&units=metric&exclude=minutely,hourly,alerts,daily')
    except:
        await ctx.message.add_reaction('😭')
        await ctx.send("Error occurred at the API's end.")
        return
    data = response.json()
    temp = str(data['current']['temp']) + "°"
    weather = data['current']['weather'][0]['main']
    iconUrl = 'http://openweathermap.org/img/w/' + data['current']['weather'][0]['icon'] + '.png'
    feelsLike = str(data['current']['feels_like']) + "°"

    embed=discord.Embed(color = 0xffff00, title = temp, description = weather + " | Feels like " + feelsLike)
    embed.set_thumbnail(url = iconUrl)
    embed.add_field(name = "🌏", value=str(location.address), inline=False)
    embed.set_footer(text = f"Weather by OpenWeather | {client.user.name}", icon_url = client.user.avatar_url)
    await ctx.message.add_reaction('✅')
    await ctx.send(embed = embed)

@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Umm, share a location too next time, thanks.")


# Yoda Command
@client.command(aliases = ['yodish'], pass_context = True)
async def yoda(ctx, *, text):
    text = str(text)
    try:
        yodaURL = "http://yoda-api.appspot.com/api/v1/yodish?text="
        response = requests.get(yodaURL+text)
        data = response.json()
    except:
        await ctx.send("Failed by the API, I have been.")
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data["yodish"])

@yoda.error
async def yoda_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction('❎')
        await ctx.send("Text to translate, I need.")


# Animal Commands
animalURL = "http://shibe.online/api/"
@client.command(aliases = ['pussy', 'meow', 'kitty', 'catto'], pass_context = True)
async def cat(ctx):
    try:
        response = requests.request("GET", animalURL + "cats")
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data[0])

@client.command(aliases = ['birb'], pass_context = True)
async def bird(ctx):
    try:
        response = requests.request("GET", animalURL + "birds")
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data[0])

@client.command()
async def shibe(ctx):
    try:
        response = requests.request("GET", animalURL + "shibes")
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data[0])

dogURL = "https://dog.ceo/api/breeds/image/random"

@client.command(aliases = ['doggo', 'woof'], pass_context = True)
async def dog(ctx):
    try:
        response = requests.request("GET", dogURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['message'])

foxURL = "https://randomfox.ca/floof/"

@client.command()
async def fox(ctx):
    try:
        response = requests.request("GET", foxURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['image'])

duckURL = "https://random-d.uk/api/random"

@client.command(aliases = ['quack'], pass_context = True)
async def duck(ctx):
    try:
        response = requests.request("GET", duckURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['url'])

bunnyURL = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

@client.command()
async def bunny(ctx):
    try:
        response = requests.request("GET", bunnyURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['media']['gif'])

lizardURL = "https://nekos.life/api/v2/img/lizard"

@client.command()
async def lizard(ctx):
    try:
        response = requests.request("GET", lizardURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['url'])

owlURL = "http://pics.floofybot.moe/owl"

@client.command()
async def owl(ctx):
    try:
        response = requests.request("GET", owlURL)
        data = response.json()
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The API failed me!')
        return
    await ctx.message.add_reaction('✅')
    await ctx.send(data['image'])


# GIF Command
giphyURL = "https://api.giphy.com/v1/gifs/random"

@client.command(aliases = ['giphy', 'g'], pass_context = True)
async def gif(ctx, *, query):
    query = str(query)
    param = {
        'api_key': 'api-key',
        'tag': query,
    }
    try:
        response = requests.request("GET", giphyURL, params = param)
        data = response.json()
    except Exception as e:
        print(e)
        return
    if data['meta']['status'] == 400:
        await ctx.message.add_reaction('❎')
        await ctx.send("Ya made a mistake somewhere, FIX IT!")
    elif data['meta']['status'] == 403:
        await ctx.message.add_reaction('❎')
        await ctx.send("Wow, GIPHY told me to fuck off.")
    elif data['meta']['status'] == 404 or 'embed_url' not in data['data']:
        await ctx.message.add_reaction('❎')
        await ctx.send("Welp, ya got us. We could not find a GIF for that.")
    elif data['meta']['status'] == 429:
        await ctx.message.add_reaction('❎')
        await ctx.send("OI! You're requesting too fast, slow down.")
    else:
        await ctx.message.add_reaction('✅')
        await ctx.send(data['data']['embed_url'])

@gif.error
async def gif_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        param = {
            'api_key': 'api-key'
        }
        try:
            response = requests.request("GET", giphyURL, params = param)
            data = response.json()
        except Exception as e:
            print(e)
            return
        if data['meta']['status'] == 400:
            await ctx.message.add_reaction('❎')
            await ctx.send("Ya made a mistake somewhere, FIX IT!")
        elif data['meta']['status'] == 403:
            await ctx.message.add_reaction('❎')
            await ctx.send("Wow, GIPHY told me to fuck off.")
        elif data['meta']['status'] == 404:
            await ctx.message.add_reaction('❎')
            await ctx.send("Welp, ya got us. We could not find a GIF for that.")
        elif data['meta']['status'] == 429:
            await ctx.message.add_reaction('❎')
            await ctx.send("OI! You're requesting too fast, slow down.")
        else:
            await ctx.message.add_reaction('✅')
            await ctx.send(data['data']['embed_url'])


# Image Command
@client.command(aliases = ['img', 'i', 'photu'], pass_context = True)
async def image(ctx, *, query):
    query = str(query)
    flag = ""
    if ctx.message.channel.nsfw == False:
        querystring = {
            "q": query,
            "pageNumber":"1",
            "pageSize":"10",
            "autoCorrect":"true",
            "safeSearch":"true"
        }
        flag = "NSFW Off"
    else:
        querystring = {
            "q": query,
            "pageNumber":"1",
            "pageSize":"10",
            "autoCorrect":"true",
            "safeSearch":"false"
        }
        flag = "NSFW On"

    response = requests.request("GET", imageURL, headers=imageHeaders, params=querystring)
    data = response.json()
    count = len(data['value'])
    if(count == 0):
        await ctx.message.add_reaction('❎')
        await ctx.send("Welp, I was not able to get an image for that query!")
        return
    imageData =  data['value'][random.randint(0,count-1)]
    embed=discord.Embed(color = 0xffff00, title = "🖼", description = flag)
    embed.set_image(url= imageData['thumbnail'])
    embed.set_footer(text = f"{imageData['title']}", icon_url = client.user.avatar_url)
    await ctx.message.add_reaction('✅')
    await ctx.send(embed = embed)

# Image error
@image.error
async def image_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.add_reaction('❎')
        await ctx.send("Smh. Try again and this time, lemme know what to search for.")

client.run('bot-key')