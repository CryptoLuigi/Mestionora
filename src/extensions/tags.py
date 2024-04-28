from typing import Optional
import discord
from discord.ext import commands

from src import c, conn
from src.utils import PageView, TagModal


class Tags(commands.Cog, name="tag", description="Commands to manage tags."):

    # Tag command, added entry to database Usage: /tag <name> <text>
    @discord.app_commands.command(description="Create a tag with text or a link")
    async def tag(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TagModal("create"))

    # Show command, shows entry from database Usage: /show <name>
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.command(description="Shows a stored tag")
    @discord.app_commands.describe(name="The name of the tag you want to see.")
    async def show(self, interaction: discord.Interaction, name: str):
        c.execute(f"SELECT LINK from tags where NAME = ?", (name,))
        ret = c.fetchone()

        if ret is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        else:
            await interaction.response.send_message(ret[0])

    # Admin remove command Usage: /superrm <name>
    @discord.app_commands.checks.has_any_role(
        "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
    )
    @discord.app_commands.command(description="Admin command to remove tags")
    @discord.app_commands.describe(name="The name of the tag you want to remove.")
    async def superrm(self, interaction: discord.Interaction, name: str):
        c.execute(f"SELECT ID from tags where NAME = ?", (name,))
        user_check = c.fetchone()

        if user_check is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        else:
            confirm_delete1 = discord.ui.Button(
                label="Yes", style=discord.ButtonStyle.red
            )

            async def confirm_callback1(interaction: discord.Interaction):
                c.execute(f"DELETE FROM tags WHERE tags . NAME = ?", (name,))
                conn.commit()

                await interaction.response.send_message(
                    ephemeral=True, content=f'Tag "{name}" has been removed.'
                )

            confirm_delete1.callback = confirm_callback1

            view = discord.ui.View(timeout=180)
            view.add_item(confirm_delete1)

            embed = discord.Embed(
                title="Confirm removal",
                description=f'Are you sure you want to remove tag "{name}"?',
                color=0xF1C40F,
            )

            await interaction.response.send_message(
                ephemeral=True, embed=embed, view=view
            )

    # Admin edit command Usage: /sedit <name> <text>
    @discord.app_commands.command(description="Admin command to edit tags")
    @discord.app_commands.describe(name="The name of the tag you want to edit.")
    @discord.app_commands.checks.has_any_role(
        "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
    )
    async def sedit(self, interaction: discord.Interaction, name: str):
        c.execute(f"SELECT NAME, LINK from tags where NAME = ?", (name,))
        ret = c.fetchone()

        if ret is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        else:
            name, msg = ret

            await interaction.response.send_modal(
                TagModal("edit", msg=msg.replace("\\n", "\n"), tagn=name)
            )

    # Change user id in database: /sgive <name> <member>
    @discord.app_commands.command(description="Admin command to give tags")
    @discord.app_commands.describe(name="The name of the tag you want to give.")
    @discord.app_commands.describe(member="The member you want to give the tag to.")
    @discord.app_commands.checks.has_any_role(
        "Aub", "Zent", "Giebe", "Discord admin", "Discord Mods", "staff"
    )
    async def sgive(
        self, interaction: discord.Interaction, name: str, member: discord.Member
    ):
        c.execute(f"SELECT ID from tags where NAME = ?", (name,))
        user_check = c.fetchone()

        if user_check is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        else:
            c.execute(f"UPDATE tags SET ID = ? WHERE NAME = ?", (member.id, name))
            conn.commit()

            await interaction.response.send_message(
                ephemeral=True,
                content=f'Tag "{name}" has been given to <@{member.id}>.',
            )

    # Change user id in database: /give <name> <member>
    @discord.app_commands.command(description="Give a tag")
    @discord.app_commands.describe(name="The name of the tag you want to give.")
    @discord.app_commands.describe(member="The member you want to give the tag to.")
    async def give(
        self, interaction: discord.Interaction, name: str, member: discord.Member
    ):
        c.execute(f"SELECT ID from tags where NAME = ?", (name,))
        user_check = c.fetchone()

        if user_check is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        elif user_check[0] == f"{interaction.user.id}":
            c.execute(f"UPDATE tags SET ID = ? WHERE NAME = ?", (member.id, name))
            conn.commit()

            await interaction.response.send_message(
                ephemeral=True,
                content=f'Tag "{name}" has been given to <@{member.id}>.',
            )
        else:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" is created by someone else.'
            )

    # Edit entry from tag database Usage: /edit <name>
    @discord.app_commands.command(description="Edit a tag")
    @discord.app_commands.describe(name="The name of the tag you want to edit.")
    async def edit(self, interaction: discord.Interaction, name: str):
        c.execute(f"SELECT ID, NAME, LINK from tags where NAME = ?", (name,))
        user_check = c.fetchone()

        if user_check is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        elif int(user_check[0]) != interaction.user.id:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" is created by someone else.'
            )
        else:
            _, name, msg = user_check

            await interaction.response.send_modal(
                TagModal("edit", msg=msg.replace("\\n", "\n"), tagn=name)
            )

    @discord.app_commands.command(description="Remove a tag")
    @discord.app_commands.describe(name="The name of the tag you want to remove.")
    async def rm(self, interaction: discord.Interaction, name: str):
        c.execute(f"SELECT ID from tags where NAME = ?", (name,))
        user_check = c.fetchone()

        if user_check is None:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" does not exist.'
            )
        elif user_check[0] == f"{interaction.user.id}":
            confirm_delete1 = discord.ui.Button(
                label="Yes", style=discord.ButtonStyle.red
            )

            async def confirm_callback1(interaction: discord.Interaction):
                c.execute(f"DELETE FROM tags WHERE tags . NAME = ?", (name,))
                conn.commit()

                await interaction.response.send_message(
                    ephemeral=True, content=f'Tag "{name}" has been removed.'
                )

            confirm_delete1.callback = confirm_callback1

            view = discord.ui.View(timeout=180)
            view.add_item(confirm_delete1)

            embed = discord.Embed(
                title="Confirm removal",
                description=f'Are you sure you want to remove tag "{name}"?',
                color=0xF1C40F,
            )

            await interaction.response.send_message(
                ephemeral=True, embed=embed, view=view
            )
        else:
            await interaction.response.send_message(
                ephemeral=True, content=f'Tag "{name}" is created by someone else.'
            )

    @discord.app_commands.guild_only()
    @discord.app_commands.command(description="Display the list of tags.")
    @discord.app_commands.describe(page="The page number to view.")
    @discord.app_commands.describe(set_member="The member whose tags you want to view")
    async def taglist(
        self,
        interaction: discord.Interaction,
        page: Optional[int],
        set_member: Optional[discord.Member],
    ):
        items = []
        assert interaction.guild

        if set_member:
            tags = c.execute(
                "SELECT ID, name FROM tags WHERE ID = ? ORDER BY name",
                (set_member.id,),
            ).fetchall()
        else:
            tags = c.execute("SELECT ID, name FROM tags ORDER BY name").fetchall()

        page = page or 1

        for user_id, tag_name in tags:
            if user_id:
                member = interaction.guild.get_member(int(user_id))
                creator = member.display_name if member else None
            else:
                creator = None

            items.append(f"• **{tag_name}** - {creator}")

        view = PageView(
            title="List of tags",
            content="This is the list of tags for Mestionora bot.",
            interaction=interaction,
            items=items,
            page=page,
        )

        await interaction.response.send_message(embed=view.embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tags(bot))
