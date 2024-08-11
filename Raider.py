import requests
import time
import random
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Load tokens from tokens.txt
def load_tokens(filename='tokens.txt'):
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# Send message function
def send_message(token, channel_id, message):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        'content': f"```{message}```"
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(Fore.RED + f"Message successfully sent with token {token[:10]}...!")
    else:
        print(Fore.RED + f"Failed to send message: {response.status_code} - {response.text}")

# Join server function
def join_server(token, invite_code):
    url = f'https://discord.com/api/v9/invites/{invite_code}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        print(Fore.RED + f"Token {token[:10]}... successfully joined the server!")
    else:
        print(Fore.RED + f"Failed to join server: {response.status_code} - {response.text}")

# Get random users function
def get_random_users(token, guild_id, num_users):
    url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit={num_users}'
    headers = {
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        members = response.json()
        return [f"<@{member['user']['id']}>" for member in members]
    else:
        print(Fore.RED + f"Failed to retrieve member info: {response.status_code} - {response.text}")
        return []

# Set online status and custom status function
def set_online_status(token, status_message="Raider Playing"):
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        "status": "online",
        "custom_status": {
            "text": status_message
        }
    }
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(Fore.RED + f"Token {token[:10]}... successfully set to online with custom status!")
    else:
        print(Fore.RED + f"Failed to set status: {response.status_code} - {response.text}")

# Raid function
def raid(tokens):
    if not tokens:
        print(Fore.RED + "Failed to load tokens from tokens.txt.")
        return

    channel_id = input(Fore.RED + "Enter the channel ID to send messages to: ")
    message = input(Fore.RED + "Enter the message to send: ")
    num_messages = int(input(Fore.RED + "How many messages to send? "))
    ping_everyone = input(Fore.RED + "Ping everyone? (y/n): ").strip().lower()
    delay_between_messages = float(input(Fore.RED + "Delay between messages (seconds): "))
    random_tag = input(Fore.RED + "Tag random users from the server? (y/n): ").strip().lower()
    if random_tag == 'y':
        guild_id = input(Fore.RED + "Enter the server ID: ")
        num_tags = int(input(Fore.RED + "How many users to tag: "))

    ping_everyone = '@everyone ' if ping_everyone == 'y' else ''
    
    for i in range(num_messages):
        for token in tokens:
            full_message = ping_everyone + message
            if random_tag == 'y':
                random_users = get_random_users(token, guild_id, num_tags)
                if random_users:
                    full_message += " " + " ".join(random_users)
            send_message(token, channel_id, full_message)
            time.sleep(delay_between_messages)  # Wait for the specified delay between messages

# Mass Join function
def mass_join(tokens):
    if not tokens:
        print(Fore.RED + "Failed to load tokens from tokens.txt.")
        return

    invite_link = input(Fore.RED + "Enter the Discord invite link or code: ")
    invite_code = invite_link.split('/')[-1]  # Extract invite code only

    for token in tokens:
        join_server(token, invite_code)
        time.sleep(0.1)  # Wait for 0.1 seconds between joins

# Onliner function
def onliner(tokens):
    if not tokens:
        print(Fore.RED + "Failed to load tokens from tokens.txt.")
        return

    for token in tokens:
        set_online_status(token)
        time.sleep(0.1)  # Wait for 0.1 seconds between actions

    print(Fore.RED + "All tokens set to online and custom status applied.")

# Main menu
def main():
    while True:
        # New Menu
        print(Fore.RED + """
██████╗░░█████╗░██╗██████╗░███████╗██████╗░
██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██████╔╝███████║██║██║░░██║█████╗░░██████╔╝
██╔══██╗██╔══██║██║██║░░██║██╔══╝░░██╔══██╗
██║░░██║██║░░██║██║██████╔╝███████╗██║░░██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝

         1-) Raid             2-) Mass Join            3-)  Onliner       Made By D0ruk
        """)
        choice = input(Fore.RED + "Enter your choice: ")

        tokens = load_tokens()
        if choice == '1':
            raid(tokens)
        elif choice == '2':
            mass_join(tokens)
        elif choice == '3':
            onliner(tokens)
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
