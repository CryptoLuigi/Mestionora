import calendar
import datetime
import random

import discord
from discord.ext import commands

from src import c
from src.constants import (
    bookworm_server_id,
    welcome_channel_id,
    chibi_server_id,
    intro_channel_id,
    role_channel_id,
)


class Events(commands.Cog, name="events"):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self._bot = bot
        self._cooldown = commands.CooldownMapping.from_cooldown(
            1, 15, type=commands.BucketType.member
        )

    # On message on member join
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        if guild.id == chibi_server_id:

            if member.bot:
                role = discord.utils.get(guild.roles, name="Bots")
                if role is None:
                    raise commands.RoleNotFound("`Bots` role not found")

            else:
                role = discord.utils.get(guild.roles, name="Bookworms 📚")
                if role is None:
                    raise commands.RoleNotFound("`Bookworms 📚` role not found")

            await member.add_roles(role)

        if guild.id == bookworm_server_id:
            await self._bot.get_partial_messageable(welcome_channel_id).send(
                f"Welcome! {member.mention} welcome to **Ascendance of a Bookworm!** "
                f"Be sure to check our <#{welcome_channel_id}>! "
                f"Feel free to introduce yourself in <#{intro_channel_id}> "
                f"and get a role in <#{role_channel_id}> <:MyneSparkle:1018941182430154902>"
            )

    # Start up message
    @commands.Cog.listener()
    async def on_ready(
        self,
    ):
        print("Mestionora lives")
        d = datetime.datetime.today()
        w = calendar.day_name[d.weekday()]
        print("Mestionora wishes you a happy", w)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self._bot.get_partial_messageable(payload.channel_id)
        message = discord.PartialMessage(channel=channel, id=payload.message_id)

        if self._bot.user is None or payload.user_id == self._bot.user.id:
            return

        if payload.channel_id in [intro_channel_id, welcome_channel_id]:
            await message.add_reaction(payload.emoji)
            print("Mestionora added a reaction")

    # Random quote generator
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        banchannel = f"bots"
        if message.author == self._bot.user:
            return

        print(f"{message.channel}")

        if (f"{message.channel}") != banchannel:
            return

        retry_after = self._cooldown.update_rate_limit(message)

        if "praise be to the gods" in message.content.lower():
            if retry_after:
                assert self._cooldown._cooldown is not None
                print("cooldown")
                return

            await message.channel.send("Blessings upon " + str(message.author.mention))
            links = [
                "https://cdn.discordapp.com/attachments/1027597999091753010/1028786413455552583/unknown.png",
                "https://cdn.discordapp.com/attachments/883777134911422466/1028791311807037510/LN_P4V3-2.jpg",
                "https://media.discordapp.net/attachments/883777134911422466/1028793143652536320/Screenshot_20221009-151607_Google_Play_Books.jpg",
                "https://cdn.discordapp.com/attachments/883777134911422466/1028794786569797775/LN_P1V3-Insert.jpg",
                "https://cdn.discordapp.com/attachments/883777134911422466/1028795750999674880/LN_P2V2-7.jpg",
                "https://cdn.discordapp.com/attachments/1027597999091753010/1028855796731232296/unknown.png",
                "https://media.discordapp.net/attachments/1029782845071294595/1030838261184208947/LN_P4V4-Insert.jpg?width=993&height=775",
                "https://media.discordapp.net/attachments/1029782845071294595/1030838628710088785/11.jpg",
            ]

            await message.channel.send(random.choice(links))

        if message.content.startswith("I hate books"):
            if retry_after:
                assert self._cooldown._cooldown is not None
                print("cooldown")
                return

            await message.channel.send("You are cursed for 10 generations.")

        if "mestionora, bless" in message.content.lower():
            if retry_after:
                assert self._cooldown._cooldown is not None
                print("cooldown")
                return

            value = random.randint(1, 46)
            c.execute(f"SELECT LINE from quotes where ID = '{value}'")
            print("Mestionora fetches quote from the db")
            bless = c.fetchone()
            await message.channel.send(bless[0])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
