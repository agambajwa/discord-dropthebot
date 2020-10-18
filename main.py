import discord
import urllib3, json, random
import codecs
import http.client

connection = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "your api key from rapidapi"
    }

client = discord.Client()
owner = client.get_user(int("375638836245561344"))

async def sendHelp(message):
    await message.add_reaction('✅')
    embed=discord.Embed(color=0xffff00,description=f"Yello! I am DropTheBot :D")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/758950626297249812/75ce3685f04a7acb1d27a7e8472c4922.jpg?size=1024")
    embed.add_field(name = "List of commands that I listen to", value = "This is still being populated", inline = False)
    embed.add_field(name = "dtb avatar", value = "Returns the avatar of the user you mention or leave it empty to get your own, ya damn stalker.", inline = True)
    embed.add_field(name = "dtb def word", value = "Returns the Urban Dictionary definiton of the 'word' you mentioned.", inline = True)
    embed.add_field(name = "dtb ping", value = "Returns pong.", inline = True)
    embed.add_field(name = "dtb covid", value = "Returns COVID-19 Data for India, ``dtb covid help`` for more info. [Coming Soon].", inline = True)
    embed.set_footer(text=f"{client.user.name} - By agummybear#8008", icon_url=client.user.avatar_url)
    await message.channel.send(embed = embed)
    return

async def sendAvatar(message):
    person = str(message.content)[14:-1]
    try:    
        mentionedUser = client.get_user(int(person))
        await message.add_reaction('👀')
        embed = discord.Embed(title=" ",description=f"Here is {mentionedUser.mention}'s avatar, ya damn stalker", colour=discord.Colour(0xffff00))
        embed.set_image(url=mentionedUser.avatar_url)
    except ValueError:
        await message.add_reaction('🤦‍♂️')
        embed = discord.Embed(title=" ",description=f"Uh, okay, look at yourself, you narcissistic human.", colour=discord.Colour(0xffff00))
        embed.set_image(url=message.author.avatar_url)
          
    embed.set_footer(text=f"{client.user.name} - By agummybear#8008", icon_url=client.user.avatar_url)
    await message.channel.send(embed=embed)
    return

async def sendDefinition(message):
    if(random.randint(0,10) == 6):
        await message.add_reaction('😝') 
        await message.channel.send('https://tenor.com/view/golmaal3-johnny-lever-pappi-bhai-mai-nahi-bataunga-mein-nahi-bataunga-gif-17855218')
        return
    word = str(message.content)[8:]
    try:
        connection.request("GET", "/define?term=" + word, headers=headers) 
        response = connection.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        first = data['list'][0]

        await message.add_reaction('✅')
        await message.channel.send('**Definition - **' + first['definition'])
        await message.channel.send('**Example - **_' + first['example'] + "_")
        await message.channel.send('**' + str(first['thumbs_up']) + "** people have liked this shit.")
        if(len(data['list'])-1 > 0):
            await message.channel.send("There were **" + str(len(data['list']) - 1) + "** other definition(s), go look 'em up yourself!")
    except:
        await message.add_reaction('❎')
        await message.channel.send("Either there is no definition for that word, or some error occurred. Anyway, I couldn't care less ¯\_(ツ)_/¯")
    return

async def sendCovidHelp(message):
    await message.add_reaction('✅')
    embed=discord.Embed(color=0xffff00,description=f"dtb covid help")
    embed.add_field(name = "Coming Soon", value = "...", inline = False)
    embed.set_footer(text=f"{client.user.name} - By agummybear#8008", icon_url=client.user.avatar_url)
    await message.channel.send(embed = embed)
    return

async def sendCovidData(message):
    await message.channel.send("Coming soon!")
    return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    statustxt = 'Poopie | dtb help'
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # help command
    if message.content.startswith('dtb help'):
        await sendHelp(message = message)
        return
        
    # avatar command
    if message.content.startswith('dtb avatar'):
        if message.channel.name == 'covid-19':
            return
        await sendAvatar(message = message)
        return
            
    # random
    if message.content.startswith('dtb ping'):
        if message.channel.name == 'covid-19':
            return
        await message.channel.send('Pong! ||What did you expect?||')
        return

    # urban dict definitons
    if message.content.startswith('dtb def'):
        if message.channel.name == 'covid-19':
            return
        await sendDefinition(message = message)
        return     

    # covid-19
    if message.content.startswith('dtb covid help'):
        await sendCovidHelp(message = message)
        return   

    if message.content.startswith('dtb covid'):
        await sendCovidData(message = message)
        return

client.run('Your Token Here')