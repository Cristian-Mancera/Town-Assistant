import discord
from discord.ext import commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="serverinfo", description="Gets information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        humans = len([member for member in guild.members if not member.bot])
        bots = len([member for member in guild.members if member.bot])
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        roles = len(guild.roles) - 1  # Subtract 1 to exclude the @everyone role
        emojis = len(guild.emojis)
        static_emojis = len([emoji for emoji in guild.emojis if not emoji.animated])
        animated_emojis = len([emoji for emoji in guild.emojis if emoji.animated])
        stickers = len(guild.stickers)
        boosts = guild.premium_subscription_count
        boost_level = guild.premium_tier
        relative_time = discord.utils.format_dt(guild.created_at, style='R')
        
        embed = discord.Embed(
            title=f"{guild.name}",
            color=discord.Color(0xFFFFFF),
            timestamp=datetime.now()
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_image(url=guild.banner.url if guild.banner else None)

        embed.add_field(
            name="__General:__", 
            value=f"• ID: {guild.id}\n• Owner: {guild.owner.mention}\n• Created on: {guild.created_at.strftime('%d/%m/%Y')}\n• Relative time: {relative_time}", 
            inline=False
        )
        embed.add_field(
            name="__Members:__", 
            value=f"• Total: {guild.member_count}\n• Humans: {humans}\n• Bots: {bots}", 
            inline=False
        )
        embed.add_field(
            name="__Channels:__", 
            value=f"• Text: {text_channels}\n• Voice: {voice_channels}\n• Categories: {categories}", 
            inline=False
        )
        embed.add_field(name="__Boosts:__",
            value=f"• Level: {boost_level}\n• Count: {boosts}",
            inline=True
        )
        embed.add_field(
            name="__Others:__", 
            value=f"• Roles: {roles}\n• Emojis: {emojis}\n• Static: {static_emojis}\n• Animated: {animated_emojis}\n• Stickers: {stickers}", 
            inline=False
        )
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
