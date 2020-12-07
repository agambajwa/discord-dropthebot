import discord
from discord.ext import commands
import urllib3, json, random
import http.client
import datetime

client = discord.Client()
client = commands.Bot(command_prefix='.')
htt = urllib3.PoolManager()
owner = client.get_user(int("375638836245561344"))
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

connectionDef = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")
connectionCovid = http.client.HTTPSConnection("api.covid19india.org")

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "your-rapid-api-key"
    }

client.remove_command('help')

def queryToUrlStr(query):
    string = ""
    for e in query:
        string = string + e + "%20"
    string = string[:-3]
    return string

def queryToStr(query):
    string = ""
    for e in query:
        string = string + " " + e
    return string.lower().strip()

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
    
    await ctx.message.add_reaction('✅')

    # Frustrating checks
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

    embed = discord.Embed(title = f"**COVID-19 Data for India**", description = f"Updated on {sendTime(str(data['TT']['meta']['last_updated']))}", color = 0xffff00)
    embed.add_field(name = "Confirmed", value = str(data['TT']['total']['confirmed']) + " " + deltaConf, inline = False)
    embed.add_field(name = "Deceased", value = str(data['TT']['total']['deceased']) + " " + deltaDec, inline = False)
    embed.add_field(name = "Recovered", value = str(data['TT']['total']['recovered']) + " " + deltaRec, inline = False)
    embed.add_field(name = "Tested", value = str(data['TT']['total']['tested']) + " - _As on " + str(data['TT']['meta']['tested']['last_updated']) + "_", inline = False)

    embed.set_footer(text=f"Data by api.covid19india.org - DropTheBot")
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
    print('We have logged in as {0.user}'.format(client))
    statustxt = "Poopie v2.1 | .help"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)

# Help Command
@client.command()
async def help(ctx, *query):
    query = queryToStr(query)
    if query == '':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00, title = f"Yello! I am DropTheBot 🤗", description = "Bot Prefix : .")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "avatar / av", value = "Returns the avatar of the user you mention or your own, for... whatever reasons. 👀", inline = True)
        embed.add_field(name = "df word", value = "Returns the Urban Dictionary definiton of the 'word' you mentioned.", inline = True)
        embed.add_field(name = "ping", value = "Returns pong.", inline = True)
        embed.add_field(name = "covid", value = "Returns COVID-19 Data for India, ``.help covid`` for more info.", inline = True)
        embed.set_footer(text = f"{client.user.name} - By agummybear#8008", icon_url = client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'covid':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"covid help", description = "Bot Prefix : .")
        embed.add_field(name = "covid", value = "Returns COVID-19 Data for India.", inline = True)
        embed.add_field(name = "covid state", value = "Returns COVID-19 Data for the 'state'(or UT) you mention.", inline = True)
        embed.add_field(name = "Example", value = "``.covid delhi``", inline = False)
        embed.set_footer(text=f"{client.user.name} - By agummybear#8008", icon_url=client.user.avatar_url)
        await ctx.send(embed = embed)
    else: 
        await ctx.message.add_reaction('❎')
        await ctx.send("I can only help with things that I can do, for other things, help yourself 🙃")


# Random ping command
@client.command()
async def ping(ctx):
    await ctx.message.add_reaction('🏓')
    await ctx.send('Pong! ' + str(round(client.latency * 1000.0, 1)) + ' ms')


# COVID Command
@client.command()
async def covid(ctx, *state):
    state = queryToStr(state)
    if state == '':
        await sendIndianCovidData(ctx = ctx)
    else:
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


# UD Definition Command
@client.command(aliases = ['def', 'df'], pass_context = True)
async def define(ctx, *Query):
    if(random.randint(0,10) == 6):
        await ctx.message.add_reaction('😝') 
        await ctx.send('https://tenor.com/view/golmaal3-johnny-lever-pappi-bhai-mai-nahi-bataunga-mein-nahi-bataunga-gif-17855218')
        return
    word = queryToUrlStr(Query)
    if word == '':
        await ctx.message.add_reaction('⁉')
        await ctx.send("I need a damn word to look up, how bout you try again?")
        return 
    try:
        connectionDef.request("GET", "/define?term=" + word, headers=headers) 
        response = connectionDef.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        first = data['list'][0]

        await ctx.message.add_reaction('✅')
        await ctx.send('**Definition for - **' + first['definition'])
        await ctx.send('**Example - **_' + first['example'] + "_")
        await ctx.send('**' + str(first['thumbs_up']) + "** people have liked this shit.")
        if(len(data['list'])-1 > 0):
            await ctx.send("There were **" + str(len(data['list']) - 1) + "** other definition(s), go look 'em up yourself!")
    except:
        await ctx.message.add_reaction('❎')
        await ctx.send("Either there is no definition for the word, or some error occurred. Anyway, I couldn't care less ¯\_(ツ)_/¯")


# Avatar Command
@client.command(aliases = ['av', 'a'], pass_context = True)
async def avatar(ctx, username=None):
    if(username == None):
        await ctx.message.add_reaction('🤦‍♂️')
        embed = discord.Embed(title="🤦‍♂️",description=f"Uh, okay, look at yourself, you narcissistic human.", colour=discord.Colour(0xffff00))
        embed.set_image(url=ctx.message.author.avatar_url)
    else:
        try:
            mentionedUser = client.get_user(int(str(username)[3:-1]))
        except:
            await ctx.message.add_reaction('❎')
            await ctx.send("Beep boop, user not found or you made a dumb mistake. Try again, boop beep.")
            return
        await ctx.message.add_reaction('👀')
        embed = discord.Embed(title="👀",description=f"Here is {mentionedUser.mention}'s avatar, ya damn stalker", colour=discord.Colour(0xffff00))
        embed.set_image(url = mentionedUser.avatar_url)
        
    embed.set_footer(text=f"{client.user.name} - By agummybear#8008", icon_url=client.user.avatar_url)
    await ctx.send(embed = embed)


client.run('your-discord-bot-token')