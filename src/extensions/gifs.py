from typing import Optional

import discord
from discord.ext import commands

from src import c
from src.constants import bot_channel_id
from src.extensions.misc import is_bot_channel
from src.utils import PageView


class Gifs(commands.Cog, name="gifs", description="Gif commands"):

    @discord.app_commands.command(description="Display the list of gifs.")
    @discord.app_commands.describe(page="The page number to view.")
    async def giflist(self, interaction: discord.Interaction, page: Optional[int]):
        page = page or 1

        items = [
            f"{_gif[0]} • **{_gif[1]}** • [View Gif]({_gif[2]})"
            for _gif in c.execute("SELECT id, name, gif FROM gif_table").fetchall()
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
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.command(description="Recieve a divine blessing")
    @discord.app_commands.describe(name="The name of the gif you want to see.")
    @discord.app_commands.describe(id_num="The id of the gif you want to see.")
    async def gif(
        self,
        interaction: discord.Interaction,
        name: Optional[str],
        id_num: Optional[int],
    ):
        if is_bot_channel(interaction.channel):
            if name is not None and id_num is not None:
                await interaction.response.send_message(
                    "You cannot use the gif name and gif id simultaneously.",
                    ephemeral=True,
                )
                return
            elif name is not None:
                gif = c.execute(
                    "SELECT gif FROM gif_table WHERE name = ?", (name,)
                ).fetchone()
            elif id_num is not None:
                gif = c.execute(
                    "SELECT gif FROM gif_table WHERE id = ?", (id_num,)
                ).fetchone()
            else:
                gif = c.execute(
                    "SELECT gif FROM gif_table ORDER BY RANDOM() LIMIT 1"
                ).fetchone()

            if gif is None:
                await interaction.response.send_message(
                    "No gif found with that name or id.", ephemeral=True
                )
                return

            await interaction.response.send_message(gif[0])
        else:
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{interaction.user.mention} This can only be used in <#{bot_channel_id}>!",
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Gifs(bot))
