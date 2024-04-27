import discord
from discord.ext import commands
import sqlalchemy as sa

from src import Session
from src.models import Club, ClubMember


class Clubs(commands.GroupCog, name="club", description="Commands to manage clubs."):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @discord.app_commands.command(description="Create a club", name="create")
    @discord.app_commands.describe(name="The name of the club to create")
    async def create_club(self, interaction: discord.Interaction, name: str):
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

    @discord.app_commands.command(description="Delete a club", name="delete")
    @discord.app_commands.describe(name="The name of the club to delete")
    async def delete_club(self, interaction: discord.Interaction, name: str):
        """Delete a club. This will remove all members from the club."""
        name = name.lower()

        if (
            interaction.guild is None
            or interaction.channel is None
            or not isinstance(interaction.user, discord.Member)
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

    @discord.app_commands.command(description="Join a club", name="join")
    @discord.app_commands.describe(name="The name of the club to join")
    async def join_club(self, interaction: discord.Interaction, name: str):
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

    @discord.app_commands.command(description="Leave a club", name="leave")
    @discord.app_commands.describe(name="The name of the club to leave")
    async def leave_club(self, interaction: discord.Interaction, name: str):
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
                    ClubMember.user_id == interaction.user.id,
                    ClubMember.club_id == club.id,
                )
            )

        await interaction.response.send_message(
            ephemeral=True,
            content=f"Left club {name}",
        )

    @discord.app_commands.command(description="List all clubs in a server", name="list")
    async def list_clubs(self, interaction: discord.Interaction):
        current_channel = f"{interaction.channel}"
        if current_channel == "bots" or current_channel == "🐍-bots":
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

                embed = discord.Embed(
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

                embed = discord.Embed(
                    title="Clubs",
                    description=description,
                    color=0xF1C40F,
                )
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=embed,
                )

    @discord.app_commands.command(description="Publish to a club", name="publish")
    @discord.app_commands.describe(name="The name of the club to publish to")
    async def publish_to_club(self, interaction: discord.Interaction, name: str):
        """Publish a thread to a club.
        This will add all the members of this club to this thread, which gives them a notification.
        """
        name = name.lower()

        guild = interaction.guild
        channel = interaction.channel
        author = interaction.user

        if (
            guild is None
            or channel is None
            or not isinstance(channel, discord.Thread)
            or not isinstance(author, discord.Member)
        ):
            return await interaction.response.send_message(
                ephemeral=True,
                content="This command must be used in a thread in a server.",
            )

        # For typing purposes, now that the above has passed, we can assert the checks

        with Session.begin() as session:
            club = session.execute(
                sa.select(Club).filter(Club.name == name, Club.guild_id == guild.id)
            ).scalar_one_or_none()

            if not club:
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f"Club {name} does not exist",
                )

            if (
                club.creator_id != author.id
                and not author.guild_permissions.manage_threads
            ):
                return await interaction.response.send_message(
                    ephemeral=True,
                    content=f"You are not the creator of club {name}",
                )

            await interaction.response.defer()

            # Pin the first message if it exists, and we have permission to do so
            if (
                channel.starter_message
                and channel.permissions_for(guild.me).manage_messages
            ):
                await channel.starter_message.pin()

            async def consolidate_members():
                # Find all the members that aren't in the thread, and add them
                members = await channel.fetch_members()
                members_in_channel = {member.id for member in members}
                club_members = {member.user_id for member in club.members}

                for member_id in club_members.difference(members_in_channel):
                    try:
                        await channel.add_user(discord.Object(id=member_id))
                    except Exception:
                        print("Error adding user:", member_id)

            # For some reason discord seems to be dropping some of the people we add to the thread
            #  so perform this action twice to ensure everyone is added
            await consolidate_members()
            await consolidate_members()

            await interaction.edit_original_response(
                content=f"Added everyone from club {name}"
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clubs(bot))
