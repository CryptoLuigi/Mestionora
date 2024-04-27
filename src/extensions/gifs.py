import random
from typing import Optional

import discord
from discord.ext import commands

from src import c
from src.constants import bot_channel_id
from src.utils import PageView


class Gifs(commands.Cog, name="gifs", description="Gif commands"):

    @discord.app_commands.command(description="Display the list of gifs.")
    @discord.app_commands.describe(page="The page number to view.")
    async def giflist(self, interaction: discord.Interaction, page: Optional[int]):
        page = page or 1

        items = [
            f"{_gif[0]} • **{_gif[1]}** • [View Gif]({_gif[2]})"
            for _gif in c.execute(f"SELECT id, name, gif from gif_table").fetchall()
        ]

        view = PageView(
            title="List of gifs",
            content="This is the list of gifs available on Mestionora bot.\nUse the </gif:0> command to make use of them.",
            interaction=interaction,
            items=items,
            page=page,
        )

        await interaction.response.send_message(embed=view.embed, view=view)

    # gif command, shows entry from database Usage: /gif
    @commands.cooldown(1, 30, type=commands.BucketType.member)
    @discord.app_commands.command(description="Recieve a divine blessing")
    @discord.app_commands.describe(name="The name of the gif you want to see.")
    @discord.app_commands.describe(id_num="The id of the gif you want to see.")
    async def gif(
        self,
        interaction: discord.Interaction,
        name: Optional[str],
        id_num: Optional[int],
    ):
        current_channel = f"{interaction.channel}"

        if current_channel == f"bots" or current_channel == f"🐍-bots":
            if id_num == None and name == None:
                value = random.randint(1, 76)
                c.execute(f"SELECT gif from gif_table where id = '{value}'")
                print("Mestionora fetches from the db".format)
                bless = c.fetchone()
                await interaction.response.send_message(bless[0])
            elif id_num != None and name == None:
                c.execute(f"SELECT gif from gif_table where id = '{id_num}'")
                quote = c.fetchone()
                await interaction.response.send_message(quote[0])
            elif id_num == None and name != None:
                c.execute(f"SELECT gif from gif_table where name = '{name}'")
                quote = c.fetchone()
                await interaction.response.send_message(quote[0])
            elif id_num != None and name != None:
                await interaction.response.send_message(
                    "You cannot use the gif name and gif id simultaneously.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Gifs(bot))
