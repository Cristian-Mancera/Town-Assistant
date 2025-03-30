import re
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime

class Copy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="copy", description="Copies an emoji from another server to the current server.")
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def copy_emoji(self, interaction: discord.Interaction, emojis: str):

        emoji_list = emojis.split()  # Splits the provided emojis by spaces

        # Ensure there are between 1 and 10 emojis
        if len(emoji_list) < 1 or len(emoji_list) > 10:
            await interaction.response.send_message(
                "Please provide between 1 and 10 emojis.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)  # Defer the response to avoid the time limit

        for emoji_or_url in emoji_list:
            try:
                # Try extracting the ID and name if it's in the format <:name:ID> or <a:name:ID>
                match = re.match(r"<a?:(\w+):(\d+)>", emoji_or_url)
                if match:
                    name = match.group(1)
                    emoji_id = match.group(2)
                    is_animated = emoji_or_url.startswith("<a:")
                    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if is_animated else 'png'}"
                elif emoji_or_url.isdigit():
                    # If it's a direct ID, use a generic name
                    name = f"emoji_{emoji_or_url}"
                    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_or_url}.png"
                else:
                    # Consider it as a direct URL and use a generic name based on time
                    name = f"emoji_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    emoji_url = emoji_or_url

                # Create an HTTP session to download the emoji
                async with aiohttp.ClientSession() as session:
                    async with session.get(emoji_url) as response:
                        if response.status != 200:
                            await interaction.followup.send(
                                f"Failed to retrieve the emoji `{emoji_or_url}`. Please check the URL, ID, or provided emoji.",
                                ephemeral=True
                            )
                            continue

                        # Get the emoji data
                        emoji_data = await response.read()

                        # Try adding the emoji to the server
                        new_emoji = await interaction.guild.create_custom_emoji(name=name, image=emoji_data)

                        # Generate the format to display the emoji
                        emoji_display = f"<{'a' if new_emoji.animated else ''}:{new_emoji.name}:{new_emoji.id}>"

                        # Respond with success, showing the emoji
                        await interaction.followup.send(
                            f"Emoji successfully copied to the server: {emoji_display}",
                            ephemeral=True
                        )

            except discord.HTTPException as e:
                await interaction.followup.send(
                    f"Discord error while copying the emoji `{emoji_or_url}`: {str(e)}",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.followup.send(
                    f"Unexpected error while copying the emoji `{emoji_or_url}`: {str(e)}",
                    ephemeral=True
                )

async def setup(bot):
    await bot.add_cog(Copy(bot))
