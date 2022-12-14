import cooldowns, random , nextcord, sqlite3, calendar, os
from enum import Enum
from nextcord import Intents, Interaction, Member, Embed, Message, ButtonStyle
from nextcord.ext import application_checks, commands
from cooldowns import CallableOnCooldown, Cooldown, SlashBucket
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from utils import TagModal, get_page_giflist, get_page_taglist

load_dotenv()

conn = sqlite3.connect('db_tags.db')
c = conn.cursor()

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

@client.message_command(name="Convert to fxtwitter")
async def conv_fxtwitter(interaction: Interaction, message: Message):
    msg = message.content
    x = msg.find("https://twitter.com/")
    if x == -1:
        await interaction.response.send_message("Nothing to convert", ephemeral=True)
    else:
        msg = msg.replace("https://twitter.com/","https://fxtwitter.com/")
        await interaction.response.send_message(f"{msg}", ephemeral=True)

@client.slash_command(description="Fetch the list of bots on the server.")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
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
        await interaction.response.send_message(contentmsg)
        print(f"{interaction.user} requested the bot list")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# Hello Command
@client.slash_command(description="Say hello to the Goddess")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
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
        embed=Embed(title=f"Welcome!", description=f"{member.mention}, welcome to Chibi's Library 📚.\nCheck out <#1029192039293792377> to get roles.", type="image",color=0xf1c40f)
        embed.set_image("https://cdn.discordapp.com/attachments/946041447348596747/1029832048522821723/image.png?size=4096")
        await channel.send(embed=embed)
        bookwormrole = nextcord.utils.get(servercheck.roles, name="Bookworms 📚")
        await member.add_roles(bookwormrole)

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
    print('Mestionora wishes you a happy', w)

# error message
@client.event
async def on_application_command_error(inter: Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await inter.send(ephemeral=True, content=f"You are being rate-limited! Retry in `{error.retry_after}` seconds.")
    elif isinstance(error, application_checks.ApplicationMissingAnyRole):
        await inter.send(ephemeral=True, content=f"You don't have permission to do that.")
    elif isinstance(error, sqlite3.OperationalError):
        await inter.send(f"⚠There was an error with the sqlite database.⚠\n ```{error}```")
        raise error
    elif isinstance(error, AttributeError):
        await inter.send(f"⚠There was an attribute error.⚠\n ```{error}```")
        raise error
    elif isinstance(error, NameError):
        await inter.send(f"⚠There was an name error.⚠\n ```{error}```")
        raise error
    else:
        raise error

# gif command, shows entry from database Usage: /gif
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def gif(interaction : Interaction, name: Optional[str], id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        if id_num == None and name == None:
            value = random.randint(1,76) 
            c.execute(f"SELECT gif from gif_table where id = '{value}'")
            print('Mestionora fetches from the db'.format(client))
            bless = c.fetchone()
            await interaction.send(bless[0])
        elif id_num != None and name == None:
            c.execute(f"SELECT gif from gif_table where id = '{id_num}'")
            quote = c.fetchone()  
            await interaction.send(quote[0])
        elif id_num == None and name != None:
            c.execute(f"SELECT gif from gif_table where name = '{name}'")
            quote = c.fetchone()   
            await interaction.send(quote[0])
        elif id_num != None and name != None:
            await interaction.send("You cannot use the gif name and gif id simultaneously.", ephemeral=True)
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# bless command, shows entry from database Usage: /bless
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def bless(interaction : Interaction, id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f'bots' or current_channel ==f'🐍-bots':
        if id_num == None:
            value = random.randint(1,46) 
            c.execute(f"SELECT LINE from QUOTES where ID = '{value}'")
            print('Mestionora fetches from the db'.format(client))
            bless = c.fetchone()
            await interaction.send(bless[0])
        else:
            c.execute(f"SELECT LINE from QUOTES where ID = '{id_num}'")
            quote = c.fetchone() 
            await interaction.send(quote[0])
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

# Tag command, added entry to database Usage: /tag <name> <text>
@client.slash_command(description="Create a tag with text or a link")
async def tag(interaction : Interaction):
    msg = ""
    tagn = ""
    await interaction.response.send_modal(TagModal("create",msg,tagn))

@client.message_command(name="Create tag")
async def tag_from_msg(interaction: Interaction, message: Message):
    msg = message.content
    tagn = ""
    await interaction.response.send_modal(TagModal("create",msg,tagn))        

# Show command, shows entry from database Usage: /show <name>
@client.slash_command(description="Shows a stored tag")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def show(interaction : Interaction, name:str):
    c.execute(f"SELECT LINK from tags where NAME = '{name}'")
    print('Mestionora fetches from the db'.format(client))
    show = c.fetchone()
    if show[0] == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        await interaction.send(show[0])

# Admin remove command Usage: /superrm <name>
@client.slash_command(description="Admin command to remove tags")
@application_checks.has_any_role("Aub","Zent","Giebe","Discord admin","Discord Mods","staff")
async def superrm(interaction : Interaction, name:str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        confirm_delete1 = nextcord.ui.Button(label="Yes", style=ButtonStyle.red)

        async def confirm_callback1(interaction:Interaction):
            c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}'")
            await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" has been removed.") 
            print('Mestionora deleted from the db'.format(client))

        confirm_delete1.callback = confirm_callback1

        view = nextcord.ui.View(timeout=180)
        view.add_item(confirm_delete1)

        embed=Embed(title="Confirm removal", description=f"Are you sure you want to remove tag \"{name}\"?",color=0xf1c40f)

        await interaction.response.send_message(ephemeral=True, embed=embed, view=view)

# Admin edit command Usage: /sedit <name> <text>
@client.slash_command(description="Admin command to edit tags")
@application_checks.has_any_role("Aub","Zent","Giebe","Discord admin","Discord Mods","staff")
async def sedit(interaction : Interaction, name:str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        c.execute(f"SELECT NAME from tags where NAME = '{name}'")
        tagn = c.fetchone()
        c.execute(f"SELECT LINK from tags where NAME = '{name}'")
        msg = c.fetchone()
        msg = msg.replace("\\n","\n")
        await interaction.response.send_modal(TagModal("edit",msg[0],tagn[0]))

# Change user id in database: /sgive <name> <member>
@client.slash_command(description="Admin command to give tags")
@application_checks.has_any_role("Aub","Zent","Giebe","Discord admin","Discord Mods","staff")
async def sgive(interaction : Interaction, name:str, member:Member):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        c.execute(f"UPDATE tags SET ID = '{member.id}' WHERE NAME = '{name}'")
        conn.commit()
        print('Mestionora changed tag owner in the db'.format(client))
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" has been given to <@{member.id}>.")

# Change user id in database: /give <name> <member>
@client.slash_command(description="Give a tag")
async def give(interaction : Interaction, name:str, member:Member):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        c.execute(f"UPDATE tags SET ID = '{member.id}' WHERE NAME = '{name}'")
        conn.commit()
        print('Mestionora changed tag owner in the db'.format(client))
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" has been given to <@{member.id}>.")
    elif user_check == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" is created by someone else.")

# Edit entry from tag database Usage: /edit <name>
@client.slash_command(description="Edit a tag")
async def edit(interaction : Interaction, name:str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        c.execute(f"SELECT NAME from tags where NAME = '{name}'")
        tagn = c.fetchone()
        c.execute(f"SELECT LINK from tags where NAME = '{name}'")
        msg = c.fetchone()
        msg = msg.replace("\\n","\n")
        await interaction.response.send_modal(TagModal("edit",msg[0],tagn))
    elif user_check == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" is created by someone else.")

@client.slash_command(description="Remove a tag")
async def rm(interaction : Interaction, name:str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        confirm_delete1 = nextcord.ui.Button(label="Yes", style=ButtonStyle.red)

        async def confirm_callback1(interaction:Interaction):
            c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}'")
            await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" has been removed.") 
            print('Mestionora deleted from the db'.format(client))

        confirm_delete1.callback = confirm_callback1

        view = nextcord.ui.View(timeout=180)
        view.add_item(confirm_delete1)

        embed=Embed(title="Confirm removal", description=f"Are you sure you want to remove tag \"{name}\"?",color=0xf1c40f)

        await interaction.response.send_message(ephemeral=True, embed=embed, view=view)
    elif user_check == "None":
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" does not exist.")
    else:
        await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" is created by someone else.")

# Praise command
@client.slash_command(description="Praise be to the Gods!")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
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

    banchannel2 = f"welcome"
    if (f"{message.channel}") == banchannel2:
        await message.add_reaction(payload.emoji)
        print('Mestionora added a reaction'.format(client))
        return

    banchannel3 = f"introductions"        
    if (f"{message.channel}") == banchannel3:
        await message.add_reaction(payload.emoji)
        print('Mestionora added a reaction'.format(client))
        return              

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

    if message.content.startswith('I hate books'):
        try:               
            async with cooldown(message):
                await message.channel.send('You are cursed for 10 generations.')
        except cooldowns.CallableOnCooldown:
            print(f'cooldown')

    if 'mestionora, bless' in message.content.lower():
        try:               
            async with cooldown(message):                
                value = random.randint(1,46) 
                c.execute(f"SELECT LINE from quotes where ID = '{value}'")
                print('Mestionora fetches quote from the db'.format(client))
                bless = c.fetchone()
                await message.channel.send(bless[0])
        except cooldowns.CallableOnCooldown:
            print(f'cooldown')
    
    await client.process_commands(message) 

@client.slash_command(description="Display the list of gifs.")
async def giflist(interaction:Interaction, page:Optional[int]):
    print(f"{interaction.user.name} requested the giflist")
    await get_page_giflist(client,interaction,page)

@client.slash_command(description="Display the list of tags.")
async def taglist(interaction:Interaction, page:Optional[int], set_member:Optional[Member]):
    print(f"{interaction.user.name} requested the taglist")
    await get_page_taglist(client,interaction,page,set_member)

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

        </give:0> `name` `member` - Allows to change the owner of once of your tags.
        `name` = The name of the tag you want to give.
        `member` = The user you want to set as the owner.
        '''

        acommands='''
        </sedit:0> `name` `text` - Allows edition of any existing tag (regardless of the creator).
        `name` = The name of the tag you want to edit.
        `text` = Content you want to store in the tag.

        </superrm:0> `name` - Allows removal of any existing tag (regardless of the creator).
        `name` = The name of the tag you want to remove.

        </sgive:0> `name` `member` - Allows to change the owner of a tag (regardless of the creator).
        `name` = The name of the tag you want to change owner.
        `member` = The user you want to set as the owner.
        '''

        embed=nextcord.Embed(title="Help", description="This is the list of commands for <@1027592830719377439>.",color=0xf1c40f)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png")
        embed.add_field(name="Slash Commands:", value=f"{scommands}", inline=False)
        embed.add_field(name="Admin/Mod Slash Commands:", value=f"{acommands}", inline=False)

        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in {botchannel}!")

client.run(os.getenv("TOKEN"))
