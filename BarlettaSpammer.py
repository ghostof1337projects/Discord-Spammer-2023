import ctypes
import os
import platform
import socket
import sys
import time
import discord
import requests
import json
import re
import random

from discord.ext import commands
from tqdm import tqdm

# version variable

__VERSION__ = '5.0'

# disable buttons on console, activate only X and minimise button
GWL_STYLE = -16
WS_MAXIMIZEBOX = 0x00010000
WS_SIZEBOX = 0x00040000

hwnd = ctypes.windll.kernel32.GetConsoleWindow()

style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
style &= ~WS_MAXIMIZEBOX
style &= ~WS_SIZEBOX

ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
ctypes.windll.user32.DeleteMenu(hwnd, 0xF000, 0x0001)
ctypes.windll.user32.RedrawWindow(hwnd, None, None, 0x0400 | 0x0001)

# logs all the activities

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    
    with open("log.txt", "a") as log_file:
        log_file.write(log_message + "\n")

log("INFO: Script started - The script has started executing.")
log("INFO: Setting up console - Configuring the console display for a welcoming interface.")

def get_username():
    if platform.system() == 'Windows':
        return os.getlogin()
    return os.environ.get('USER')

# check is discord token if valid or not

def validate_discord_token(token):
    try:
        headers = {
            'authorization': token
        }
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        return False
# check for channel id if valid or not

def validate_channel_id(token, channel_id):
    try:
        headers = {
            'authorization': token
        }
        response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

log("INFO: Validating channel ID - Validating the provided Discord channel ID.")
log("INFO: Channel ID validation successful - Provided channel ID is valid.")

username = get_username()
discord_token = input('\x1b[34m\n                                TOKEN:')

if not validate_discord_token(discord_token):
    print('\x1b[31m\n                                INVALID TOKEN.')
    time.sleep(2)
    sys.exit(1)

# feedback system

show_feedback_message = random.randint(0, 1)

if show_feedback_message:
    user_response = ctypes.windll.user32.MessageBoxW(
        0,
        "Would you like to rate Barletta Spammer v5?",
        "Rate Barletta Spammer v5",
        0x4 | 0x20,
    )

    if user_response == 6:
        while True:
            user_input = input("\x1b[34m\n                           Please enter your rating and comments: ")
            if not user_input.strip():
                print("\x1b[31m\n                           You must enter a message")
                continue

            # Comprehensive pattern to block SQL injection attempts
            sql_injection_pattern = r'((?i)(alter|create|delete|drop|exec(ute)?|insert( +into)?|'
            sql_injection_pattern += r'select( +\*| +from)?|truncate|update)( +\w+)*)( *\;|\)|--|\/\*)*'

            # Check for mathematical expressions within SQL functions
            if re.search(r'(?i)(\w+)\s*\(\s*(.*?)\s*\)', user_input):
                print("\x1b[31m\n      Your input contains potentially dangerous SQL keywords. Please provide a different message.")
                continue

            if re.search(sql_injection_pattern, user_input):
                print("\x1b[31m\n      Your input contains potentially dangerous SQL keywords. Please provide a different message.")
                continue

            # Check for links with specific TLDs and domains
            # This pattern will block .com, .net, .org, and custom domain links
            if re.search(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|discord\.gg/[a-zA-Z0-9]+|\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org)\b', user_input):
                print("\x1b[31m\n      You cannot put links with common TLDs or custom domains.")
                continue

            break  # Exit the loop if the input is valid

        # Get the Discord username
        def get_discord_username(token):
            try:
                headers = {
                    'authorization': token
                }
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
                response.raise_for_status()
                user_data = response.json()
                return user_data['username']
            except requests.exceptions.RequestException as e:
                print(f'\x1b[30m\n                                FAILED TO FETCH DISCORD USERNAME: {e}')
                return None

        discord_username = get_discord_username(discord_token)

        if not discord_username:
            print('\x1b[30m\n                                INTERNAL ERROR LINE [if not discord_username:]')
            sys.exit(1)

        webhook_url = 'INPUT YOUR WEBHOOK HERE'
        data = {
            "content": f"# NEW FEEDBACK! \nDiscord Username: **{discord_username}** \n\nMessage: ```{user_input}```"
        }
        response = requests.post(webhook_url, json=data)



log("INFO: Validating Discord token - Validating the Discord token provided by the user.")
log("INFO: Token validation successful - Discord token is valid.")

log("INFO: Setting up notifications - Configuring notifications for displaying messages.")

log("INFO: Writing token to file - Storing the Discord token in a file named 'token.txt'.")

with open("token.txt", "w") as token_file:
    token_file.write(discord_token)

def get_discord_username(token):
    try:
        headers = {
            'authorization': token
        }
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        return user_data['username']
    except requests.exceptions.RequestException as e:
        print(f'\x1b[30m\n                                FAILED TO FETCH DISCORD USERNAME: {e}')
        return None

discord_username = get_discord_username(discord_token)

if not discord_username:
    print('\x1b[30m\n                                INTERNAL ERROR LINE [if not discord_username:]')
    sys.exit(1)

log("INFO: Fetching Discord username - Fetching the username associated with the provided token.")
log("INFO: Discord username retrieved - Discord username successfully retrieved.")

hostname = socket.gethostname()
os_name = platform.system()
architecture = platform.architecture()[0]
tick = "128"

log("INFO: Retrieving system information - Gathering information about the system platform and setup.")
log("INFO: System information retrieved - Successfully retrieved system information.")

def main():
    bot = commands.Bot('.', discord.Intents.all(), **{'command_prefix': 'intents'})

def Spinner():
    l = ['|', '/', '-', '\\']
    for i in l + l + l:
        sys.stdout.write(f'\r[\x1b[95m+\x1b[95m\x1b[37m] MafiaBarletta Loading... [{i}]')
        sys.stdout.flush()
        time.sleep(0.1)

print(f'\x1b[95m')

log("INFO: Initializing progress bar - Setting up the progress bar for visual indication of loading.")
# progress bar
progressbar = tqdm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 60, 100])

for item in progressbar:
    time.sleep(0.1)
    progressbar.set_description(' Loading Barletta Spammer ')

time.sleep(1)
ctypes.windll.kernel32.SetConsoleTitleW('[Barletta Spammer] - Welcome')

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

Mbox('BarlettaSpammer', 'Welcome to Barletta Spammer', 64)

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

Mbox('BarlettaSpammer', 'NOTE! YOU NEED A FILE NAMED text.txt IN THE SAME FOLDER AS YOUR SCRIPT TO WORK!', 48)

# if a error is happening, it skips (error suppressor)
class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()
os.system('cls & mode 85,20 & title [Barletta Spammer] - LOGIN - Made by Ghost of 1337')

channelID = input('\x1b[34m\n                                Enter the channel ID: ')

if not validate_channel_id(discord_token, channelID):
    print('\x1b[31m\n                                INVALID CHANNEL ID.')
    time.sleep(2)
    sys.exit(1)

#User input
log("INFO: Requesting channel ID - Prompting the user to input the Discord channel ID.")

# Message sending
log("INFO: Sending messages - Initiating the process to send messages to the specified channel.")

print('\x1b[34m\n                                Connecting...                                \n')
time.sleep(1)
os.system(f'''cls & mode 85,20 & title [Barletta Spammer] - v{__VERSION__} - Made by Ghost of 1337''')
print('\x1b[1;37m       USERNAME :\x1b[1;32m ' + discord_username)
print('\x1b[1;37m       HOSTNAME :\x1b[1;32m ' + hostname)
print('\x1b[1;37m       OS       :\x1b[1;32m ' + os_name)
print('\x1b[1;37m       ARCHITECTURE :\x1b[1;32m ' + architecture)
print('\x1b[1;37m       TICK :\x1b[1;32m ' + tick)
print('\x1b[31m\n\n               \n               ╔╗ ┌─┐┬─┐┬  ┌─┐┌┬┐┌┬┐┌─┐  ╔═╗┌─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐\n               ╠╩╗├─┤├┬┘│  ├┤  │  │ ├─┤  ╚═╗├─┘├─┤││││││├┤ ├┬┘\n               ╚═╝┴ ┴┴└─┴─┘└─┘ ┴  ┴ ┴ ┴  ╚═╝┴  ┴ ┴┴ ┴┴ ┴└─┘┴└─\n               \n               ')
print(f'''\n                              \x1b[1;37m{username}\x1b[31m@\x1b[1;34m{hostname}\n\n               \n''')
time.sleep(1)
headers = {
    'authorization': discord_token
}
file = open("text.txt", "r")
lines = file.readlines()

while True:
    for line in lines:
        try:
            requests.post(
                f"https://discord.com/api/v9/channels/{channelID}/messages",
                headers=headers,
                json={"content": line})
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(5)
            continue
