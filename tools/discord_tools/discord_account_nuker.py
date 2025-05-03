import requests
import json
import time
import sys
import os
import threading
import random
from colorama import init, Fore, Style

init(autoreset=True)

DISCORD_API = "https://discord.com/api/v9"

def get_user_guilds(token):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{DISCORD_API}/users/@me/guilds", headers=headers)

        if response.status_code == 200:
            guilds = response.json()
            return True, guilds
        else:
            print(f"{Fore.RED}[-] Failed to get user guilds. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting user guilds: {str(e)}{Style.RESET_ALL}")
        return False, None

def leave_guild(token, guild_id):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(f"{DISCORD_API}/users/@me/guilds/{guild_id}", headers=headers)

        if response.status_code == 204:
            return True
        else:
            return False

    except:
        return False

def leave_all_guilds(token):
    success, guilds = get_user_guilds(token)

    if not success or not guilds:
        print(f"{Fore.RED}[-] Failed to get guilds to leave.{Style.RESET_ALL}")
        return False

    # Filter out guilds where the user is the owner (can't leave those)
    guilds_to_leave = [guild for guild in guilds if not guild.get('owner', False)]

    total_guilds = len(guilds_to_leave)
    left_count = 0

    print(f"\n{Fore.YELLOW}[*] Leaving {total_guilds} guilds...{Style.RESET_ALL}")

    for guild in guilds_to_leave:
        guild_id = guild.get('id')
        guild_name = guild.get('name')

        if leave_guild(token, guild_id):
            left_count += 1
            print(f"{Fore.GREEN}[+] Left guild: {guild_name} ({guild_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to leave guild: {guild_name} ({guild_id}){Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {left_count}/{total_guilds} guilds left ({int(left_count/total_guilds*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Left {left_count}/{total_guilds} guilds.{Style.RESET_ALL}")
    return left_count > 0

def get_user_relationships(token):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{DISCORD_API}/users/@me/relationships", headers=headers)

        if response.status_code == 200:
            relationships = response.json()
            return True, relationships
        else:
            print(f"{Fore.RED}[-] Failed to get user relationships. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting user relationships: {str(e)}{Style.RESET_ALL}")
        return False, None

def remove_relationship(token, user_id):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(f"{DISCORD_API}/users/@me/relationships/{user_id}", headers=headers)

        if response.status_code == 204:
            return True
        else:
            return False

    except:
        return False

def remove_all_friends(token):
    success, relationships = get_user_relationships(token)

    if not success or not relationships:
        print(f"{Fore.RED}[-] Failed to get relationships to remove.{Style.RESET_ALL}")
        return False

    # Filter only friends (type 1)
    friends = [rel for rel in relationships if rel.get('type') == 1]

    total_friends = len(friends)
    removed_count = 0

    print(f"\n{Fore.YELLOW}[*] Removing {total_friends} friends...{Style.RESET_ALL}")

    for friend in friends:
        user_id = friend.get('id')
        username = friend.get('user', {}).get('username')

        if remove_relationship(token, user_id):
            removed_count += 1
            print(f"{Fore.GREEN}[+] Removed friend: {username} ({user_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to remove friend: {username} ({user_id}){Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {removed_count}/{total_friends} friends removed ({int(removed_count/total_friends*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Removed {removed_count}/{total_friends} friends.{Style.RESET_ALL}")
    return removed_count > 0

def get_user_channels(token):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{DISCORD_API}/users/@me/channels", headers=headers)

        if response.status_code == 200:
            channels = response.json()
            return True, channels
        else:
            print(f"{Fore.RED}[-] Failed to get user channels. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting user channels: {str(e)}{Style.RESET_ALL}")
        return False, None

def delete_channel(token, channel_id):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(f"{DISCORD_API}/channels/{channel_id}", headers=headers)

        if response.status_code == 200:
            return True
        else:
            return False

    except:
        return False

def delete_all_dm_channels(token):
    success, channels = get_user_channels(token)

    if not success or not channels:
        print(f"{Fore.RED}[-] Failed to get DM channels to delete.{Style.RESET_ALL}")
        return False

    # Filter only DM channels (type 1)
    dm_channels = [channel for channel in channels if channel.get('type') == 1]

    total_channels = len(dm_channels)
    deleted_count = 0

    print(f"\n{Fore.YELLOW}[*] Deleting {total_channels} DM channels...{Style.RESET_ALL}")

    for channel in dm_channels:
        channel_id = channel.get('id')
        recipients = channel.get('recipients', [])
        recipient_name = recipients[0].get('username') if recipients else "Unknown"

        if delete_channel(token, channel_id):
            deleted_count += 1
            print(f"{Fore.GREEN}[+] Deleted DM channel with: {recipient_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to delete DM channel with: {recipient_name}{Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {deleted_count}/{total_channels} DM channels deleted ({int(deleted_count/total_channels*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Deleted {deleted_count}/{total_channels} DM channels.{Style.RESET_ALL}")
    return deleted_count > 0

def change_account_settings(token, username=None, email=None, password=None, new_password=None, avatar=None):
    # Format token properly if it's not already formatted
    if not token.startswith(('Bot ', 'Bearer ')):
        # For user tokens
        formatted_token = token
    else:
        formatted_token = token

    headers = {
        "Authorization": formatted_token,
        "Content-Type": "application/json"
    }

    data = {}

    if username:
        data["username"] = username

    if email:
        data["email"] = email

    if password and new_password:
        data["password"] = password
        data["new_password"] = new_password

    if avatar:
        data["avatar"] = avatar

    if not data:
        print(f"{Fore.YELLOW}[!] No settings to change.{Style.RESET_ALL}")
        return False

    try:
        response = requests.patch(f"{DISCORD_API}/users/@me", headers=headers, json=data)

        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Account settings changed successfully!{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Failed to change account settings. Status code: {response.status_code}{Style.RESET_ALL}")
            if response.text:
                print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}[-] Error changing account settings: {str(e)}{Style.RESET_ALL}")
        return False

def full_account_nuke(token):
    print(f"\n{Fore.RED}[!] Starting full account nuke...{Style.RESET_ALL}")

    # Leave all guilds
    leave_all_guilds(token)

    # Remove all friends
    remove_all_friends(token)

    # Delete all DM channels
    delete_all_dm_channels(token)

    print(f"\n{Fore.GREEN}[+] Full account nuke completed!{Style.RESET_ALL}")
