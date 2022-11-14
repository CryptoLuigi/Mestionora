import cooldowns, random , nextcord, sqlite3
from cooldowns import CallableOnCooldown, Cooldown
from enum import Enum
from nextcord import Intents, Interaction, Embed
from nextcord.ext import commands, application_checks
from nextcord.ui import View, Button
from typing import Optional
from math import ceil

#Updated

conn = sqlite3.connect('db_tags.db')
c = conn.cursor()

intents = Intents.all()
intents.message_content = True
#client = commands.Bot(command_prefix='!', help_command=None, intents=intents)
client = nextcord.Client(intents=intents)

class TagModal(nextcord.ui.Modal):
    def __init__(self, usemode, msg, tagn):
        ModalTitle = ""
        if usemode == "create":
            ModalTitle = "Create a Tag"
        elif usemode == "edit":
            ModalTitle = "Edit a Tag"
        else:
            ModalTitle = "Error: Unknown usemode"
        super().__init__(
            ModalTitle,
        )

        self.usemode = usemode
        self.msg = msg
        self.tagn = tagn

        self.tagname = nextcord.ui.TextInput(label="Name of the Tag:", min_length=1, max_length=50, required=True, default_value=f"{tagn}", placeholder="Tag Name", style=nextcord.TextInputStyle.short,)
        self.add_item(self.tagname)
        self.tagcontent = nextcord.ui.TextInput(label="Tag Content:", min_length=1, max_length=4000, required=True, default_value=f"{msg}", placeholder="Enter wisdom here", style=nextcord.TextInputStyle.paragraph,)
        self.add_item(self.tagcontent)

    async def callback(self, interaction: Interaction) -> None:
        name = self.tagname.value
        text = self.tagcontent.value
        usemode = self.usemode
        msg = self.msg
        tagn = self.tagn
        if usemode == "create":
            c.execute(f"SELECT NAME from tags where NAME = '{name}'")
            name_check = c.fetchone()
            if name_check == None:
                sql = f"INSERT INTO tags (NAME, LINK, ID) VALUES (?, ?, ?)"
                val = (name, text, interaction.user.id)
                c.execute(sql, val)
                conn.commit()
                print('Mestionora added to the db'.format(client))
                return await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" created.\n__**Preview:**__\n{text}")
            else:
                return await interaction.response.send_message(ephemeral=True, content=f"Tag \"{name}\" already exists.")
        elif usemode == "edit":
            if tagn == name and msg == text:
                return await interaction.response.send_message(ephemeral=True, content="Nothing has been edited")
            elif tagn != name and msg == text:
                c.execute(f"UPDATE tags SET NAME = '{name}' WHERE NAME = '{tagn}'")
                conn.commit()
                print('Mestionora edited the db (name)'.format(client))
                return await interaction.response.send_message(ephemeral=True, content=f"Tag \"{tagn}\" got their tag name edited.\n__**New Tag Name:**__ {name}")
            elif tagn == name and msg != text:
                c.execute(f"UPDATE tags SET LINK = '{text}' WHERE NAME = '{tagn}'")
                conn.commit()
                print('Mestionora edited the db (text)'.format(client))
                return await interaction.response.send_message(ephemeral=True, content=f"Tag \"{tagn}\" got their content edited.\n__**Preview:**__\n{text}")
            elif tagn != name and msg != text:
                c.execute(f"UPDATE tags SET LINK = '{text}' WHERE NAME = '{tagn}'")
                conn.commit()
                c.execute(f"UPDATE tags SET NAME = '{name}' WHERE NAME = '{tagn}'")
                conn.commit()
                print('Mestionora edited the db (name+text)'.format(client))
                return await interaction.response.send_message(ephemeral=True, content=f"Tag \"{tagn}\" got their content and tag name edited.\n__**New Tag Name:**__ {name}\n__**Preview:**__\n{text}")
        else:
            return await interaction.response.send_message("**Error:** `usemode` is incorrect.\n\nIf you're reading this, please report this to the devs.")

class SetPage(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Set Page",
        )

        self.setpagenb = nextcord.ui.TextInput(label="Page number:", min_length=1, max_length=50, required=True, style=nextcord.TextInputStyle.short)
        self.add_item(self.setpagenb)

    async def callback(self, interaction: Interaction) -> None:
        pagenb = self.setpagenb.value
        print(pagenb)
        return pagenb


async def get_page_giflist(client,interaction,page:int) -> None:
    NextButton = Button(label="Next", style=nextcord.ButtonStyle.blurple, emoji="⏭")
    PrevButton = Button(label="Previous", style=nextcord.ButtonStyle.blurple, emoji="⏮")
    view = View(timeout=600)
    view.add_item(PrevButton)
    view.add_item(NextButton)

    c.execute(f"SELECT id from gif_table")
    gif_data = c.fetchall()
    
    gif_list_content = f"This is the list of gifs availlable on Mestionora bot.\nUse the </gif:0> command to make use of them.\n\n"

    last_page = ceil(len(gif_data)/10)

    if page == None or page <= 0:
        if last_page == 0:
            page = int(0)
        else:
            page = int(1)
    elif page > last_page:
        page = last_page

    caller = interaction.user

    async def button_callback(interaction):
        if interaction.user == caller:
            await get_page_giflist(client, interaction, page=page+1)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    async def button_callback2(interaction):
        if interaction.user == caller:
            await get_page_giflist(client, interaction, page=page-1)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    NextButton.callback = button_callback
    PrevButton.callback = button_callback2

    for data in gif_data[(((page*10)-10)):(10+((page*10)-10))]:
        c.execute(f"SELECT name from gif_table where id = '{data[0]}'")
        name_entry = c.fetchone()
        gif_list_content += f"{data[0]} • **{name_entry[0]}**\n"

    embed = Embed(title=f"List of gifs", description=f"{gif_list_content}",color=0xf1c40f)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png")
    embed.set_footer(text=f"Page ({page}/{last_page})")
    try:
        await interaction.response.edit_message(embed=embed, view=view)
    except:
        await interaction.response.send_message(embed=embed, view=view)

async def get_page_taglist(client,interaction,page:int,set_member) -> None:
    NextButton = Button(label="Next", style=nextcord.ButtonStyle.blurple, emoji="⏭")
    PrevButton = Button(label="Previous", style=nextcord.ButtonStyle.blurple, emoji="⏮")
    view = View(timeout=600)
    view.add_item(PrevButton)
    view.add_item(NextButton)

    selected_id = None
    if set_member != None:
        selected_id = set_member.id

    c.execute(f"SELECT NAME from tags")
    tags_data = c.fetchall()
    tags_filtered_data = ["Mestionora"]

    for data in tags_data:
        c.execute(f"SELECT ID from tags where NAME = '{data[0]}'")
        tag_id = c.fetchone()
        if tag_id[0] == None:
            current_id = None
        else:
            current_id = int(tag_id[0])

        if selected_id != None:
            if selected_id == current_id:
                tags_filtered_data.append(data[0])
        else:
            tags_filtered_data.append(data[0])
    
    tags_filtered_data.pop(0)
    taglist_content = f"This is the list of tags for Mestionora bot.\n\n"
    last_page = ceil(len(tags_filtered_data)/10)

    if page == None or page <= 0:
        if last_page == 0:
            page = int(0)
        else:
            page = int(1)
    elif page > last_page:
        page = last_page

    caller = interaction.user
    async def button_callback(interaction):
        if interaction.user == caller:
            await get_page_taglist(client, interaction, page=page+1, set_member=set_member)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    async def button_callback2(interaction):
        if interaction.user == caller:
            await get_page_taglist(client, interaction, page=page-1, set_member=set_member)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    NextButton.callback = button_callback
    PrevButton.callback = button_callback2

    for data in tags_filtered_data[(((page*10)-10)):(10+((page*10)-10))]:
        c.execute(f"SELECT ID from tags where NAME = '{data}'")
        tag_id = c.fetchone()
        if tag_id[0] == None:
            current_id = None
        else:
            current_id = int(tag_id[0])

        guild = client.get_guild(interaction.guild.id)

        print(interaction.guild.id)
        print(guild)

        user = None
        member = None
        if current_id != None:
            member = guild.get_member(current_id)
            # user = client.get_user(current_id)
        if member:
            if member.nick != None:
                taglist_content += f"• **{data}** - {member.nick}\n"
            else:
                taglist_content += f"• **{data}** - {member.name}\n"
        # elif user and not member:
        #     #print("print user name")
        #     taglist_content += f"• **{data}** - {user.name}\n"
        elif current_id == None:
            #print("print none")
            taglist_content += f"• **{data}** - *None*\n"
        else:
            #print("print id")
            taglist_content += f"• **{data}** - {current_id}\n"
    
    embed = Embed(title=f"List of tags", description=f"{taglist_content}",color=0xf1c40f)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1027597999091753010/1029853959122325554/f9c0b03d3186867d4196e15dd8828606.png")
    embed.set_footer(text=f"Page ({page}/{last_page})")
    try:
        await interaction.response.edit_message(embed=embed, view=view)
    except:
        await interaction.response.send_message(embed=embed, view=view)
