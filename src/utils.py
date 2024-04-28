from math import ceil
from typing import Any, Optional

import discord
import sqlite3

# from discord import Interaction, Embed, ButtonStyle, TextStyle
from discord.ui import View, Button, TextInput, Modal

conn = sqlite3.connect("db_tags.db")
c = conn.cursor()


class TagModal(Modal):
    def __init__(self, usemode: str, *, msg: str = "", tagn: str = ""):
        if usemode == "create":
            ModalTitle = "Create a Tag"
        elif usemode == "edit":
            ModalTitle = "Edit a Tag"
        else:
            ModalTitle = "Error: Unknown usemode"

        super().__init__(title=ModalTitle)

        self.usemode = usemode
        self.msg = msg
        self.tagn = tagn

        self.tagname = TextInput(
            label="Name of the Tag:",
            min_length=1,
            max_length=50,
            required=True,
            default=f"{tagn}",
            placeholder="Tag Name",
            style=discord.TextStyle.short,
        )
        self.add_item(self.tagname)
        self.tagcontent = TextInput(
            label="Tag Content:",
            min_length=1,
            max_length=4000,
            required=True,
            default=f"{msg}",
            placeholder="Enter wisdom here",
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.tagcontent)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        name = self.tagname.value
        text = self.tagcontent.value
        usemode = self.usemode
        msg = self.msg
        tagn = self.tagn
        if usemode == "create":
            c.execute(f"SELECT NAME from tags where NAME = ?", (name,))
            name_check = c.fetchone()

            if name_check == None:
                sql = f"INSERT INTO tags (NAME, LINK, ID) VALUES (?, ?, ?)"
                val = (name, text, interaction.user.id)
                c.execute(sql, val)
                conn.commit()
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f'Tag "{name}" created.\n__**Preview:**__\n{text}',
                )
            else:
                return await interaction.response.send_message(
                    ephemeral=True, content=f'Tag "{name}" already exists.'
                )
        elif usemode == "edit":
            if tagn == name and msg == text:
                return await interaction.response.send_message(
                    ephemeral=True, content="Nothing has been edited"
                )
            elif tagn != name and msg == text:
                c.execute(f"UPDATE tags SET NAME = '{name}' WHERE NAME = '{tagn}'")
                conn.commit()
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f'Tag "{tagn}" got their tag name edited.\n__**New Tag Name:**__ {name}',
                )
            elif tagn == name and msg != text:
                c.execute(f"UPDATE tags SET LINK = '{text}' WHERE NAME = '{tagn}'")
                conn.commit()
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f'Tag "{tagn}" got their content edited.\n__**Preview:**__\n{text}',
                )
            elif tagn != name and msg != text:
                c.execute(f"UPDATE tags SET LINK = '{text}' WHERE NAME = '{tagn}'")
                conn.commit()
                c.execute(f"UPDATE tags SET NAME = '{name}' WHERE NAME = '{tagn}'")
                conn.commit()
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f'Tag "{tagn}" got their content and tag name edited.\n__**New Tag Name:**__ {name}\n__**Preview:**__\n{text}',
                )
        else:
            return await interaction.response.send_message(
                "**Error:** `usemode` is incorrect.\n\nIf you're reading this, please report this to the devs."
            )


class PageView(View):

    def __init__(
        self,
        *,
        title: str,
        content: str,
        interaction: discord.Interaction,
        items: list[Any],
        timeout: Optional[float] = 600,
        page: int = 1,
    ):
        super().__init__(timeout=timeout)
        self._items = items
        self._interaction = interaction
        self._title = title
        self._content = content
        self._page = page

        self._next = Button(label="Next", style=discord.ButtonStyle.blurple, emoji="⏭")
        self._next.callback = self.next_page
        self._prev = Button(
            label="Previous", style=discord.ButtonStyle.blurple, emoji="⏮"
        )
        self._prev.callback = self.prev_page

        self.add_item(self._prev)
        self.add_item(self._next)

    @property
    def last_page(self) -> int:
        return ceil(len(self._items) / 10)

    @property
    def page(self) -> int:
        return self._page

    @property
    def embed(self) -> discord.Embed:
        item_content = "\n".join(self._items[(self._page - 1) * 10 : self._page * 10])
        content = f"{self._content}\n\n{item_content}"

        embed = discord.Embed(title=self._title, description=content, color=0xF1C40F)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png"
        )
        embed.set_footer(text=f"Page ({self.page}/{self.last_page})")

        return embed

    async def next_page(self, interaction: discord.Interaction):
        if self._page == self.last_page:
            return
        if interaction.user.id != self._interaction.user.id:
            await interaction.response.send_message(
                "Only the caller can do that.", ephemeral=True
            )
            return

        self._page += 1
        await interaction.response.defer()
        await self._interaction.edit_original_response(embed=self.embed)

    async def prev_page(self, interaction: discord.Interaction):
        if self._page == 1:
            return
        if interaction.user.id != self._interaction.user.id:
            await interaction.response.send_message(
                "Only the caller can do that.", ephemeral=True
            )
            return

        self._page -= 1
        await interaction.response.defer()
        await self._interaction.edit_original_response(embed=self.embed)
