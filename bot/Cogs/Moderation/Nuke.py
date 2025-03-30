import discord
from discord.ext import commands
import asyncio

class ConfirmNukeView(discord.ui.View):
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.result = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to confirm this action.", ephemeral=True)
            return

        self.result = True
        self.stop()  
        await interaction.response.defer() 

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You are not authorized to cancel this action.", ephemeral=True)
            return

        self.result = False
        self.stop() 
        await interaction.response.defer()  

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="nuke", description="Clones and deletes a channel.")
    @discord.app_commands.checks.has_permissions(manage_channels=True)  
    async def nuke(self, interaction: discord.Interaction):
        
        if not interaction.guild.me.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "I do not have permission to manage channels.",
                ephemeral=True
            )
            return

        view = ConfirmNukeView(interaction.user)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Are you sure?",
                description=f"Proceeding will permanently delete all messages in {interaction.channel.mention}. This action cannot be undone.",
                color=discord.Color.from_rgb(255, 0, 0),
            ),
            view=view,
            ephemeral=True
        )

        await view.wait()

        if view.result is None:
            await interaction.followup.send("The Nuke request has expired.", ephemeral=True)
            return

        if not view.result:
            await interaction.followup.send("Nuke canceled.", ephemeral=True)
            return

        channel = interaction.channel
        position = channel.position  
        category = channel.category  

        try:
            new_channel = await channel.clone()
            await new_channel.edit(position=position, category=category)

            await channel.delete()

            nuke_message = await new_channel.send(f"**Channel nuked by {interaction.user.mention}.**")
            await asyncio.sleep(10)  # Wait 10 seconds
            await nuke_message.delete()  # Delete the message
        except discord.Forbidden:
            await interaction.followup.send(
                "I do not have permission to delete this channel.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"An error occurred while deleting the channel: {e}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Nuke(bot))
