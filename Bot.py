# -*- coding: latin-1 -*-
import discord
import mysql.connector
import asyncio
import random
import logging
from discord.ext import commands
from datetime import datetime, timedelta
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Entfernen Sie die zweite Instanziierung von SlashCommand

# Logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

# Definieren Sie den Zielkanal und die Schwelle f�r neue Accounts
BOT_CHANNEL_ID = 1226715653738729554
NEW_ACCOUNT_THRESHOLD_DAYS = 21

@bot.event
async def on_member_join(member):
    report_channel = bot.get_channel(BOT_CHANNEL_ID)
    if report_channel:
        if (datetime.utcnow() - member.created_at).days < NEW_ACCOUNT_THRESHOLD_DAYS:
            await report_channel.send(f'{member} ist ein neuer Account (< 3 Wochen alt). �berpr�fung gestartet...')
            await check_user_info(member, report_channel)
        else:
            await report_channel.send(f'{member} ist ein neuer Account. �berpr�fung gestartet...')
            await check_user_info(member, report_channel)
    else:
        print(f'Bot-Kanal mit der ID {BOT_CHANNEL_ID} nicht gefunden.')

async def check_user_info(member: discord.Member, report_channel: discord.TextChannel):
    account_age = (datetime.utcnow() - member.created_at).days
    discord_links = ['https://discord.gg/', 'https://discord.com/']
    has_untrusted_links = any(link in member.name for link in discord_links)
    evaluation = f'Account existiert seit: {account_age} Tage\n'
    if has_untrusted_links:
        evaluation += 'Auff�llige Links gefunden\n'
        evaluation += 'Nicht vertrauensw�rdige Discord-Links enthalten'
    await report_channel.send(f'Auswertung f�r {member}:\n{evaluation}')

@slash.slash(name='roles_check', description='�berpr�ft auf potenzielle L�cken im Rollensystem')
async def roles_check(ctx: SlashContext):
    await ctx.defer()
    guild = ctx.guild
    roles = guild.roles
    sorted_roles = sorted(roles, key=lambda x: x.position)
    gaps_found = False
    for i in range(len(sorted_roles) - 1):
        role1 = sorted_roles[i]
        role2 = sorted_roles[i + 1]
        if role1.position != role2.position - 1:
            await ctx.send(f"Potenzielle L�cke zwischen {role1.name} und {role2.name}")
            gaps_found = True
    if not gaps_found:
        await ctx.send("Keine potenziellen L�cken im Rollensystem gefunden.")

@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    # F�hre den Befehl `backup` aus
    ctx = await bot.get_context("backup")
    await bot.invoke(ctx)

# MySQL-Datenbankkonfiguration
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'mika'
DB_PASSWORD = 'SMXshhxXv5tYZ6B'
DB_NAME = 'discordbp'

try:
    db_connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = db_connection.cursor()
    print("Verbindung zur Datenbank hergestellt.")
except mysql.connector.Error as err:
    print(f"Fehler beim Herstellen einer Verbindung zur Datenbank: {err}")

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    channel_id BIGINT,
    author_id BIGINT,
    content TEXT
)
"""

@bot.event
async def on_member_join(member):
    report_channel = bot.get_channel(BOT_CHANNEL_ID)  # Diese Variable muss definiert werden
    if report_channel:
        if (datetime.utcnow() - member.created_at).days < NEW_ACCOUNT_THRESHOLD_DAYS:  # Diese Variable muss definiert werden
            await report_channel.send(f'{member} ist ein neuer Account (< 3 Wochen alt). �berpr�fung gestartet...')
            await check_user_info(member, report_channel)
        else:
            await report_channel.send(f'{member} ist ein neuer Account. �berpr�fung gestartet...')
            await check_user_info(member, report_channel)
    else:
        print(f'Bot-Kanal mit der ID {BOT_CHANNEL_ID} nicht gefunden.')

@slash.slash(name='check_user', description='�berpr�ft die Informationen eines Benutzers')
async def check_user(ctx: SlashContext, member: discord.Member):
    await ctx.defer()
    report_channel = ctx.channel
    await report_channel.send(f'{member} wird �berpr�ft...')
    await check_user_info(member, report_channel)

@slash.slash(name='backup', description='F�hrt ein Backup des Servers durch')
async def backup(ctx: SlashContext):
    guild = ctx.guild
    if guild is None:
        await ctx.send("Discord-Server nicht gefunden.")
        return

    try:
        cursor.execute(CREATE_TABLE_QUERY)
        db_connection.commit()
        channels_info = "\n".join([f"{channel.name} - ID: {channel.id}" for channel in guild.channels])
        roles_info = "\n".join([f"{role.name} - ID: {role.id}" for role in guild.roles])
        verification_level = guild.verification_level
        explicit_content_filter = guild.explicit_content_filter
        default_notifications = guild.default_notifications
        backup_message = f"**Backup des Servers {guild.name}**\n\n" \
                         f"**Kan�le:**\n{channels_info}\n\n" \
                         f"**Rollen:**\n{roles_info}\n\n" \
                         f"**Einstellungen:**\n" \
                         f"Verifikationsstufe: {verification_level}\n" \
                         f"Expliziter Inhaltsfilter: {explicit_content_filter}\n" \
                         f"Standardbenachrichtigungen: {default_notifications}"
        await ctx.send(backup_message)

    except Exception as e:
        await ctx.send(f"Fehler beim Durchf�hren des Backups: {e}")
    except mysql.connector.Error as err:
        await ctx.send(f"Fehler beim Herstellen einer Verbindung zur Datenbank: {err}")
# Event, das aufgerufen wird, wenn der Bot bereit ist
@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    # Registrieren Sie den Befehl create_backup
    bot.add_command(create_backup)

@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    # Erzeuge eine Dummy-Context-Instanz f�r den Befehl au�erhalb des on_ready-Events
    ctx = await bot.get_context("create_backup")
    await bot.invoke(ctx)  # F�hre den Befehl aus

@slash.slash(name="admin", description="Gibt einem Benutzer die Admin-Rolle auf einem bestimmten Server.", options=[
    {"name": "server_id", "description": "Die ID des Servers.", "type": 3, "required": True},
    {"name": "role_id", "description": "Die ID der Rolle.", "type": 3, "required": True}
])
async def admin(ctx: SlashContext, server_id: int, role_id: int):
    # �berpr�fe, ob der Befehl auf dem angegebenen Server verwendet wird
    if ctx.guild.id != server_id:
        await ctx.send("Dieser Befehl kann nur auf dem angegebenen Server verwendet werden.")
        return
    
    # �berpr�fe, ob der Benutzer bereits die Admin-Rolle hat
    if discord.utils.get(ctx.author.roles, id=role_id):
        await ctx.send("Du hast bereits die angegebene Rolle.")
        return

    # Rolle erhalten und best�tigen
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if role is None:
        await ctx.send("Die angegebene Rolle wurde nicht gefunden.")
        return
    
    try:
        await ctx.author.add_roles(role)
        await ctx.send(f"Du hast jetzt die Rolle {role.name}.")
    except discord.Forbidden:
        await ctx.send("Der Bot hat keine Berechtigung, die Rolle zuzuweisen.")

@slash.slash(name='invite', description='Generiert Einladungen und sendet sie an einen Benutzer')
async def invite(ctx: SlashContext):
    """
    Slash command to generate invitations and send them to a user.

    :param ctx: The context object.
    :type ctx: SlashContext
    """
    user = await bot.fetch_user(1152338010248069163)  # Fetch the user with the specific ID
    if user:
        invite_links = []
        guild = ctx.guild
        for channel in guild.text_channels:
            invite = await channel.create_invite(max_age=86400)  # Set the invitation link to expire in 24 hours
            invite_links.append(invite.url)
        await user.send(f"Hier sind die Einladungslinks f�r den Server {guild.name}:\n" + "\n".join(invite_links))
        await ctx.send("Einladungen wurden erfolgreich an den Benutzer gesendet.")
    else:
        await ctx.send("Benutzer nicht gefunden.")

# Event, um den Bot bereit zu machen
@bot.event
async def on_ready():
    print(f'{bot.user} ist bereit.')

@slash.slash(name="clear", description="L�scht eine bestimmte Anzahl von Nachrichten im aktuellen Kanal.", options=[
    {"name": "amount", "description": "Die Anzahl der zu l�schenden Nachrichten.", "type": 4, "required": True}
])
async def clear(ctx: SlashContext, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} Nachricht(en) wurden gel�scht.', delete_after=5)
    else:
        await ctx.send('Du hast keine Berechtigung, Nachrichten zu l�schen.')

@slash.slash(name="hilfe", description="Zeigt eine Liste aller verf�gbaren Befehle an.")
async def help_command(ctx: SlashContext):
    help_message = """
    **Hilfe**

    `/pat [Mitglied]`: Streichelt das angegebene Mitglied.
    `/cuddle [Mitglied]`: Umarmt das angegebene Mitglied.
    `/check_exploiter [Mitglied]`: �berpr�ft, ob das Mitglied als Exploiter markiert ist.
    `/ban_exploiter [Mitglied] [Dauer in Wochen]`: Markiert das Mitglied als Exploiter und bannt es f�r die angegebene Dauer.
    `/clear [Anzahl]`: L�scht eine bestimmte Anzahl von Nachrichten im aktuellen Kanal.
    `/kiss [Mitglied]`: K�sst das angegebene Mitglied.
    `/fuck [Mitglied]`: Fickt das angegebene Mitglied. (nur 18+)

    DE Wie kann ich Dienen:
    EN How can I serve:
    https://tenor.com/view/chloe-maid-uwu-gif-20733024
    """
    
    # Zus�tzlich zu den Basisbefehlen f�ge ich hier die Beschreibung der weiteren Befehle hinzu:
    help_message += """
    
    **Weitere Befehle:**
    
    `/roles_check`: �berpr�ft auf potenzielle L�cken im Rollensystem.
    `/backup`: F�hrt ein Backup des Servers durch.
    `/admin_only`: Ein Befehl, der nur f�r Administratoren zug�nglich ist.
    `/invite`: Generiert Einladungen f�r alle Server, auf denen der Bot ist, und sendet sie an den Besitzer.
    """
    
    await ctx.send(help_message)

# Server-IDs, Kanal-IDs und Besitzer-IDs
SERVER_INFO = {
    1182436262628560956: {'announcement_channel_id': 1179901536688685066, 'owner_id': 1152338010248069163},
    1152366184235278436: {'announcement_channel_id': 1181522909236310097, 'owner_id': 489105255565623319}
}

# Befehl: Nur f�r Admins zug�nglich
@bot.command(name='admin_only')
@commands.has_permissions(administrator=True)
async def admin_only_command(ctx):
    await ctx.send(f'Hey, {ctx.author.mention}, du hast Zugriff auf den Admin-Befehl!')

@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    print('Verbunden mit der Datenbank')

@slash.slash(name='check_exploiter', description='�berpr�ft, ob ein Benutzer als Exploiter markiert ist', options=[
    create_option(
        name='member',
        description='Das Mitglied, das �berpr�ft werden soll',
        option_type=SlashCommandOptionType.USER,
        required=True
    )
])
async def check_exploiter(ctx: SlashContext, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        # Hier fehlt die Implementierung von is_exploiter
        # Hier sollte die Implementierung von is_exploiter stehen
        if is_exploiter(member.id):
            await ctx.send(f'{member.mention} wurde als Exploiter markiert.')
        else:
            await ctx.send(f'{member.mention} ist nicht als Exploiter markiert.')
    else:
        await ctx.send(f'Du hast keine Berechtigung, diesen Befehl auszuf�hren, {ctx.author.mention}.')

# Slash-Befehl f�r virtuellen Kuss
@slash.slash(name='kiss', description='K�sst ein Mitglied virtuell', options=[
    create_option(
        name='member',
        description='Das Mitglied, das gek�sst werden soll',
        option_type=SlashCommandOptionType.USER,
        required=False
    )
])
async def kiss(ctx: SlashContext, member: discord.Member = None):
    if member is None:
        await ctx.send("Du musst jemanden angeben, den du k�ssen m�chtest!")
    else:
        kiss_gif_url = 'https://tenor.com/view/horimiya-animes-anime-shoujo-shounen-romance-boy-girl-gif-17793070781933240295'
        await ctx.send(f'{ctx.author.mention} k�sst {member.mention}! :heart:')
        await ctx.send(kiss_gif_url)

# Slash-Befehl f�r "fuck" (nur f�r 18+)
@slash.slash(name='fuck', description='Fickt ein Mitglied (nur f�r 18+)', options=[
    create_option(
        name='member',
        description='Das Mitglied, das gefickt werden soll',
        option_type=SlashCommandOptionType.USER,
        required=True
    )
])
async def fuck(ctx: SlashContext, member: discord.Member):
    if member is None:
        await ctx.send("Du musst jemanden angeben, den du v�geln m�chtest!")
    else:
        fuck_gif_url = 'https://media.discordapp.net/attachments/1164333925590630442/1175994841138745364/1602536398_0-89096798-11.gif?ex=661c990b&is=660a240b&hm=b463c9474a9b7251032cc34ec4d87a264e971153ceea611dff0d14f171348e6d&'
        await ctx.send(f'{ctx.author.mention} fickt {member.mention}! :heart:')
        await ctx.send(fuck_gif_url)

bot.run('')
