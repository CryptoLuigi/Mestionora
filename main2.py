import cooldowns, random , nextcord, sqlite3, calendar, os
from enum import Enum
from nextcord import Intents, Interaction
from nextcord.ext import commands, application_checks
from cooldowns import CallableOnCooldown, Cooldown
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

intents = Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='!', help_command=None, intents=intents)

ServerID = 883777134282293258
ServerID2 = 630606651992309760
ChannelID = 1028869157841797180
ChannelID2 = 630606651992309763
welcomechannel = f'<#630606999050125316>'
introchannel  = f'<#721199596084396063>'
botchannel = f'<#638020706935767100>'
rolechannel = f'<#637097683030638624>'

reaction1 = '👋'
reaction2 = '🙂'
reaction3 = '📖'
reaction4 = "<:praisekami:946117405111898192>"
reaction5 = '☄️'
reaction6 = '💢'
reaction7 = '<:MyneMad:1028864874526294057>'
reaction8 = '💿'
reaction9 = '<:Schwartz:1011313391660453969>'
reaction10 = '<:Weiss:1011313394890055711>'
reaction11 = '<:MynePuhi:895244115237826580>'
reaction12 = '<:Lessy:904422684266483712>'
reaction13 = '<:Benno_lol:1035766132281446464>'
reaction14 = '<:MyneSparkle:1018941182430154902>'
reaction15 = '<:MyneBliss:696155170333130782>'
reaction16 = '<:MyneRofl:729576361492086884>'
reaction17 = '🤓'
reaction18 = '<:RzOhDear:1037385011499896964>'

conn = sqlite3.connect('db_tags.db')
c = conn.cursor()

def fail():
    1/0

@client.message_command(name="Convert to fxtwitter")
async def conv_fxtwitter(interaction: nextcord.Interaction, message: nextcord.Message):
    msg = message.content
    x = msg.find("https://twitter.com/")
    if x == -1:
        await interaction.response.send_message("Nothing to convert", ephemeral=True)
    else:
        msg = msg.replace("https://twitter.com/","https://fxtwitter.com/")
        await interaction.response.send_message(f"{msg}", ephemeral=True)

@client.slash_command(description="Fetch the list of bots on the server.")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def list_bots(interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        guild = nextcord.utils.find(lambda g: g.id == interaction.guild.id, client.guilds)
        role = nextcord.utils.get(guild.roles, name="Bots")
        members = role.members
        contentmsg = "This is the list of bots in the *Ascendance of a Bookworm* discord server:\n\n"
        for member in members:
            if member.mention != "<@420692327019839504>": #ignore the server owner
                contentmsg += f"• {member.mention}\n"

        embed=nextcord.Embed(title="Bots", description=f"{contentmsg}",color=0xf1c40f)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png")
        await interaction.response.send_message(embed=embed)
        print(f"{interaction.user} requested the bot list")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# Hello Command
@client.slash_command(description="Say hello to the Goddess")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def hello(interaction : Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")
    elif current_channel == f'bot-development':
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# On message on member join
@client.event
async def on_member_join(member):

    servercheck = client.get_guild(member.guild.id)

    channel = client.get_channel(ChannelID)
    allowedserver = client.get_guild(ServerID)
    if f'{servercheck}' == f'{allowedserver}':
        embed=nextcord.Embed(title=f"Welcome!", description=f"{member.mention}, welcome to Chibi's Library 📚.\nCheck out <#1029192039293792377> to get roles.", type="image",color=0xf1c40f)
        embed.set_image("https://cdn.discordapp.com/attachments/946041447348596747/1029832048522821723/image.png?size=4096")
        await channel.send(embed=embed)

#    channel = client.get_channel(ChannelID2)
#    allowedserver = client.get_guild(ServerID2)
#    if f'{servercheck}' == f'{allowedserver}':
#        embed=nextcord.Embed(title="Welcome!",description=f"{member.mention} welcome to **Ascendance of a Bookworm!** Be sure to check our {welcomechannel}! Feel free to introduce yourself in {introchannel} and get a role in {rolechannel} <:MyneSparkle:1018941182430154902>",color=0xf1c40f)
#        await channel.send(embed=embed)


# Start up message
@client.event
async def on_ready():
    print('Mestionora lives'.format(client))
    d = datetime.today()
    w = calendar.day_name[d.weekday()]
    print('Mestionora wishes you a happy ', w)

# Cooldown error message
@client.event
async def on_application_command_error(inter: nextcord.Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await inter.send(ephemeral=True, content=f"You are being rate-limited! Retry in `{error.retry_after}` seconds.")
    elif isinstance(error, application_checks):
        await inter.send(ephemeral=True, content=f"You do not have permission to do that.")           
    else:
        raise error

# gif command, shows entry from database Usage: +gif
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def gif(interaction : Interaction, id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        if id_num == None:
            value = random.randint(1,75) 
            c.execute(f"SELECT gif from gif_table where id = '{value}'")
            print('Mestionora fetches from the db'.format(client))
            bless = f"{c.fetchone()}"
            bless = bless.lstrip("(\'")
            bless = bless.rstrip("\',)")
            await interaction.send(bless)
        else:
            c.execute(f"SELECT gif from gif_table where id = '{id_num}'")
            quote = f'{c.fetchone()}'
            quote = quote.lstrip("(\'")
            quote = quote.rstrip("\',)")    
            await interaction.send(quote)
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# bless command, shows entry from database Usage: +bless
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def bless(interaction : Interaction, id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        if id_num == None:
            value = random.randint(1,46) 
            c.execute(f"SELECT LINE from QUOTES where ID = '{value}'")
            print('Mestionora fetches from the db'.format(client))
            bless = f"{c.fetchone()}"
            bless = bless.lstrip("(\'")
            bless = bless.rstrip("\',)")
            await interaction.send(bless)
        else:
            c.execute(f"SELECT LINE from QUOTES where ID = '{id_num}'")
            quote = f'{c.fetchone()}'
            quote = quote.lstrip("(\'")
            quote = quote.rstrip("\',)")    
            await interaction.send(quote)
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")
        
# Tag command, added entry to database Usage: +tag <name> <link>
@client.slash_command(description="Create a tag with text or a link")
async def tag(interaction : Interaction, name:str, text:str):
    #name = name.lower
    c.execute(f"SELECT NAME from tags where NAME = '{name}'")
    name_check = c.fetchone()
    if name_check == None:
        sql = f"INSERT INTO tags (NAME, LINK, ID) VALUES (?, ?, ?)"
        val = (name, text, interaction.user.id)
        c.execute(sql, val)
        conn.commit()
        print('Mestionora added to the db'.format(client))
        await interaction.response.send_message(ephemeral=True, content=f"Tag added {interaction.user.mention}!")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"Tag already exists {interaction.user.mention}!")         

# Show command, shows entry from database Usage: +show <name>
@client.slash_command(description="Shows a stored tag")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def show(interaction : Interaction, name:str):
    #name = name.lower
    try:
        c.execute(f"SELECT LINK from tags where NAME = '{name}'")
        print('Mestionora fetches from the db'.format(client))
        show = f"{c.fetchone()}"
        print(show)
        if show == "None":
            fail()
        else:
            show = show.lstrip("(\'")
            show = show.rstrip("\',)")
            await interaction.send(show)
    except:
        c.execute(f"SELECT gif from gif_table where NAME = '{name}'")
        print('Mestionora fetches from the db'.format(client))
        show = f"{c.fetchone()}"
        print(f'show in gif{show}')
        if show == "None":
            await interaction.send(ephemeral=True, content=f"That tag does not exist.")
        else:
            show = show.lstrip("(\'")
            show = show.rstrip("\',)")
            await interaction.send(show)

# Admin remove command Usage: +superrm <name>
@client.slash_command(description="Admin command to remove tags")
@application_checks.has_any_role("Aub","Zent","Giebe")
async def superrm(interaction : Interaction, name:str):
    c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}'")
    await interaction.response.send_message(ephemeral=True, content=f"Tag deleted {interaction.user.mention}!")   
    print('Mestionora deleted from the db'.format(client))

# Admin edit command Usage: +sedit <name> <link>
@client.slash_command(description="Admin command to edit tags")
@application_checks.has_any_role("Aub","Zent","Giebe")
async def sedit(interaction : Interaction, name:str, text:str):
    c.execute(f"UPDATE tags SET LINK = '{name}' WHERE NAME = '{text}'")
    await interaction.response.send_message(ephemeral=True, content=f"Tag updated {interaction.user.mention}!")   
    print('Mestionora edited the db'.format(client))

# Edit entry from tag database Usage: +edit <name> <link>
@client.slash_command(description="Edit a tag")
async def edit(interaction : Interaction, name:str, text:str):
    c.execute(f"UPDATE tags SET LINK = '{text}' WHERE NAME = '{name}' AND ID = '{interaction.user.id}'")
    await interaction.response.send_message(ephemeral=True, content=f"Tag updated {interaction.user.mention}!")   
    print('Mestionora edited the db'.format(client))

# remove entry from tag databae Usage: +rm <name>
@client.slash_command(description="Remove a tag")
async def rm(interaction : Interaction, name:str):
    c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}' AND ID = '{interaction.user.id}'")
    await interaction.response.send_message(ephemeral=True, content=f"Tag removed {interaction.user.mention}!")   

# Praise command
@client.slash_command(description="Praise be to the Gods!")
@cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
async def praise(interaction : Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        await interaction.send(f"Blessings upon {interaction.user.mention}!")      
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")      

class CooldownBucket(Enum):
    message_author = 1
    def process(self, *args, **kwargs):
        return args[0].author.id

cooldown = Cooldown(1, 15, CooldownBucket.message_author)

@client.event
async def on_raw_reaction_add(payload):

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)

    if message.author == client.user:
        return  

    if payload.emoji.name=="MyneRofl":
        value = random.randint(1,300)
        if value == 1:
            await message.add_reaction(reaction16)
            print('Mestionora added a reaction'.format(client))   

# Random quote generator       
@client.event
async def on_message(message):
    banchannel = f"bots"
    if message.author == client.user:
        return
    
    print(f"{message.channel}")

    if (f"{message.channel}") != banchannel:
        return

    if 'praise be to the gods' in message.content.lower():
        try:
            async with cooldown(message):
                await message.channel.send('Blessings upon ' + str(message.author.mention))       
                value = random.randint(1,8)
                if value == 1:
                    await message.channel.send('https://cdn.discordapp.com/attachments/1027597999091753010/1028786413455552583/unknown.png')
                if value == 2:
                    await message.channel.send('https://cdn.discordapp.com/attachments/883777134911422466/1028791311807037510/LN_P4V3-2.jpg')
                if value == 3:
                    await message.channel.send('https://media.discordapp.net/attachments/883777134911422466/1028793143652536320/Screenshot_20221009-151607_Google_Play_Books.jpg')
                if value == 4:
                    await message.channel.send('https://cdn.discordapp.com/attachments/883777134911422466/1028794786569797775/LN_P1V3-Insert.jpg')
                if value == 5:
                    await message.channel.send('https://cdn.discordapp.com/attachments/883777134911422466/1028795750999674880/LN_P2V2-7.jpg')
                if value == 6:
                    await message.channel.send('https://cdn.discordapp.com/attachments/1027597999091753010/1028855796731232296/unknown.png')
                if value == 7:
                    await message.channel.send('https://media.discordapp.net/attachments/1029782845071294595/1030838261184208947/LN_P4V4-Insert.jpg?width=993&height=775')
                if value == 8:
                    await message.channel.send('https://media.discordapp.net/attachments/1029782845071294595/1030838628710088785/11.jpg')

        except cooldowns.CallableOnCooldown:
            print(f'cooldown')

    if 'mestionora, bless' in message.content.lower():
        try:               
            async with cooldown(message):                
                value = random.randint(1,46) 
                c.execute(f"SELECT LINE from quotes where ID = '{value}'")
                print('Mestionora fetches quote from the db'.format(client))
                bless = f"{c.fetchone()}"
                bless = bless.lstrip("(\'")
                bless = bless.rstrip("\',)")
                await message.channel.send(bless)
        except cooldowns.CallableOnCooldown:
            print(f'cooldown')
    
    await client.process_commands(message) 

# Help command
@client.slash_command(description="Get help from Mestionora")
async def help_mestionora(interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        scommands='''
        </bless:0> - Receive a divine blessing and a *quote*. Optional: `id_num` - Pulls out a *quote*.
        `id_num` = The quote's identification number.

        </edit:0> `name` `text` - Allows edition an existing tag (as long as the tag has been created by you).
        `name` = The name of the tag you want to edit.
        `text` = Content you want to store in the tag.

        </hello:0> - Say hello to Mestionora :slight_smile:.

        </praise:0> - Praise be to the gods!

        </rm:0> `name` - Allows removal an existing tag (as long as the tag has been created by you).
        `name` = The name of the tag you want to remove.

        </show:0> `name` - Allows to display an existing tag.
        `name` = The name of the tag you want to display.

        </tag:0> `name` `text` - Allows creation of a new tag.
        `name` = The name of the tag you want to create.
        `text` = Content you want to store in the tag.
        '''

        acommands='''
        </sedit:0> `name` `text` - Allows edition of any existing tag (regardless of the creator).
        `name` = The name of the tag you want to edit.
        `text` = Content you want to store in the tag.

        </superrm:0> `name` - Allows removal of any existing tag (regardless of the creator).
        `name` = The name of the tag you want to remove.
        '''

        embed=nextcord.Embed(title="Help", description="This is the list of commands for <@1027592830719377439>.",color=0xf1c40f)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png")
        embed.add_field(name="Slash Commands:", value=f"{scommands}", inline=False)
        embed.add_field(name="Admin/Mod Slash Commands:", value=f"{acommands}", inline=False)

        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

client.run(os.getenv("TOKEN"))