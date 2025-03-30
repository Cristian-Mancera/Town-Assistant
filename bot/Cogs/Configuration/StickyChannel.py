import discord
from discord.ext import commands
import json
import os

class Sticky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='stickycreate', description='Creates a sticky message in a specific channel.')
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def stickycreate(self, interaction: discord.Interaction, title: str, description: str, 
                           image: str = None, thumbnail: str = None, color: int = 0xFFFFFF):
        description = description.replace('  ', '\n')

        embed = discord.Embed(title=title, description=description, color=color)

        if image:
            embed.set_image(url=image)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        message = await interaction.channel.send(embed=embed)

        guild_id = str(interaction.guild.id)
        sticky_data = self.load_sticky_data()

        if guild_id not in sticky_data:
            sticky_data[guild_id] = []

        sticky_data[guild_id].append({
            'message_id': message.id,
            'channel_id': interaction.channel.id,
            'title': title,
            'description': description,
            'image': image,
            'thumbnail': thumbnail,
            'color': color
        })

        self.save_sticky_data(sticky_data)

        await interaction.response.send_message(f"Sticky message created in <#{interaction.channel.id}>.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        guild_id = str(message.guild.id)
        sticky_data = self.load_sticky_data()

        if guild_id in sticky_data:
            for sticky in sticky_data[guild_id]:
                if sticky['channel_id'] == message.channel.id:
                    channel = message.channel
                    try:
                        sticky_message = await channel.fetch_message(sticky['message_id'])
                        await sticky_message.delete()

                        embed = discord.Embed(
                            title=sticky['title'], 
                            description=sticky['description'], 
                            color=sticky['color']
                        )
                        if sticky['image']:
                            embed.set_image(url=sticky['image'])
                        if sticky['thumbnail']:
                            embed.set_thumbnail(url=sticky['thumbnail'])

                        new_message = await channel.send(embed=embed)
                        sticky['message_id'] = new_message.id
                        self.save_sticky_data(sticky_data)
                    except discord.NotFound:
                        pass

    def load_sticky_data(self):
        if not os.path.exists('../Data/Sticky.json') or os.path.getsize('../Data/Sticky.json') == 0:
            return {}
        
        try:
            with open('../Data/Sticky.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_sticky_data(self, data):
        with open('../Data/Sticky.json', 'w') as f:
            json.dump(data, f, indent=4)

    @discord.app_commands.command(name='stickydelete', description='Deletes a sticky message in a specific channel.')
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def stickydelete(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        sticky_data = self.load_sticky_data()

        if guild_id not in sticky_data or not sticky_data[guild_id]:
            await interaction.response.send_message("No sticky messages found on this server.", ephemeral=True)
            return

        options = []
        for sticky in sticky_data[guild_id]:
            channel = interaction.guild.get_channel(sticky['channel_id'])
            options.append(discord.SelectOption(
                label=f"#{channel.name[:99]}", 
                description=f"{sticky['title'][:75]} - {sticky['description'][:75]}", 
                value=str(sticky['message_id'])
            ))

        select = discord.ui.Select(
            placeholder="Select the sticky message to delete...",
            options=options
        )

        async def select_callback(interaction: discord.Interaction):
            message_id = int(select.values[0])
            channel_id = sticky_data[guild_id][0]['channel_id']
            channel = interaction.guild.get_channel(channel_id)

            try:
                message = await channel.fetch_message(message_id)
                await message.delete()
            except discord.NotFound:
                pass

            sticky_data[guild_id] = [sticky for sticky in sticky_data[guild_id] if sticky['message_id'] != message_id]
            self.save_sticky_data(sticky_data)

            await interaction.response.send_message(f"Sticky message deleted from <#{interaction.channel.id}>.", ephemeral=True)

        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message("Select a sticky message to delete:", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Sticky(bot))