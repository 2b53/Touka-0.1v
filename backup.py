import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignoriere die Nachrichten des Bots selbst

    # Überprüfe, ob die Nachricht ein Backup-Befehl ist
    if message.content.startswith('!backup'):
        await bot.process_commands(message)

@bot.command(name='backup')
async def backup(ctx):
    guild = ctx.guild
    channels = guild.channels
    members = guild.members
    roles = guild.roles

    backup_data = {
        'guild': guild.name,
        'channels': [{'name': channel.name, 'id': channel.id, 'type': str(channel.type)} for channel in channels],
        'members': [{'name': member.name, 'id': member.id} for member in members],
        'roles': [{'name': role.name, 'id': role.id, 'permissions': role.permissions.value} for role in roles]
    }

    with open('backup.json', 'w') as file:
        json.dump(backup_data, file)

    await ctx.send('Backup created successfully.')

@bot.command(name='restore')
async def restore(ctx):
    try:
        with open('backup.json', 'r') as file:
            backup_data = json.load(file)

        guild = ctx.guild

        # Restore channels
        for channel_data in backup_data['channels']:
            await guild.create_text_channel(name=channel_data['name'], id=channel_data['id'])

        # Restore roles
        for role_data in backup_data['roles']:
            await guild.create_role(name=role_data['name'], id=role_data['id'], permissions=discord.Permissions(
                permissions=role_data['permissions']))

        # Restore members
        for member_data in backup_data['members']:
            member = guild.get_member(member_data['id'])
            if member:
                await member.add_roles(guild.get_role(backup_data['roles'][0]['id']))  # Assign a default role
            else:
                await guild.create_member(name=member_data['name'], id=member_data['id'],
                                          roles=[guild.get_role(backup_data['roles'][0]['id'])])

        await ctx.send('Backup restored successfully.')

    except FileNotFoundError:
        await ctx.send('No backup found. Create a backup using !backup.')

bot.run('MTE5Mjg2NDY5NjI5OTE1OTU1Mg.Gw2r2x.NCw8D4dv5ZRztqElN1zVlfdBDgZhDeCiez8-8Q')
