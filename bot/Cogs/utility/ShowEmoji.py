import discord
from discord.ext import commands
from datetime import datetime

class ShowEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="show", description="Gets information about an emoji.")
    async def show(self, interaction: discord.Interaction, emoji: str):
        
        if emoji.startswith("<") and emoji.endswith(">"):
            parts = emoji.strip("<>").split(":")
            if len(parts) == 3:
                emoji_name = parts[1]
                emoji_id = parts[2]
                is_animated = emoji.startswith("<a")
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if is_animated else 'png'}"

                emoji_obj = self.bot.get_emoji(int(emoji_id))
                embed = discord.Embed(
                    title=f"Emoji Information",
                    description=f"",
                    color=discord.Color(0xFFFFFF),
                    timestamp=datetime.now()
                )

                embed.set_thumbnail(url=emoji_url)

                embed.add_field(name="**Name**", value=emoji_name, inline=True)
                embed.add_field(name="**Animated**", value="Yes" if is_animated else "No", inline=True)
                embed.add_field(name="**ID**", value=emoji_id, inline=True)

                if emoji_obj:
                    uploaded_at = emoji_obj.created_at
                    uploaded_relative = discord.utils.format_dt(uploaded_at, "R")  # Relative date
                    embed.add_field(name="**Uploaded**", value=uploaded_at.strftime('%d/%m/%Y'), inline=True)
                    embed.add_field(name="**Relative**", value=uploaded_relative, inline=True)

                if not emoji_obj:
                    embed.add_field(name="**Uploaded**", value="N/A", inline=True)
                    embed.add_field(name="**Relative**", value="N/A", inline=True)

                embed.add_field(name="**URL**", value=emoji_url, inline=False)

                download_button = discord.ui.Button(label="Download Emoji", url=emoji_url)
                view = discord.ui.View()
                view.add_item(download_button)

                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)

                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.response.send_message("Invalid emoji format. Please use the format <:emoji_name:emoji_id>.", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid emoji format. Please use the format <:emoji_name:emoji_id>.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ShowEmoji(bot))
