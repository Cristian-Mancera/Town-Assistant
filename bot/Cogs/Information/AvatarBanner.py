import discord
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="avatar", description="Gets a user's avatar.")
    @discord.app_commands.describe(user="Select a server member or provide a user ID.")
    async def avatar(self, interaction: discord.Interaction, user: str = None):

        try:
            target_user = None

            if user:
                member = discord.utils.get(interaction.guild.members, display_name=user) or \
                         discord.utils.get(interaction.guild.members, name=user)
                if member:
                    target_user = member
                else:
                    try:
                        target_user = await self.bot.fetch_user(int(user))
                    except ValueError:
                        await interaction.response.send_message(
                            "The input must be a valid username or ID.", ephemeral=True
                        )
                        return
            else:
                target_user = interaction.user

            embed = discord.Embed(
                title=f"{target_user.display_name}'s Avatar",
                color=discord.Color(0xFFFFFF),
                timestamp=datetime.now()
            )

            embed.set_image(url=target_user.avatar.url if target_user.avatar else None)

            avatar_button = Button(label="Avatar", style=discord.ButtonStyle.primary, custom_id="avatar")
            banner_button = Button(label="Banner", style=discord.ButtonStyle.secondary, custom_id="banner")

            async def avatar_callback(interaction: discord.Interaction):
                embed.title = f"{target_user.display_name}'s Avatar"
                embed.set_image(url=target_user.avatar.url if target_user.avatar else None)
                if not interaction.response.is_done():
                    await interaction.response.edit_message(embed=embed, view=view)

            async def banner_callback(interaction: discord.Interaction):
                target_user_full = await self.bot.fetch_user(target_user.id)
                try:
                    if target_user_full.banner:
                        embed.title = f"{target_user.display_name}'s Banner"
                        embed.set_image(url=target_user_full.banner.url)
                        # Solo editamos el mensaje si no se ha respondido previamente
                        if not interaction.response.is_done():
                            await interaction.response.edit_message(embed=embed, view=view)
                    else:
                        embed.title = f"{target_user.display_name}'s Banner"
                        embed.set_image(url=None)
                        # Solo respondemos si no se ha respondido previamente
                        if not interaction.response.is_done():
                            await interaction.response.send_message("This user does not have a banner.", ephemeral=True)
                except Exception as e:
                    embed.title = "No Banner Found"
                    embed.set_image(url=None)
                    # Solo respondemos si no se ha respondido previamente
                    if not interaction.response.is_done():
                        await interaction.response.send_message(f"Error fetching the banner: {str(e)}", ephemeral=True)

                # Solo editamos el mensaje si no se ha respondido previamente
                if not interaction.response.is_done():
                    await interaction.response.edit_message(embed=embed, view=view)

            avatar_button.callback = avatar_callback
            banner_button.callback = banner_callback

            view = View(timeout=180)  
            view.add_item(avatar_button)
            view.add_item(banner_button)

            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed, view=view)

        except discord.NotFound:
            await interaction.response.send_message("The provided user ID is not valid or does not exist.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have sufficient permissions to retrieve this user's avatar or banner.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {str(e)}", ephemeral=True)

    @avatar.autocomplete("user")
    async def user_autocomplete(self, interaction: discord.Interaction, current: str):
        members = [
            member for member in interaction.guild.members
            if current.lower() in member.display_name.lower()
        ]
        return [
            discord.app_commands.Choice(name=member.display_name, value=str(member.id))
            for member in members[:5]
        ]

async def setup(bot):
    await bot.add_cog(Avatar(bot))
