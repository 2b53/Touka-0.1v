# -*- coding: latin-1 -*-
import discord
import mysql.connector
import asyncio
import random
import logging
from discord.ext import commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext  # Import für cog_ext hinzugefügt

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Entfernen Sie die zweite Instanziierung von SlashCommand

# Definieren Sie den Zielkanal und die Schwelle ür neue Accounts
BOT_CHANNEL_ID = 1226715653738729554
NEW_ACCOUNT_THRESHOLD_DAYS = 21

@bot.event
async def on_ready():
    print("Bot is ready.")

bot = commands.Bot(command_prefix='/')
MAX_LATENCY_THRESHOLD = 500  # Schwellenwert für maximale Latenzzeit in Millisekunden

@bot.event
async def on_ready():
    print(f'Bot ist bereit. Die Latenzzeit beträgt: {bot.latency * 1000} ms')
    # Starte die Latenzzeitüberwachung
    latency_check.start()

@tasks.loop(minutes=5)  # Überprüfe alle 5 Minuten
async def latency_check():
    latency = bot.latency * 1000  # Latenzzeit in Millisekunden
    print(f'Latenzzeit: {latency} ms')
    if latency > MAX_LATENCY_THRESHOLD:
        await handle_high_latency(latency)

async def handle_high_latency(latency):
    # Aktion bei hoher Latenzzeit ausführen, z.B. eine Benachrichtigung senden
    developer = await bot.fetch_user(YourDeveloperID)
    if developer:
        await developer.send(f"Achtung! Hohe Bot-Latenzzeit: {latency} ms. Möglicherweise gibt es Probleme.")
    # Weitere Aktionen hier, z.B. Versuch, die Ursache der Latenzzeit zu ermitteln oder den Bot neu zu starten

# Benutzerdefinierte Datenstruktur für Slash-Befehle
class SlashCommandInfo:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Definiere alle Slash-Befehle hier
slash_commands = [
    SlashCommandInfo(name="command1", description="Description of command1"),
    SlashCommandInfo(name="command2", description="Description of command2"),
    # Weitere Befehle hier hinzufügen
]

# Dummy-Funktionen erstellen und Befehle hinzufügen
for cmd_info in slash_commands:
    @slash.slash(name=cmd_info.name, description=cmd_info.description)
    async def dummy_command(ctx: SlashContext):
        await ctx.send(f"{ctx.author.mention}, Dummy command: {cmd_info.name}")

@bot.event
async def on_ready():
    print("Bot is ready.")

@slash.slash(
    name="check_cmds",
    description="Prüft die Funktionsfähigkeit aller Slash-Befehle.",
)
async def check_cmds(ctx: SlashContext):
    results = {}

    for cmd_info in slash_commands:
        try:
            # Führe den Befehl aus, um zu überprüfen, ob er funktioniert
            await bot.get_command(cmd_info.name).callback(ctx)
            results[cmd_info.name] = "Successful"
        except Exception as e:
            results[cmd_info.name] = f"Error: {e}"

    await ctx.send("Prüfung der Slash-Befehle abgeschlossen. Hier sind die Ergebnisse:")
    for command, result in results.items():
        await ctx.send(f"{command}: {result}")

async def check_user_info(member: discord.Member, report_channel: discord.TextChannel):
    account_age = (datetime.utcnow() - member.created_at).days
    discord_links = ['https://discord.gg/', 'https://discord.com/']
    has_untrusted_links = any(link in member.name for link in discord_links)
    evaluation = f'Account existiert seit: {account_age} Tage\n'
    if has_untrusted_links:
        evaluation += 'Auffällige Links gefunden\n'
        evaluation += 'Nicht vertrauenswürdige Discord-Links enthalten'
    await report_channel.send(f'Auswertung für {member}:\n{evaluation}')

@slash.slash(name='roles_check', description=' überprüft auf potenzielle Lücken im Rollensystem')
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
            await ctx.send(f"Potenzielle Lücke zwischen {role1.name} und {role2.name}")
            gaps_found = True
    if not gaps_found:
        await ctx.send("Keine potenziellen Lücken im Rollensystem gefunden.")

@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    # F hre den Befehl `backup` aus
    ctx = await bot.get_context("backup")
    await bot.invoke(ctx)

# MySQL-Datenbankkonfiguration
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'Touka'
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

class AdminCommandInfo:
    def __init__(self, name, description):
        self.name = name
        self.description = description

bot = commands.Bot(command_prefix='/')
BOT_CHANNEL_ID = 1234567890  # Replace with your actual channel ID
NEW_ACCOUNT_THRESHOLD_DAYS = 21
required_role_ids = [1225167417265750128, 1110550747453591593, 374155120952475648]

@bot.event
async def on_message(message):
    if any(role.id in required_role_ids for role in message.author.roles):
        gif_url = "https://tenor.com/view/smug-smile-he-he-he-elf-frieren-gif-5058064641539350421"
        await message.channel.send(f"{gif_url}\nTry it, du bist nicht mein Meister")
    else:
        await message.add_reaction("??")

@bot.event
async def on_member_join(member):
    report_channel = bot.get_channel(BOT_CHANNEL_ID)
    if report_channel:
        if (datetime.utcnow() - member.created_at).days < NEW_ACCOUNT_THRESHOLD_DAYS:
            await report_channel.send(f'{member} ist ein neuer Account (< 3 Wochen alt). Überprüfung gestartet...')
            await check_user_info(member, report_channel)
        else:
            await report_channel.send(f'{member} ist ein neuer Account. Überprüfung gestartet...')
            await check_user_info(member, report_channel)
    else:
        print(f'Bot-Kanal mit der ID {BOT_CHANNEL_ID} nicht gefunden.')

async def check_user_info(member, report_channel):
    # Implement your logic for checking user information here
    pass

@cog_ext.cog_slash(name='check_user', description='Überprüft die Informationen eines Benutzers')
async def check_user(ctx: SlashContext, member: discord.Member):
    await ctx.defer()
    report_channel = ctx.channel
    await report_channel.send(f'{member} wird überprüft...')
    await check_user_info(member, report_channel)

@cog_ext.cog_slash(name='backup', description='Führt ein Backup des Servers durch')
async def backup(ctx: SlashContext):
    guild = ctx.guild
    if guild is None:
        await ctx.send("Discord-Server nicht gefunden.")
        return
    # Implement your backup logic here
    try:
        cursor.execute(CREATE_TABLE_QUERY)
        db_connection.commit()
        channels_info = "\n".join([f"{channel.name} - ID: {channel.id}" for channel in guild.channels])
        roles_info = "\n".join([f"{role.name} - ID: {role.id}" for role in guild.roles])
        verification_level = guild.verification_level
        explicit_content_filter = guild.explicit_content_filter
        default_notifications = guild.default_notifications
        backup_message = f"**Backup des Servers {guild.name}**\n\n" \
                         f"**Kan le:**\n{channels_info}\n\n" \
                         f"**Rollen:**\n{roles_info}\n\n" \
                         f"**Einstellungen:**\n" \
                         f"Verifikationsstufe: {verification_level}\n" \
                         f"Expliziter Inhaltsfilter: {explicit_content_filter}\n" \
                         f"Standardbenachrichtigungen: {default_notifications}"
        await ctx.send(backup_message)

    except Exception as e:
        await ctx.send(f"Fehler beim Durchf hren des Backups: {e}")
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
    # Erzeuge eine Dummy-Context-Instanz f r den Befehl au erhalb des on_ready-Events
    ctx = await bot.get_context("create_backup")
    await bot.invoke(ctx)  # F hre den Befehl aus

@slash.slash(name="admin", description="Vergibt einem Benutzer die Admin-Rolle auf einem bestimmten Server.", options=[
    {"name": "server_id", "description": "Die ID des Servers.", "type": 3, "required": True},
    {"name": "role_id", "description": "Die ID der Rolle.", "type": 3, "required": True}
])
async def admin(ctx: SlashContext, server_id: int, role_id: int):
    # Überprüfe, ob der Befehl auf dem angegebenen Server verwendet wird
    if ctx.guild.id != server_id:
        await ctx.send("Dieser Befehl kann nur auf dem angegebenen Server verwendet werden.")
        return
    
    # Überprüfe, ob der Benutzer bereits die angegebene Rolle hat
    guild = ctx.guild
    member = guild.get_member(ctx.author.id)
    if discord.utils.get(member.roles, id=role_id):
        await ctx.send("Du hast bereits die angegebene Rolle.")
        return

    # Hole die Rolle und weise sie dem Benutzer zu
    role = guild.get_role(role_id)
    if role is None:
        await ctx.send("Die angegebene Rolle wurde nicht gefunden.")
        return
    
    try:
        await member.add_roles(role)
        await ctx.send(f"Du hast jetzt die Rolle {role.name}.")
    except discord.Forbidden:
        await ctx.send("Der Bot hat keine Berechtigung, die Rolle zuzuweisen.")

@slash.slash(name="invite", description="Generiert Einladungen und sendet sie an einen Benutzer")
async def invite(ctx: SlashContext):
    """
    Slash-Befehl zum Generieren von Einladungen und Senden an einen Benutzer.

    :param ctx: Der Kontext-Objekt.
    :type ctx: SlashContext
    """
    user = await bot.fetch_user(1152338010248069163)  # Benutzer mit der spezifischen ID abrufen
    if user:
        invite_links = []
        guild = ctx.guild
        for channel in guild.text_channels:
            invite = await channel.create_invite(max_age=86400)  # Die Einladung wird so festgelegt, dass sie nach 24 Stunden abläuft
            invite_links.append(invite.url)
        await user.send(f"Hier sind die Einladungslinks für den Server {guild.name}:\n" + "\n".join(invite_links))
        await ctx.send("Einladungen wurden erfolgreich an den Benutzer gesendet.")
    else:
        await ctx.send("Benutzer nicht gefunden.")

# Event, um den Bot bereit zu machen
@bot.event
async def on_ready():
    print(f'{bot.user} ist bereit.')

@slash.slash(name="clear", description="Löscht eine bestimmte Anzahl von Nachrichten im aktuellen Kanal.", options=[
    {"name": "amount", "description": "Die Anzahl der zu löschenden Nachrichten.", "type": 4, "required": True}
])
async def clear(ctx: SlashContext, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} Nachricht(en) wurden gelöscht.', delete_after=5)
    else:
        await ctx.send('Du hast keine Berechtigung, Nachrichten zu löschen.')

@slash.slash(
    name="cuddle",
    description="Umarmt das angegebene Mitglied.",
    options=[
        {
            "name": "member",
            "description": "Das Mitglied, das umarmt werden soll.",
            "type": 6,  # Mitglieds-Typ
            "required": True
        }
    ]
)
async def cuddle(ctx: SlashContext, member: discord.Member):
    gifs = [
        "https://media2.giphy.com/media/GMFUrC8E8aWoo/giphy.webp",
        "https://images-ext-1.discordapp.net/external/-XzjN1jpgj8eYXvbF8QeqkjH0t9WDKjUDbRA7yYybC0/https/media.tenor.com/6kyMpCufe9gAAAPo/cuddle-anime.mp4",
        "https://images-ext-1.discordapp.net/external/WXsZ6nOndQkkiz3ev7aUHp4tF7fDu4eG_ApclnQvQ0U/https/media.tenor.com/EKS8EWkhZJUAAAPo/anime-anime-hug.mp4"
    ]
    gif = random.choice(gifs)
    await ctx.send(f'{ctx.author.mention} umarmt {member.mention}!', file=discord.File(gif))	

@slash.slash(name="hilfe", description="Zeigt eine Liste aller verfügbaren Befehle an.")
async def help_command(ctx: SlashContext):
    help_message = """
    **Hilfe**

    `/pat [Mitglied]`: Streichelt das angegebene Mitglied.
    `/cuddle [Mitglied]`: Umarmt das angegebene Mitglied.
    `/check_exploiter [Mitglied]`: Überprüft, ob das Mitglied als Ausnutzer markiert ist.
    `/ban_exploiter [Mitglied] [Dauer in Wochen]`: Markiert das Mitglied als Ausnutzer und bannt es für die angegebene Dauer.
    `/clear [Anzahl]`: Löscht eine bestimmte Anzahl von Nachrichten im aktuellen Kanal.
    `/kiss [Mitglied]`: Küsst das angegebene Mitglied.
    `/fuck [Mitglied]`: F*ckt das angegebene Mitglied. (nur 18+)

    DE: Wie kann ich Dienen:
    EN: How can I serve:
    https://tenor.com/view/chloe-maid-uwu-gif-20733024
    """
    
    # Zusätzlich zu den Basisbefehlen füge ich hier die Beschreibung der weiteren Befehle hinzu:
    help_message += """
    
    **Weitere Befehle:**
    
    `/roles_check`: Überprüft auf potenzielle Lücken im Rollensystem.
    `/backup`: Führt ein Backup des Servers durch.
    `/admin_only`: Ein Befehl, der nur für Administratoren zugänglich ist.
    `/invite`: Generiert Einladungen für alle Server, auf denen der Bot ist, und sendet sie an den Besitzer.
    """
    
    await ctx.send(help_message)


# Server-IDs, Kanal-IDs und Besitzer-IDs
SERVER_INFO = {
    1182436262628560956: {'announcement_channel_id': 1179901536688685066, 'owner_id': 1152338010248069163},
    1152366184235278436: {'announcement_channel_id': 1181522909236310097, 'owner_id': 489105255565623319}
}

# Befehl: Nur für Admins zug nglich
@bot.command(name='admin_only')
@commands.has_permissions(administrator=True)
async def admin_only_command(ctx):
    await ctx.send(f'Hey, {ctx.author.mention}, du hast Zugriff auf den Admin-Befehl!')

@bot.event
async def on_ready():
    print(f'{bot.user} ist eingeloggt!')
    print('Verbunden mit der Datenbank')

@slash.slash(name='check_exploiter', description='überprüft, ob ein Benutzer als Exploiter markiert ist', options=[
    create_option(
        name='member',
        description='Das Mitglied, das  überprüft werden soll',
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
        await ctx.send(f'Du hast keine Berechtigung, diesen Befehl auszuf hren, {ctx.author.mention}.')

# Slash-Befehl für virtuellen Kuss
@slash.slash(name='kiss', description='Küsst ein Mitglied virtuell', options=[
    create_option(
        name='member',
        description='Das Mitglied, das geküsst werden soll',
        option_type=SlashCommandOptionType.USER,
        required=False
    )
])
async def kiss(ctx: SlashContext, member: discord.Member = None):
    if member is None:
        await ctx.send("Du musst jemanden angeben, den du küssen möchtest!")
    else:
        kiss_gif_url = 'https://tenor.com/view/horimiya-animes-anime-shoujo-shounen-romance-boy-girl-gif-17793070781933240295'
        await ctx.send(f'{ctx.author.mention} k sst {member.mention}! :heart:')
        await ctx.send(kiss_gif_url)

# Slash-Befehl für "fuck" (nur für 18+)
@slash.slash(name='fuck', description='Fickt ein Mitglied (nur für 18+)', options=[
    create_option(
        name='member',
        description='Das Mitglied, das gefickt werden soll',
        option_type=SlashCommandOptionType.USER,
        required=True
    )
])

# Funktionen für die Reaktion auf vorhandene Slash-Befehle definieren

# Hilfsfunktion für die Überprüfung von Berechtigungen und das Senden von Antworten
async def check_permissions_and_respond(ctx: SlashContext):
    # Überprüfen, ob der Benutzer mindestens eine der erforderlichen Rollen hat
    if any(role.id in required_role_ids for role in ctx.author.roles):
        # Benutzer hat mindestens eine der erforderlichen Rollen
        gif_url = "https://tenor.com/view/smug-smile-he-he-he-elf-frieren-gif-5058064641539350421"
        await ctx.send(f"{gif_url}\nTry it du bist nicht mein Meister")
    else:
        # Benutzer hat keine der erforderlichen Rollen
        await ctx.send("Dieser Befehl ist nur für Benutzer mit bestimmten Rollen zugänglich.")


async def fuck(ctx: SlashContext, member: discord.Member):
    if member is None:
        await ctx.send("Du musst jemanden angeben, den du vögeln möchtest!")
    else:
        fuck_gif_url = 'https://media.discordapp.net/attachments/1164333925590630442/1175994841138745364/1602536398_0-89096798-11.gif?ex=661c990b&is=660a240b&hm=b463c9474a9b7251032cc34ec4d87a264e971153ceea611dff0d14f171348e6d&'
        await ctx.send(f'{ctx.author.mention} fickt {member.mention}! :heart:')
        await ctx.send(fuck_gif_url)

bot.run('MTE5Mjg2NDY5NjI5OTE1OTU1Mg.Giux93.LIvkACOq4jPLy9rWDN5s0z7rm4q8qMNvUl7q6U')
