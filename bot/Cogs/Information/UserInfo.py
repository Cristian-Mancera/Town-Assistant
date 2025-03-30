import discord
from discord.ext import commands
from datetime import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def member_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=member.display_name, value=str(member.id))
            for member in interaction.guild.members
            if current.lower() in member.display_name.lower()
        ][:25]

    @discord.app_commands.command(name="userinfo", description="Displays information about a user.") 
    @discord.app_commands.describe(user="Select a server member or provide a user ID.")
    @discord.app_commands.autocomplete(user=member_autocomplete)
    async def userinfo(self, interaction: discord.Interaction, user: str = None):
    
        target_user = interaction.user

        if user:
            try:
                server_member = interaction.guild.get_member(int(user)) if user.isdigit() else None
                if server_member:
                    target_user = server_member
                else:
                    target_user = await self.bot.fetch_user(int(user))
            except ValueError:
                await interaction.response.send_message(
                    "Invalid user ID. Please provide a valid user ID.", ephemeral=True
                )
                return
            except discord.NotFound:
                await interaction.response.send_message(
                    "User not found. Please provide a valid user ID.", ephemeral=True
                )
                return

        embed = discord.Embed(
            title=f"{target_user.display_name}",
            color=discord.Color(0xFFFFFF),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)

        embed.add_field(
            name="__General:__",
            value=f"• ID: {target_user.id}\n• Username: @{target_user.name}\n• Mention: {target_user.mention}",
            inline=False
        )

        embed.add_field(
            name="__Created on:__",
            value=f"• Date: {target_user.created_at.strftime('%d/%m/%Y')} ({discord.utils.format_dt(target_user.created_at, 'R')})",
            inline=False
        )

        if isinstance(target_user, discord.Member):
            roles = [role.mention for role in sorted(target_user.roles, key=lambda r: r.position, reverse=True) if role != interaction.guild.default_role]
            roles_count = len(roles)

            embed.add_field(
                name="__Joined on:__",
                value=f"• Date: {target_user.joined_at.strftime('%d/%m/%Y')} ({discord.utils.format_dt(target_user.joined_at, 'R')})",
                inline=False
            )
            embed.add_field(
                name=f"Roles [{roles_count}]",
                value="\n".join([f"• {role}" for role in roles]) if roles else "",
                inline=False
            )

        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
