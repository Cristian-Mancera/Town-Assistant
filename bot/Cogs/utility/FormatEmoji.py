import discord
from discord.ext import commands

class FormatEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="formatemoji", description="Gets the format of an emoji.")
    async def format_emoji(self, interaction: discord.Interaction, emoji: str):
        # Checks if the emoji is a custom emoji
        if emoji.startswith("<") and emoji.endswith(">"):
            # Extracts emoji information
            parts = emoji.strip("<>").split(":")
            if len(parts) == 3:
                emoji_name = parts[1]
                emoji_id = parts[2]
                is_animated = emoji.startswith("<a")
                emoji_format = f"<{'a' if is_animated else ''}:{emoji_name}:{emoji_id}>"

                await interaction.response.send_message(
                    content=f"API format for {emoji_format}:\n```{emoji_format}```",
                    ephemeral=True
                )

async def setup(bot):
    await bot.add_cog(FormatEmoji(bot))
