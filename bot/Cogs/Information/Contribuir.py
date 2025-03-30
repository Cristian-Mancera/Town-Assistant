import discord
from discord.ext import commands
from datetime import datetime

class Contribute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="contribute", description="Support the bot through donations and join our community!")
    async def contribute(self, interaction: discord.Interaction):
        
        embed = discord.Embed(
            title="Support Town Assistant",
            description=(
                "🌟 Help us keep the bot running and improving! "
                "Your contributions allow us to maintain and develop new features.\n\n"
                "💖 **Donate here:** [Support Us](https://town.mysellauth.com/product/donations)\n"
                "📢 **Join our community:** [Discord Server](https://discord.gg/VzSMQHfKVs)"
            ),
            color=discord.Color(0xFFFFFF),
            timestamp=datetime.now()
        )

        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Contribute(bot))
