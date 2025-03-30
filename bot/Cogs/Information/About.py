import discord
from discord.ext import commands
from datetime import datetime

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="about", description="Get information about the bot.")
    async def about(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="Bot Information",
            description="",
            color=discord.Color.from_rgb(255, 255, 255),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="__General:__",
            value=f"• ID: {interaction.client.user.id}\n• Name: {interaction.client.user.name}\n• Mention: {interaction.client.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="__Developer:__",
            value="• @cristian.pve",  
            inline=False
        )
        
        embed.add_field(
            name="__Ping:__",
            value=f"• {latency} ms", 
            inline=False
        )
        
        embed.add_field(
            name="__Commands:__",
            value="• `/help` to see available commands.",
            inline=False
        )
        
        embed.add_field(
            name="__Support Server:__",
            value="• [Join here](https://discord.gg/VzSMQHfKVs)",
            inline=False
        )

        footer_text = f"{interaction.user.name}"
        footer_icon = interaction.user.avatar.url if interaction.user.avatar else self.bot.user.avatar.url
        embed.set_footer(text=footer_text, icon_url=footer_icon)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
