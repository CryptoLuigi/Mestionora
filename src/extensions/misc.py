import datetime
import random
from typing import Optional

import discord
from discord.ext import commands
import pytz

from src import c
from src.constants import bot_channel_id

myneday_gifs = (
    "https://cdn.discordapp.com/attachments/1051224405688197130/1107797923753902150/ascendence-of-a-bookworm-bookworm-monday.gif",
    "https://cdn.discordapp.com/attachments/1003970211692695642/1110114383708823572/Its_myneday.gif",
    "https://cdn.discordapp.com/attachments/630607287660314634/1168523436331638784/giphy1.gif?ex=65521341&is=653f9e41&hm=93aad3ae52d7cab17d19dbb1e233028de553066039706aa8323a3641c38b02c0&",
    "https://cdn.discordapp.com/attachments/1003970211692695642/1097360326317592667/giphy-1.gif",
)
not_myneday_gif = "https://cdn.discordapp.com/attachments/1051224405688197130/1107797980179857499/ascendence-of-a-bookworm-bookworm-anime.gif"
prepub_ended_img = "https://cdn.discordapp.com/attachments/1029266425862434846/1287178582900215938/waiting2.png"


def is_dst(currenttime):
    if currenttime > datetime.datetime(
        currenttime.year, 11, 5, 2, tzinfo=currenttime.tzinfo
    ) or currenttime < datetime.datetime(
        currenttime.year, 3, 12, 2, tzinfo=currenttime.tzinfo
    ):
        return True
    else:
        return False


def get_prepub_ended_embed(last_datetime: datetime.datetime):
    keyword = "waiting" if random.random() < 0.8 else "suffering"
    embed = discord.Embed(
        title="Myneday",
        description=f"No Myneday in sight. We are {keyword} since <t:{int(last_datetime.timestamp())}:R>",
        color=random.randint(0x0, 0xFFFFFF),
    )
    embed.set_image(url=prepub_ended_img)
    return embed


def get_myneday_embed(myne_time: datetime.datetime, is_myneday: bool):
    timestamp = f"<t:{int(myne_time.timestamp())}:R>"
    embed = discord.Embed(
        title="Myneday",
        description=f"Next prepub {timestamp} on {timestamp.replace(':R','')}.",
        color=random.randint(0x0, 0xFFFFFF),
    )
    embed.set_image(url=random.choice(myneday_gifs) if is_myneday else not_myneday_gif)
    return embed


class Misc(commands.Cog, name="misc", description="Miscellaneous commands"):
    pass

    @discord.app_commands.command(description="Print time left for prepub")
    @discord.app_commands.checks.cooldown(1, 30)
    async def dietlindetime(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "pre-pub" or current_channel == "Church Of Dietlinde":
            print(f"{interaction.user.id} tried and failed to use /dietlindetime")
            if interaction.user.id == int(519916455857487872):
                tz_locale = pytz.timezone("America/Toronto")
                currenttime = datetime.datetime.now(tz_locale)
                dst = is_dst(currenttime)
                weekday = currenttime.weekday()
                addedtime = currenttime + datetime.timedelta(days=7 - weekday)
                if dst:
                    if currenttime.hour <= 16 and weekday == 0:
                        addedtime = currenttime
                else:
                    if currenttime.hour <= 17 and weekday == 0:
                        addedtime = currenttime
                fixedtime = datetime.datetime(
                    addedtime.year,
                    addedtime.month,
                    addedtime.day,
                    hour=17,
                    tzinfo=addedtime.tzinfo,
                )
                if dst:
                    fixedtime = datetime.datetime(
                        addedtime.year,
                        addedtime.month,
                        addedtime.day,
                        hour=16,
                        tzinfo=addedtime.tzinfo,
                    )
                timestamp = f"<t:{int(fixedtime.timestamp())}:R>"
                embed = discord.Embed(
                    title="Detlinde Day",
                    description=f"Next prepub {timestamp} on {timestamp.replace(':R','')}.",
                    color=random.randint(0x0, 0xFFFFFF),
                )
                if weekday == 0:
                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/1029754680584192132/1159320943341097030/eeeeee1.png"
                    )
                else:
                    embed.set_image(
                        url="https://cdn.discordapp.com/attachments/1029754680584192132/1159320943341097030/eeeeee1.png"
                    )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    content=f"{interaction.user.mention} Only real Doge can use this!",
                )

        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in prepub!",
            )

    # Help command
    @discord.app_commands.command(description="Get help from Mestionora", name="help")
    async def help_mestionora(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bots":
            with open("help_texts/scommands_help.txt") as shelp:
                scommands = shelp.read()

            with open("help_texts/acommands_help.txt") as ahelp:
                acommands = ahelp.read()

            embed = discord.Embed(
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
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )

    @discord.app_commands.command(description="Fetch the list of bots on the server.")
    @discord.app_commands.checks.cooldown(1, 30)
    async def list_bots(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bot":
            guild = interaction.guild
            assert guild is not None
            contentmsg = "This is the list of bots in the *Ascendance of a Bookworm* discord server:\n\n"

            for member in guild.members:
                if member.bot:
                    contentmsg += f"• {member.mention}\n"
            await interaction.response.send_message(contentmsg)
            print(f"{interaction.user} requested the bot list")
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )

    # Hello Command
    @discord.app_commands.command(description="Say hello to the Goddess")
    @discord.app_commands.checks.cooldown(1, 30)
    async def hello(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bot":
            await interaction.response.send_message(
                f"Hello {interaction.user.mention}!"
            )
        elif current_channel == "bot-development":
            await interaction.response.send_message(
                f"Hello {interaction.user.mention}!"
            )
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )

    # myneday command
    @discord.app_commands.command(description="Print time left for prepub")
    async def mynetime(self, interaction: discord.Interaction):
        myne_hour = 16
        jnovel_tz = pytz.timezone("America/Chicago")
        # SSC2 prepub ends on December 23
        last_prepub_datetime = datetime.datetime(2024, 12, 23, myne_hour, tzinfo=jnovel_tz)
        jnovel_time = datetime.datetime.now(tz=jnovel_tz).replace(
            hour=myne_hour, minute=0, second=0, microsecond=0
        )

        if jnovel_time > last_prepub_datetime:
            embed = get_prepub_ended_embed(last_prepub_datetime)
        else:
            if jnovel_time.weekday() != 0 or jnovel_time.hour > myne_hour:
                myne_time = jnovel_time + datetime.timedelta(days=7 - jnovel_time.weekday())
                myne_time = jnovel_tz.localize(
                    datetime.datetime(
                        myne_time.year, myne_time.month, myne_time.day, myne_hour
                    )
                )
            else:
                myne_time = jnovel_time
            
            embed = get_myneday_embed(myne_time, jnovel_time.weekday() == 0)

        await interaction.response.send_message(embed=embed)

    # bless command, shows entry from database Usage: /bless
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.command(description="Recieve a divine blessing")
    @discord.app_commands.describe(id_num="The id of the quote you want to see.")
    async def bless(self, interaction: discord.Interaction, id_num: Optional[int]):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bots":
            if id_num is None:
                value = random.randint(1, 46)
                c.execute(f"SELECT LINE from QUOTES where ID = '{value}'")
                bless = c.fetchone()
                await interaction.response.send_message(bless[0])
            else:
                c.execute(f"SELECT LINE from QUOTES where ID = '{id_num}'")
                quote = c.fetchone()
                await interaction.response.send_message(quote[0])
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )

    # Praise command
    @discord.app_commands.command(description="Praise be to the Gods!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def praise(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bots":
            await interaction.response.send_message(
                f"Blessings upon {interaction.user.mention}!"
            )
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Misc(bot))
