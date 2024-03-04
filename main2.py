import cooldowns, random, nextcord, sqlite3, calendar, os, datetime, pytz
from enum import Enum
from nextcord import Intents, Interaction, Member, Embed, Message, ButtonStyle, Thread
from nextcord.ext import application_checks, commands
from cooldowns import CallableOnCooldown, Cooldown, SlashBucket
from typing import Optional
from dotenv import load_dotenv
from utils import TagModal, get_page_giflist, get_page_taglist
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect("db_tags.db")
c = conn.cursor()

intents = Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix="!", help_command=None, intents=intents)

ServerID = 883777134282293258
ServerID2 = 630606651992309760
ChannelID = 1028869157841797180
ChannelID2 = 630606651992309763
welcomechannel = "<#630606999050125316>"
introchannel = "<#721199596084396063>"
botchannel = "<#638020706935767100>"
rolechannel = "<#637097683030638624>"


@client.message_command(name="Convert to vxtwitter")
async def conv_vxtwitter(interaction: Interaction, message: Message):
    msg = message.content
    x = msg.find("https://twitter.com/")
    if x == -1:
        await interaction.response.send_message("Nothing to convert", ephemeral=True)
    else:
        msg = msg.replace("https://twitter.com/", "https://vxtwitter.com/")
        await interaction.response.send_message(f"{msg}", ephemeral=True)


@client.slash_command(description="Fetch the list of bots on the server.")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def list_bots(interaction: Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bot":
        guild = nextcord.utils.find(
            lambda g: g.id == interaction.guild.id, client.guilds
        )
        contentmsg = "This is the list of bots in the *Ascendance of a Bookworm* discord server:\n\n"
        for member in guild.members:
            if member.bot:
                contentmsg += f"• {member.mention}\n"
        await interaction.response.send_message(contentmsg)
        print(f"{interaction.user} requested the bot list")
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


# Hello Command
@client.slash_command(description="Say hello to the Goddess")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def hello(interaction: Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bot":
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")
    elif current_channel == f"bot-development":
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


# On message on member join
@client.event
async def on_member_join(member: Member):
    servercheck = client.get_guild(member.guild.id)

    channel = client.get_channel(ChannelID)
    allowedserver = client.get_guild(ServerID)
    if f"{servercheck}" == f"{allowedserver}":
        bookwormrole = nextcord.utils.get(servercheck.roles, name="Bookworms 📚")
        botsrole = nextcord.utils.get(servercheck.roles, name="Bots")
        if member.bot:
            await member.add_roles(botsrole)
        else:
            await member.add_roles(bookwormrole)

    channel = client.get_channel(ChannelID2)
    allowedserver = client.get_guild(ServerID2)
    if f"{servercheck}" == f"{allowedserver}":
        await channel.send(
            f"Welcome! {member.mention} welcome to **Ascendance of a Bookworm!** Be sure to check our {welcomechannel}! Feel free to introduce yourself in {introchannel} and get a role in {rolechannel} <:MyneSparkle:1018941182430154902>"
        )


# Start up message
@client.event
async def on_ready():
    print("Mestionora lives".format(client))
    d = datetime.datetime.today()
    w = calendar.day_name[d.weekday()]
    print("Mestionora wishes you a happy", w)


# error message
@client.event
async def on_application_command_error(inter: Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await inter.send(
            ephemeral=True,
            content=f"You are being rate-limited! Retry in `{error.retry_after}` seconds.",
        )
    elif isinstance(error, application_checks.ApplicationMissingAnyRole):
        await inter.send(
            ephemeral=True, content=f"You don't have permission to do that."
        )
    elif isinstance(error, sqlite3.OperationalError):
        await inter.send(
            f"⚠There was an error with the sqlite database.⚠\n ```{error}```"
        )
        raise error
    elif isinstance(error, AttributeError):
        await inter.send(f"⚠There was an attribute error.⚠\n ```{error}```")
        raise error
    elif isinstance(error, NameError):
        await inter.send(f"⚠There was an name error.⚠\n ```{error}```")
        raise error
    else:
        raise error


# myneday command
@client.slash_command(description="Print time left for prepub")
async def mynetime(interaction : Interaction):
    myne_hour = 16
    jnovel_tz = pytz.timezone("America/Chicago")
    jnovel_time = datetime.datetime.now(tz=jnovel_tz).replace(hour=myne_hour, minute=0, second=0, microsecond=0)

    if jnovel_time.weekday() != 0 or jnovel_time.hour > myne_hour:
        myne_time = jnovel_time + datetime.timedelta(days=7 - jnovel_time.weekday())
        myne_time = jnovel_tz.localize(
            datetime.datetime(myne_time.year, myne_time.month, myne_time.day, myne_hour)
        )
    else:
        myne_time = jnovel_time

    timestamp = f"<t:{int(myne_time.timestamp())}:R>"
    embed = nextcord.Embed(title="Myneday", description=f"Next prepub {timestamp} on {timestamp.replace(':R','')}.", color=random.randint(0x0, 0xffffff))

    myneday_gifs = (
        'https://cdn.discordapp.com/attachments/1051224405688197130/1107797923753902150/ascendence-of-a-bookworm-bookworm-monday.gif',
        'https://cdn.discordapp.com/attachments/1003970211692695642/1110114383708823572/Its_myneday.gif',
        'https://cdn.discordapp.com/attachments/630607287660314634/1168523436331638784/giphy1.gif?ex=65521341&is=653f9e41&hm=93aad3ae52d7cab17d19dbb1e233028de553066039706aa8323a3641c38b02c0&',
        'https://cdn.discordapp.com/attachments/1003970211692695642/1097360326317592667/giphy-1.gif'
        )

    if jnovel_time.weekday() == 0:
        embed.set_image(random.choice(myneday_gifs))
    else:
        embed.set_image(
            "https://cdn.discordapp.com/attachments/1051224405688197130/1107797980179857499/ascendence-of-a-bookworm-bookworm-anime.gif"
        )
    await interaction.response.send_message(embed=embed)


# gif command, shows entry from database Usage: /gif
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def gif(interaction: Interaction, name: Optional[str], id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bots":
        if id_num == None and name == None:
            value = random.randint(1, 76)
            c.execute(f"SELECT gif from gif_table where id = '{value}'")
            print("Mestionora fetches from the db".format(client))
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
            await interaction.send(
                "You cannot use the gif name and gif id simultaneously.", ephemeral=True
            )
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


# bless command, shows entry from database Usage: /bless
@client.slash_command(description="Recieve a divine blessing")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def bless(interaction: Interaction, id_num: Optional[int]):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bots":
        if id_num == None:
            value = random.randint(1, 46)
            c.execute(f"SELECT LINE from QUOTES where ID = '{value}'")
            print("Mestionora fetches from the db".format(client))
            bless = c.fetchone()
            await interaction.send(bless[0])
        else:
            c.execute(f"SELECT LINE from QUOTES where ID = '{id_num}'")
            quote = c.fetchone()
            await interaction.send(quote[0])
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


# Tag command, added entry to database Usage: /tag <name> <text>
@client.slash_command(description="Create a tag with text or a link")
async def tag(interaction: Interaction):
    msg = ""
    tagn = ""
    await interaction.response.send_modal(TagModal("create", msg, tagn))


@client.message_command(name="Create tag")
async def tag_from_msg(interaction: Interaction, message: Message):
    msg = message.content
    tagn = ""
    await interaction.response.send_modal(TagModal("create", msg, tagn))


# Show command, shows entry from database Usage: /show <name>
@client.slash_command(description="Shows a stored tag")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def show(interaction: Interaction, name: str):
    c.execute(f"SELECT LINK from tags where NAME = '{name}'")
    print("Mestionora fetches from the db".format(client))
    show = c.fetchone()
    if show[0] == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        await interaction.send(show[0])


# Admin remove command Usage: /superrm <name>
@client.slash_command(description="Admin command to remove tags")
@application_checks.has_any_role(
    "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
)
async def superrm(interaction: Interaction, name: str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        confirm_delete1 = nextcord.ui.Button(label="Yes", style=ButtonStyle.red)

        async def confirm_callback1(interaction: Interaction):
            c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}'")
            conn.commit()
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" has been removed.'
            )
            print("Mestionora deleted from the db".format(client))

        confirm_delete1.callback = confirm_callback1

        view = nextcord.ui.View(timeout=180)
        view.add_item(confirm_delete1)

        embed = Embed(
            title="Confirm removal",
            description=f'Are you sure you want to remove tag "{name}"?',
            color=0xF1C40F,
        )

        await interaction.response.send_message(ephemeral=True, embed=embed, view=view)


# Admin edit command Usage: /sedit <name> <text>
@client.slash_command(description="Admin command to edit tags")
@application_checks.has_any_role(
    "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
)
async def sedit(interaction: Interaction, name: str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        c.execute(f"SELECT NAME from tags where NAME = '{name}'")
        tagn = c.fetchone()
        c.execute(f"SELECT LINK from tags where NAME = '{name}'")
        msg = c.fetchone()
        msg = msg[0].replace("\\n", "\n")
        await interaction.response.send_modal(TagModal("edit", msg, tagn[0]))


# Change user id in database: /sgive <name> <member>
@client.slash_command(description="Admin command to give tags")
@application_checks.has_any_role(
    "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
)
async def sgive(interaction: Interaction, name: str, member: Member):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        c.execute(f"UPDATE tags SET ID = '{member.id}' WHERE NAME = '{name}'")
        conn.commit()
        print("Mestionora changed tag owner in the db".format(client))
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" has been given to <@{member.id}>.'
        )


# Change user id in database: /give <name> <member>
@client.slash_command(description="Give a tag")
async def give(interaction: Interaction, name: str, member: Member):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        c.execute(f"UPDATE tags SET ID = '{member.id}' WHERE NAME = '{name}'")
        conn.commit()
        print("Mestionora changed tag owner in the db".format(client))
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" has been given to <@{member.id}>.'
        )
    elif user_check == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" is created by someone else.'
        )


# Edit entry from tag database Usage: /edit <name>
@client.slash_command(description="Edit a tag")
async def edit(interaction: Interaction, name: str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        c.execute(f"SELECT NAME from tags where NAME = '{name}'")
        tagn = c.fetchone()
        c.execute(f"SELECT LINK from tags where NAME = '{name}'")
        msg = c.fetchone()
        msg = msg[0].replace("\\n", "\n")
        await interaction.response.send_modal(TagModal("edit", msg, tagn[0]))
    elif user_check == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" is created by someone else.'
        )


@client.slash_command(description="Remove a tag")
async def rm(interaction: Interaction, name: str):
    c.execute(f"SELECT ID from tags where NAME = '{name}'")
    user_check = c.fetchone()
    if user_check[0] == f"{interaction.user.id}":
        confirm_delete1 = nextcord.ui.Button(label="Yes", style=ButtonStyle.red)

        async def confirm_callback1(interaction: Interaction):
            c.execute(f"DELETE FROM tags WHERE tags . NAME = '{name}'")
            conn.commit()
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" has been removed.'
            )
            print("Mestionora deleted from the db".format(client))

        confirm_delete1.callback = confirm_callback1

        view = nextcord.ui.View(timeout=180)
        view.add_item(confirm_delete1)

        embed = Embed(
            title="Confirm removal",
            description=f'Are you sure you want to remove tag "{name}"?',
            color=0xF1C40F,
        )

        await interaction.response.send_message(ephemeral=True, embed=embed, view=view)
    elif user_check == "None":
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" does not exist.'
        )
    else:
        await interaction.response.send_message(
            ephemeral=True, content=f'Tag "{name}" is created by someone else.'
        )


# Praise command
@client.slash_command(description="Praise be to the Gods!")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def praise(interaction: Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bots":
        await interaction.send(f"Blessings upon {interaction.user.mention}!")
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


class CooldownBucket(Enum):
    message_author = 1

    def process(self, *args, **kwargs):
        return args[0].author.id


cooldown = Cooldown(1, 15, CooldownBucket.message_author)


@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(
        payload.message_id
    )

    if message.author == client.user:
        return

    banchannel2 = f"welcome"
    if (f"{message.channel}") == banchannel2:
        await message.add_reaction(payload.emoji)
        print("Mestionora added a reaction".format(client))
        return

    banchannel3 = f"introductions"
    if (f"{message.channel}") == banchannel3:
        await message.add_reaction(payload.emoji)
        print("Mestionora added a reaction".format(client))
        return


# Random quote generator
@client.event
async def on_message(message: Message):
    banchannel = f"bots"
    if message.author == client.user:
        return

    print(f"{message.channel}")

    if (f"{message.channel}") != banchannel:
        return

    if "praise be to the gods" in message.content.lower():
        try:
            async with cooldown(message):
                await message.channel.send(
                    "Blessings upon " + str(message.author.mention)
                )
                value = random.randint(1, 8)
                if value == 1:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/1027597999091753010/1028786413455552583/unknown.png"
                    )
                if value == 2:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/883777134911422466/1028791311807037510/LN_P4V3-2.jpg"
                    )
                if value == 3:
                    await message.channel.send(
                        "https://media.discordapp.net/attachments/883777134911422466/1028793143652536320/Screenshot_20221009-151607_Google_Play_Books.jpg"
                    )
                if value == 4:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/883777134911422466/1028794786569797775/LN_P1V3-Insert.jpg"
                    )
                if value == 5:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/883777134911422466/1028795750999674880/LN_P2V2-7.jpg"
                    )
                if value == 6:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/1027597999091753010/1028855796731232296/unknown.png"
                    )
                if value == 7:
                    await message.channel.send(
                        "https://media.discordapp.net/attachments/1029782845071294595/1030838261184208947/LN_P4V4-Insert.jpg?width=993&height=775"
                    )
                if value == 8:
                    await message.channel.send(
                        "https://media.discordapp.net/attachments/1029782845071294595/1030838628710088785/11.jpg"
                    )

        except cooldowns.CallableOnCooldown:
            print(f"cooldown")

    if message.content.startswith("I hate books"):
        try:
            async with cooldown(message):
                await message.channel.send("You are cursed for 10 generations.")
        except cooldowns.CallableOnCooldown:
            print(f"cooldown")

    if "mestionora, bless" in message.content.lower():
        try:
            async with cooldown(message):
                value = random.randint(1, 46)
                c.execute(f"SELECT LINE from quotes where ID = '{value}'")
                print("Mestionora fetches quote from the db".format(client))
                bless = c.fetchone()
                await message.channel.send(bless[0])
        except cooldowns.CallableOnCooldown:
            print(f"cooldown")

    await client.process_commands(message)


@client.slash_command(description="Display the list of gifs.")
async def giflist(interaction: Interaction, page: Optional[int]):
    print(f"{interaction.user.name} requested the giflist")
    await get_page_giflist(client, interaction, page)


@client.slash_command(description="Display the list of tags.")
async def taglist(
    interaction: Interaction, page: Optional[int], set_member: Optional[Member]
):
    print(f"{interaction.user.name} requested the taglist")
    await get_page_taglist(client, interaction, page, set_member)


def is_dst(currenttime):
    if currenttime > datetime.datetime(currenttime.year, 11, 5, 2, tzinfo=currenttime.tzinfo) or currenttime < datetime.datetime(currenttime.year, 3, 12, 2, tzinfo=currenttime.tzinfo):
        return True
    else:
        return False

#myneday command
#@client.slash_command(description="Print time left for prepub")
#async def mynetime(interaction : Interaction):
#    tz_locale = pytz.timezone("America/Toronto")
#    dst = currenttime = datetime.datetime.now(tz_locale)
#    weekday = currenttime.weekday()
#    addedtime = currenttime + datetime.timedelta(days=7-weekday)
#    if dst:
#        if currenttime.hour <= 17 and weekday == 0:
#            addedtime = currenttime
#    else:
#        if currenttime.hour <= 17 and weekday == 0:
#            addedtime = currenttime
#    fixedtime = datetime.datetime(addedtime.year, addedtime.month, addedtime.day, hour=17, tzinfo=addedtime.tzinfo)
#    if dst:
#        fixedtime = datetime.datetime(addedtime.year, addedtime.month, addedtime.day, hour=17, tzinfo=addedtime.tzinfo)
#    timestamp = f"<t:{int(fixedtime.timestamp())}:R>"
#    embed = nextcord.Embed(title="Myneday", description=f"Next prepub {timestamp} on {timestamp.replace(':R','')}.", color=random.randint(0x0, 0xffffff))#
#
#    myneday_gifs = (
#        'https://cdn.discordapp.com/attachments/1051224405688197130/1107797923753902150/ascendence-of-a-bookworm-bookworm-monday.gif',
#        'https://cdn.discordapp.com/attachments/1003970211692695642/1110114383708823572/Its_myneday.gif',
#        'https://cdn.discordapp.com/attachments/630607287660314634/1168523436331638784/giphy1.gif?ex=65521341&is=653f9e41&hm=93aad3ae52d7cab17d19dbb1e233028de553066039706aa8323a3641c38b02c0&',
#        'https://cdn.discordapp.com/attachments/1003970211692695642/1097360326317592667/giphy-1.gif'
#        )
#    if weekday == 0:
#        embed.set_image(random.choice(myneday_gifs))
#    else:
#        embed.set_image('https://cdn.discordapp.com/attachments/1051224405688197130/1107797980179857499/ascendence-of-a-bookworm-bookworm-anime.gif')
#    await interaction.response.send_message(embed=embed)

@client.slash_command(description="Print time left for prepub")
@cooldowns.cooldown(1, 30, bucket=SlashBucket.author)
async def dietlindetime(interaction : Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f'pre-pub' or current_channel == f'Church Of Dietlinde':
        print(f"{interaction.user.id}")
        if interaction.user.id == int(519916455857487872):
            tz_locale = pytz.timezone("America/Toronto")
            currenttime = datetime.datetime.now(tz_locale)
            dst = is_dst(currenttime)
            weekday = currenttime.weekday()
            addedtime = currenttime + datetime.timedelta(days=7-weekday)
            if dst:
                if currenttime.hour <= 16 and weekday == 0:
                    addedtime = currenttime
            else:
                if currenttime.hour <= 17 and weekday == 0:
                    addedtime = currenttime
            fixedtime = datetime.datetime(addedtime.year, addedtime.month, addedtime.day, hour=17, tzinfo=addedtime.tzinfo)
            if dst:
                fixedtime = datetime.datetime(addedtime.year, addedtime.month, addedtime.day, hour=16, tzinfo=addedtime.tzinfo)
            timestamp = f"<t:{int(fixedtime.timestamp())}:R>"
            embed = nextcord.Embed(title="Detlinde Day", description=f"Next prepub {timestamp} on {timestamp.replace(':R','')}.", color=random.randint(0x0, 0xffffff))
            if weekday == 0:
                embed.set_image('https://cdn.discordapp.com/attachments/1029754680584192132/1159320943341097030/eeeeee1.png')
            else:
                embed.set_image('https://cdn.discordapp.com/attachments/1029754680584192132/1159320943341097030/eeeeee1.png')
            await interaction.response.send_message(embed=embed)
        else:    
            await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} Only real Doge can use this!")

    else:
        await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in prepub!")

# Help command
@client.slash_command(description="Get help from Mestionora")
async def help_mestionora(interaction: Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bots":
        with open("help_texts/scommands_help.txt") as shelp:
            scommands = shelp.read()

        with open("help_texts/acommands_help.txt") as ahelp:
            acommands = ahelp.read()

        embed = Embed(
            title="Help",
            description="This is the list of commands for <@1027592830719377439>.",
            color=0xF1C40F,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png"
        )
        embed.add_field(name="Slash Commands:", value=f"{scommands}", inline=False)
        embed.add_field(
            name="Admin/Mod Slash Commands:", value=f"{acommands}", inline=False
        )

        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        await interaction.response.send_message(
            ephemeral=True,
            content=f"{interaction.user.mention} This can only be used in {botchannel}!",
        )


import sqlalchemy as sa
from src.clubs.models import Club, ClubMember
from src import Session

@client.slash_command()
async def club(interaction: Interaction):
    pass

@club.subcommand(description="Create a club", name="create")
async def create_club(interaction: Interaction, name: str):
    """Create a club. Clubs are used to get mentions when threads related to the club are created."""
    name = name.lower()

    if interaction.guild is None or interaction.channel is None:
        return await interaction.response.send_message(
            ephemeral=True,
            content="This command must be used in a server.",
        )

    with Session.begin() as session:
        club = session.execute(
            sa.select(Club).filter(
                Club.name == name, Club.guild_id == interaction.guild.id
            )
        ).scalar_one_or_none()

        if club:
            return await interaction.response.send_message(
                ephemeral=True,
                content=f"Club {name} already exists",
            )

        club = Club(
            name=name, guild_id=interaction.guild.id, creator_id=interaction.user.id
        )
        club.members.append(ClubMember(user_id=interaction.user.id))
        session.add(club)

    await interaction.response.send_message(
        ephemeral=True,
        content=f"Created club `{name}`",
    )


@club.subcommand(description="Delete a club", name="delete")
async def delete_club(interaction: Interaction, name: str):
    """Delete a club. This will remove all members from the club."""
    name = name.lower()

    if (
        interaction.guild is None
        or interaction.channel is None
        or not isinstance(interaction.user, Member)
    ):
        return await interaction.response.send_message(
            ephemeral=True,
            content="This command must be used in a server.",
        )

    with Session.begin() as session:
        club = session.execute(
            sa.select(Club).filter(
                Club.name == name, Club.guild_id == interaction.guild.id
            )
        ).scalar_one_or_none()

        if not club:
            return await interaction.response.send_message(
                ephemeral=True, 
                content=f"Club {name} does not exist",
            )

        if (
            club.creator_id != interaction.user.id
            and not interaction.user.guild_permissions.manage_guild
        ):
            return await interaction.response.send_message(
                ephemeral=True, 
                content=f"You are not the creator of the club {name}",
            )

        for member in club.members:
            session.delete(member)

        session.delete(club)

    await interaction.response.send_message(
        ephemeral=True, 
        content=f"Deleted club {name}",
    )


@club.subcommand(description="Join a club", name="join")
async def join_club(interaction: Interaction, name: str):
    """Join a club. You will get mentions when threads related to the club are created."""
    name = name.lower()

    if interaction.guild is None or interaction.channel is None:
        return await interaction.response.send_message(
            ephemeral=True, 
            content="This command must be used in a server.",
        )

    with Session.begin() as session:
        club = session.execute(
            sa.select(Club).filter(
                Club.name == name, Club.guild_id == interaction.guild.id
            )
        ).scalar_one_or_none()

        if not club:
            return await interaction.response.send_message(
                ephemeral=True, 
                content=f"Club {name} does not exist",
            )

        if interaction.user.id in {member.user_id for member in club.members}:
            return await interaction.response.send_message(
                ephemeral=True,
                content=f"You are already in club {name}",
            )

        club.members.append(ClubMember(user_id=interaction.user.id))

    await interaction.response.send_message(
        ephemeral=True, 
        content=f"Joined club {name}",
    )

@club.subcommand(description="Leave a club", name="leave")
async def leave_club(interaction: Interaction, name: str):
    """Leave a club. You will no longer get mentions when threads related to the club are created."""
    name = name.lower()

    if interaction.guild is None or interaction.channel is None:
        await interaction.response.send_message(
            ephemeral=True,
            content="This command must be used in a server.",
        )
        return

    with Session.begin() as session:
        club = session.execute(
            sa.select(Club).filter(
                Club.name == name, Club.guild_id == interaction.guild.id
            )
        ).scalar_one_or_none()

        if not club:
            await interaction.response.send_message(
                ephemeral=True, 
                content=f"Club {name} does not exist",
            )
            return

        if interaction.user.id not in [member.user_id for member in club.members]:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"You are not in club {name}",
            )
            return

        session.execute(
            sa.delete(ClubMember).filter(
                ClubMember.user_id == interaction.user.id, ClubMember.club_id == club.id
            )
        )

    await interaction.response.send_message(
        ephemeral=True, 
        content=f"Left club {name}",
    )

@club.subcommand(description="List all clubs in a server", name="list")
async def list_clubs(interaction: Interaction):
    current_channel = f"{interaction.channel}"
    if current_channel == f"bots" or current_channel == f"🐍-bots":
        if interaction.guild is None or interaction.channel is None:
            return await interaction.response.send_message(
                ephemeral=True,
                content="This command must be used in a server.",
            )

        with Session.begin() as session:
            clubs = (
                session.execute(
                    sa.select(Club).filter(Club.guild_id == interaction.guild.id)
                )
                .scalars()
                .all()
            )

            if not clubs:
                description = f"There are no clubs in {interaction.guild.name}."
            else:
                description = f"List of the clubs in {interaction.guild.name}:\n"
                description += "\n".join(
                    f"{i+1}. `{club.name}` ({len(club.members)} members)"
                    for i, club in enumerate(clubs)
                )

            embed = Embed(
                title="Clubs",
                description=description,
                color=0xF1C40F,
            )
            await interaction.response.send_message(embed=embed)
    else:
        if interaction.guild is None or interaction.channel is None:
            return await interaction.response.send_message(
                ephemeral=True,
                content="This command must be used in a server.",
            )

        with Session.begin() as session:
            clubs = (
                session.execute(
                    sa.select(Club).filter(Club.guild_id == interaction.guild.id)
                )
                .scalars()
                .all()
            )

            if not clubs:
                description = f"There are no clubs in {interaction.guild.name}."
            else:
                description = f"List of the clubs in {interaction.guild.name}:\n"
                description += "\n".join(
                    f"{i+1}. `{club.name}` ({len(club.members)} members)"
                    for i, club in enumerate(clubs)
                )

            embed = Embed(
                title="Clubs",
                description=description,
                color=0xF1C40F,
            )
            await interaction.response.send_message(
                ephemeral=True, 
                embed=embed,
            )


@club.subcommand(description="Publish to a club", name="publish")
async def publish_to_club(interaction: Interaction, name: str):
    """Publish a thread to a club.
    This will add all the members of this club to this thread, which gives them a notification.
    """
    name = name.lower()

    if (
        interaction.guild is None
        or interaction.channel is None
        or not isinstance(interaction.channel, Thread)
        or not isinstance(interaction.user, Member)
    ):
        return await interaction.response.send_message(
            ephemeral=True,
            content="This command must be used in a thread in a server.",
        )

    with Session.begin() as session:
        club = session.execute(
            sa.select(Club).filter(
                Club.name == name, Club.guild_id == interaction.guild.id
            )
        ).scalar_one_or_none()

        if not club:
            return await interaction.response.send_message(
                ephemeral=True,
                content=f"Club {name} does not exist",
            )

        if (
            club.creator_id != interaction.user.id
            and not interaction.user.guild_permissions.manage_threads
        ):
            return await interaction.response.send_message(
                ephemeral=True,
                content=f"You are not the creator of club {name}",
            )

        # Pin the first message if it exists, and we have permission to do so
        if (
            interaction.channel.starter_message
            and interaction.channel.permissions_for(
                interaction.guild.me
            ).manage_messages
        ):
            await interaction.channel.starter_message.pin()

        async def consolidate_members():
            # Find all the members that aren't in the thread, and add them
            members = await interaction.channel.fetch_members()
            members_in_channel = {member.id for member in members}
            club_members = {member.user_id for member in club.members}

            for member_id in club_members.difference(members_in_channel):
                await interaction.channel.add_user(nextcord.Object(id=member_id))

        # For some reason discord seems to be dropping some of the people we add to the thread
        #  so perform this action twice to ensure everyone is added
        await consolidate_members()
        await consolidate_members()

        await interaction.response.send_message(f"Added everyone from club {name}")


client.run(os.getenv("TOKEN"))
