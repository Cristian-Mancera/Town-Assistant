import discord
from datetime import datetime
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Displays the list of available commands.")
    async def help(self, interaction: discord.Interaction):
        # Dynamic title with the bot's name and mention
        embed = discord.Embed(
            title="Available Commands",
            description="",
            color=discord.Color(0xFFFFFF),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="General Commands:",
            value=(
                "• `/about` → Get information about the bot.\n"
                "• `/avatar` → Get a user's avatar/banner.\n"
                "• `/userinfo` → Get information about a user.\n"
                "• `/contribute` → Support the bot through donations and join our community!\n"
                "• `/serverinfo` → Get information about the server.\n"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Utility Commands:",
            value=(
                "• `/copy` → Copy an emoji from one server to the current server.\n"
                "• `/embed` → Create an embed message from scratch.\n"
                "• `/show` → Get information about an emoji.\n"
                "• `/formatchannel` → Get the format of a channel.\n"
                "• `/formatemoji` → Get the format of an emoji.\n"
                "• `/formatrole` → Get the format of a role.\n"
            ),
            inline=False
        )   
        
        embed.add_field(
            name="Moderation Commands:",
            value=( 
                "`/say` → Sends a message through the bot.\n"
                "`/ban` → Permanently ban a user from the server.\n"
                "`/unban` → Revoke a user's ban.\n"
                "`/kick` → Remove a user from the server.\n"
                "`/nuke` → Delete the channel and clone it to remove pings.\n"
                "`/purge` → Delete a specified number of messages.\n"
                "`/timeout` → Temporarily mute a user.\n"
                "`/addrole` → Assign a role to a user.\n"

            ),
            inline=False
        )  

        embed.add_field(
            name="Configuration Commands:",
            value=( 
                "`/autoroleadd` → Assign an automatic role to new server members.\n"
                "`/autoroleremove` → Remove the automatic role configuration.\n"
                "`/counterchannel` → Set up the counting channel.\n"
                "`/stickycreate` → Create a pinned message in a specific channel.\n"
                "`/stickydelete` → Remove a pinned message from a specific channel.\n"
            ),
            inline=False
        )

        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))