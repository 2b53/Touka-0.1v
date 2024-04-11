# log_script.py
import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.invites = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logging Bot is ready. Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    invites_before = await get_invites()
    # Hier kannst du benutzerdefinierte Aktionen f�r das Join-Event implementieren
    # ...

    invites_after = await get_invites()
    new_invite = find_new_invite(invites_before, invites_after)

    if new_invite:
        await log_invite(member, new_invite)

async def get_invites():
    guild = bot.guilds[0]  # Du musst dies entsprechend deiner Anforderungen anpassen
    invites = await guild.invites()
    return {invite.inviter.id: invite for invite in invites}

def find_new_invite(old_invites, new_invites):
    for inviter_id, new_invite in new_invites.items():
        if inviter_id not in old_invites or old_invites[inviter_id].uses < new_invite.uses:
            return new_invite
    return None

async def log_invite(member, invite):
    log_channel_id = 123456789012345678  # ID des Textkanals, in dem das Log geschrieben werden soll
    log_channel = member.guild.get_channel(log_channel_id)

    if log_channel:
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        log_message = f'{timestamp} - {member.name}#{member.discriminator} wurde von {invite.inviter.name}#{invite.inviter.discriminator} ({invite.inviter.id}) eingeladen.\n'
        await log_channel.send(log_message)

# Dein Bot-Token hier einf�gen
bot.run('MTE5Mjg2NDY5NjI5OTE1OTU1Mg.Gw2r2x.NCw8D4dv5ZRztqElN1zVlfdBDgZhDeCiez8-8Q')
