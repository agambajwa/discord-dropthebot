import discord
from discord.ext import commands
import urllib3, json, random, requests, html
import http.client
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="bot")

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
chuckURL = "https://api.chucknorris.io/jokes"
insultURL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
oWeatherURL = "https://api.openweathermap.org/data/2.5/onecall"


headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "yo-key"
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
    statustxt = "Poopie v2.5 | .help"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)

# Help Command
@client.command()
async def help(ctx, *query):
    query = queryToStr(query)
    if query == '':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00, title = f"Yello! I am DropTheBot 🤗", description = "`Bot Prefix : .`")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "avatar <user>", value = "Returns the avatar of the 'user' you mention or your own, for... whatever reasons. 👀", inline = True)
        embed.add_field(name = "define [word]", value = "Returns the Urban Dictionary definiton.", inline = True)
        embed.add_field(name = "ping", value = "Returns pong.", inline = True)
        embed.add_field(name = "covid", value = "Returns COVID-19 Data for India or states.", inline = True)
        embed.add_field(name = "chucknorris", value = "Returns random Chuck Norris fact.", inline=True)
        embed.add_field(name = "insult", value = "Sends a random insult, use wisely.", inline=True)
        embed.add_field(name = "weather [place]", value = "Returns weather info.", inline=True)
        embed.set_footer(text = f".help [command] for more info on a command | {client.user.name}", icon_url = client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'insult':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"insult", description = "`Aliases : roast`")
        embed.add_field(name = "insult", value = "Sends a random insult, bitch.", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'avatar':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"avatar", description = "`Aliases : av, a`")
        embed.add_field(name = "avatar", value = "Returns your avatar. 👀", inline = True)
        embed.add_field(name = "avatar [user]", value = "Returns the avatar of the 'user' you mention. 👀", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'ping':
        await ctx.message.add_reaction('🏓')
        await ctx.send("https://tenor.com/view/cats-ping-pong-gif-8942945")
    elif query == 'covid':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"covid", description = "")
        embed.add_field(name = "covid", value = "Returns COVID-19 Data for India.", inline = True)
        embed.add_field(name = "covid [state]", value = "Returns COVID-19 Data for the 'state' (or UT) you mention.", inline = True)
        embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'define':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"define", description = "`Aliases : def, df, ud, urban`")
        embed.add_field(name = "define [word]", value = "Returns the Urban Dictionary definiton of the 'word' you mentioned.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'chucknorris':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"chucknorris", description = "`Aliases : norris, cn, chuck`")
        embed.add_field(name = "chucknorris", value = "Returns random Chuck Norris fact.", inline = True)
        embed.add_field(name = "chucknorris categories", value = "Returns available categories.", inline = True)
        embed.add_field(name = "chucknorris [category]", value = "Returns random Chuck Norris fact for the 'category' you mentioned.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.send(embed = embed)
    elif query == 'weather':
        await ctx.message.add_reaction('✅')
        embed=discord.Embed(color = 0xffff00,title = f"weather", description = "`Aliases : w, mausam`")
        embed.add_field(name = "weather [place]", value = "Returns weather info for the 'place' you mention.", inline = True)
        embed.set_footer(text = f"{client.user.name}", icon_url = client.user.avatar_url)
        await ctx.send(embed = embed)
    else: 
        await ctx.message.add_reaction('❎')
        await ctx.send("I can only help with things that I can do, for other things, help yourself 🙃")


# Fun auto responses
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().find('who') != -1 and message.content.endswith('?'):
        await message.channel.send('ur mom')
        return
    return

client.add_listener(on_message, 'on_message')


# Insult command
@client.command(aliases = ['roast'], pass_context = True)
async def insult(ctx):
    try:
        response = requests.request("GET", insultURL)
    except:
        await ctx.message.add_reaction('😫')
        await ctx.send('The god damn API failed me!')
        return

    await ctx.message.add_reaction('✅')
    data = response.json()
    await ctx.send(html.unescape(data['insult']))


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
@client.command(aliases = ['def', 'df', 'ud', 'urban'], pass_context = True)
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
async def avatar(ctx, member: discord.Member = None):
    
    if(member == None):
        await ctx.message.add_reaction('🤦‍♂️')
        embed = discord.Embed(title="🤦‍♂️",description=f"Uh, okay, look at yourself, you narcissistic human.", colour=discord.Colour(0xffff00))
        embed.set_image(url=ctx.message.author.avatar_url)
    else:
        try:
            await ctx.message.add_reaction('👀')
            embed = discord.Embed(title="👀",description=f"Here is {member.mention}'s avatar, ya damn stalker", colour=discord.Colour(0xffff00))
            embed.set_image(url = member.avatar_url)
        except:
            await ctx.message.add_reaction('🤬')
            embed = discord.Embed(title="🤬",description=f"Dumb fookin error occurred!", colour=discord.Colour(0xffff00))
    embed.set_footer(text=f"Requested by {ctx.message.author.name} | {client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed = embed)


# Chuck Norris Command
@client.command(aliases = ['norris', 'cn', 'chuck'], pass_context = True)
async def chucknorris(ctx, *Query):
    query  = queryToStr(Query)
    if query  == '':
        try:
            response = requests.get(chuckURL+"/random")
            data = response.json()
            await ctx.message.add_reaction('✅')

            embed = discord.Embed(title = f"**Chuck Norris Fact**", description = f"{data['value']}", color = 0xffff00)
            embed.set_thumbnail(url = data['icon_url'])
            embed.set_footer(text=f"Totally legitmate, 100% true and trustworthy, completely reliable and truthful. Don't @ me though, I am a bot, won't respond anyway.")
            await ctx.send(embed = embed)

        except:
            await ctx.message.add_reaction('😭')
            await ctx.send("Welp, an error occurred, try again or go cry to your mommy.")
    else:
        try:
            response = requests.get(chuckURL+"/categories")
            categories = response.json()
        except:
            await ctx.message.add_reaction('😭')
            await ctx.send("Welp, an error occurred, try again or go cry to your mommy.")
            return
        
        if query == 'categories':
            await ctx.message.add_reaction('✅')
            
            string = ""
            for ele in categories:
                string = string + ele.upper() + '\n'
            embed = discord.Embed(title = f"**Chuck Norris Facts Categories**", description = f"**Available categories:** \n {string}", color = 0xffff00)
            await ctx.send(embed = embed)

        elif query in categories:
            if query == 'explicit' and ctx.message.channel.nsfw==False:
                await ctx.message.add_reaction('⁉')
                await ctx.send("Wait a minute, this ain't a NSFW channel! Feck off!")
    
            else:
                response = requests.get(chuckURL+"/random?category="+query)
                data = response.json()
                await ctx.message.add_reaction('✅')

                embed = discord.Embed(title = f"**Chuck Norris Fact**", description = f"**{query.upper()}** : {data['value']}", color = 0xffff00)
                embed.set_thumbnail(url = data['icon_url'])
                embed.set_footer(text=f"Totally legitmate, 100% true and trustworthy, completely reliable and truthful. Don't @ me though, I am a bot, won't respond anyway.")
                await ctx.send(embed = embed)

        else:
            await ctx.message.add_reaction('⁉')
            await ctx.send("I literally have a command to check the available categories, still you send dumb shit to me!")


# Weather Command
@client.command(aliases = ['w', 'mausam'], pass_context = True) 
async def weather(ctx, *Query):
    query = queryToStr(Query)
    if(query == ""):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Umm, share a location too next time, thanks.")
        return
    location = geolocator.geocode(query)
    if(location == None):
        await ctx.message.add_reaction('🤬')
        await ctx.send("Could not find the location you mentioned, learn some Geography I guess.")
        return
    try:
        response = requests.get(oWeatherURL + '?lat=' + str(location.latitude) + '&lon=' + str(location.longitude) + '&appid=yo-key&units=metric&exclude=minutely,hourly,alerts,daily')
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

client.run('bot-key')