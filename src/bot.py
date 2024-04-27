import sqlite3
import discord
from discord.ext import commands
from discord.flags import Intents

from src.utils import TagModal


class Mestionora(commands.Bot):

    async def setup_hook(self) -> None:
        pass
        # await self.tree.sync()


bot = commands.Bot(command_prefix="!", help_command=None, intents=Intents.all())

# The following are things that don't really fit into the extension/cog setup
#  such as the application command error handling, and context menus


# error message
@bot.tree.error
async def on_error(inter: discord.Interaction, error):
    error = getattr(error, "original", error)

    async def send(content: str, ephemeral: bool = True):
        if inter.response.is_done():
            await inter.followup.send(content, ephemeral=ephemeral)
        else:
            await inter.response.send_message(content, ephemeral=ephemeral)

    if isinstance(error, commands.CommandOnCooldown):
        await send(
            ephemeral=True,
            content=f"You are being rate-limited! Retry in `{error.retry_after}` seconds.",
        )
    elif isinstance(error, commands.MissingAnyRole):
        await send(ephemeral=True, content="You don't have permission to do that.")
    elif isinstance(error, sqlite3.OperationalError):
        await send(f"⚠There was an error with the sqlite database.⚠\n ```{error}```")
        raise error
    elif isinstance(error, AttributeError):
        await send(f"⚠There was an attribute error.⚠\n ```{error}```")
        raise error
    elif isinstance(error, NameError):
        await send(f"⚠There was a name error.⚠\n ```{error}```")
        raise error
    else:
        raise error


@bot.tree.context_menu(name="Convert to vxtwitter")
async def conv_vxtwitter(interaction: discord.Interaction, message: discord.Message):
    msg = message.content
    x = msg.find("https://twitter.com/")
    if x == -1:
        await interaction.response.send_message("Nothing to convert", ephemeral=True)
    else:
        msg = msg.replace("https://twitter.com/", "https://vxtwitter.com/")
        await interaction.response.send_message(f"{msg}", ephemeral=True)


@bot.tree.context_menu(name="Create tag")
async def tag_from_msg(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_modal(TagModal("create", msg=message.content))
