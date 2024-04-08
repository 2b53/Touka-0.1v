# error_checker.py
import subprocess
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Error Checker Bot is ready. Logged in as {bot.user.name}')

@bot.command(name='check_errors')
async def check_errors_command(ctx):
    try:
        working_directory = '/path/to/project_folder/'
        check_main_script = subprocess.run(['python3', 'main.py'], capture_output=True, text=True, cwd=working_directory)
        check_keep_alive_script = subprocess.run(['python3', 'keep_alive.py'], capture_output=True, text=True, cwd=working_directory)
        check_bot_script = subprocess.run(['python3', 'bot.py'], capture_output=True, text=True, cwd=working_directory)

        error_messages = []
        if check_main_script.returncode != 0:
            error_messages.append(f'Error in main.py:\n{check_main_script.stderr}')
        if check_keep_alive_script.returncode != 0:
            error_messages.append(f'Error in keep_alive.py:\n{check_keep_alive_script.stderr}')
        if check_bot_script.returncode != 0:
            error_messages.append(f'Error in bot.py:\n{check_bot_script.stderr}')

        if error_messages:
            error_report = '\n\n'.join(error_messages)
            await ctx.send(f'Error report:\n```\n{error_report}\n```')
        else:
            await ctx.send('No errors found in the scripts.')

    except Exception as e:
        await ctx.send(f'An error occurred while checking for errors: {e}')

keep_alive()
bot.run('MTE5Mjg2NDY5NjI5OTE1OTU1Mg.Gw2r2x.NCw8D4dv5ZRztqElN1zVlfdBDgZhDeCiez8-8Q')
