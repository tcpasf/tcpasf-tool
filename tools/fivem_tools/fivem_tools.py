import requests
import json
import re
import time
import sys
import os
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info

init(autoreset=True)

def cfx_to_ip(cfx_code):
    print(f"\n{Fore.YELLOW}[*] Converting CFX code to IP address...{Style.RESET_ALL}")

    try:
        cfx_code = cfx_code.strip()
        if cfx_code.startswith("cfx.re/join/"):
            cfx_code = cfx_code.replace("cfx.re/join/", "")

        url = f"https://servers-frontend.fivem.net/api/servers/single/{cfx_code}"

        spinner = ['|', '/', '-', '\\']
        i = 0
        response = None

        print(f"{Fore.CYAN}[*] Fetching server information...{Style.RESET_ALL}")

        session = requests.Session()
        request = requests.Request("GET", url)
        prepared_request = session.prepare_request(request)

        response = session.send(prepared_request)

        if response.status_code == 200:
            data = response.json()

            if "Data" in data:
                server_data = data["Data"]

                endpoints = server_data.get("connectEndPoints", [])
                if endpoints:
                    ip_port = endpoints[0]
                    ip, port = ip_port.split(":")

                    print(f"\n{Fore.GREEN}[+] Server Information:{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}IP:Port: {Style.RESET_ALL}{ip}:{port}")
                    print(f"{Fore.CYAN}Server Name: {Style.RESET_ALL}{server_data.get('hostname', 'N/A')}")
                    print(f"{Fore.CYAN}Players: {Style.RESET_ALL}{server_data.get('clients', 0)}/{server_data.get('svMaxclients', 0)}")
                    print(f"{Fore.CYAN}Game Type: {Style.RESET_ALL}{server_data.get('gametype', 'N/A')}")
                    print(f"{Fore.CYAN}Map Name: {Style.RESET_ALL}{server_data.get('mapname', 'N/A')}")

                    if "resources" in server_data:
                        print(f"\n{Fore.CYAN}Resources: {Style.RESET_ALL}")
                        for resource in sorted(server_data["resources"]):
                            print(f"  - {resource}")

                    if "vars" in server_data:
                        print(f"\n{Fore.CYAN}Server Variables: {Style.RESET_ALL}")
                        for key, value in server_data["vars"].items():
                            print(f"  {key}: {value}")

                    return ip, port
                else:
                    print(f"{Fore.RED}[-] No connection endpoints found in server data.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Invalid server data format.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to retrieve server information. Status code: {response.status_code}{Style.RESET_ALL}")
            if response.status_code == 404:
                print(f"{Fore.RED}[-] Server not found. Check your CFX code.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return None, None

def get_players_json(ip, port):
    print(f"\n{Fore.YELLOW}[*] Fetching players.json from {ip}:{port}...{Style.RESET_ALL}")

    try:
        url = f"http://{ip}:{port}/players.json"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            players = response.json()

            print(f"\n{Fore.GREEN}[+] Found {len(players)} players:{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'ID':<5} {'Name':<30} {'Ping':<10} {'Identifiers'}{Style.RESET_ALL}")
            print("-" * 80)

            for player in players:
                player_id = player.get("id", "N/A")
                name = player.get("name", "Unknown")
                ping = player.get("ping", "N/A")

                identifiers = player.get("identifiers", [])
                steam_id = discord_id = license_id = "N/A"

                for identifier in identifiers:
                    if identifier.startswith("steam:"):
                        steam_id = identifier
                    elif identifier.startswith("discord:"):
                        discord_id = identifier
                    elif identifier.startswith("license:"):
                        license_id = identifier

                print(f"{player_id:<5} {name[:30]:<30} {ping:<10} {steam_id}")
                if discord_id != "N/A":
                    print(f"{'':<5} {'':<30} {'':<10} {discord_id}")
                if license_id != "N/A":
                    print(f"{'':<5} {'':<30} {'':<10} {license_id}")

            save = input(f"\n{Fore.CYAN}Save players.json to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"players_{ip}_{port}.json"
                with open(filename, 'w') as f:
                    json.dump(players, f, indent=4)
                print(f"{Fore.GREEN}[+] Saved to {filename}{Style.RESET_ALL}")

            return players
        else:
            print(f"{Fore.RED}[-] Failed to retrieve players.json. Status code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] The server might have disabled players.json access.{Style.RESET_ALL}")

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-] Request timed out. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] Connection error. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[-] Invalid JSON response. The server might be returning non-JSON data.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return None

def get_info_json(ip, port):
    print(f"\n{Fore.YELLOW}[*] Fetching info.json from {ip}:{port}...{Style.RESET_ALL}")

    try:
        url = f"http://{ip}:{port}/info.json"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            info = response.json()

            print(f"\n{Fore.GREEN}[+] Server Information:{Style.RESET_ALL}")

            if isinstance(info, dict):
                for key, value in info.items():
                    if isinstance(value, (dict, list)):
                        print(f"{Fore.CYAN}{key}:{Style.RESET_ALL}")
                        if isinstance(value, dict):
                            for k, v in value.items():
                                print(f"  {k}: {v}")
                        else:
                            for item in value:
                                print(f"  - {item}")
                    else:
                        print(f"{Fore.CYAN}{key}: {Style.RESET_ALL}{value}")
            else:
                print(json.dumps(info, indent=4))

            save = input(f"\n{Fore.CYAN}Save info.json to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"info_{ip}_{port}.json"
                with open(filename, 'w') as f:
                    json.dump(info, f, indent=4)
                print(f"{Fore.GREEN}[+] Saved to {filename}{Style.RESET_ALL}")

            return info
        else:
            print(f"{Fore.RED}[-] Failed to retrieve info.json. Status code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] The server might have disabled info.json access.{Style.RESET_ALL}")

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-] Request timed out. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] Connection error. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[-] Invalid JSON response. The server might be returning non-JSON data.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return None

def get_dynamic_json(ip, port):
    print(f"\n{Fore.YELLOW}[*] Fetching dynamic.json from {ip}:{port}...{Style.RESET_ALL}")

    try:
        url = f"http://{ip}:{port}/dynamic.json"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            dynamic = response.json()

            print(f"\n{Fore.GREEN}[+] Dynamic Server Information:{Style.RESET_ALL}")

            if "hostname" in dynamic:
                print(f"{Fore.CYAN}Hostname: {Style.RESET_ALL}{dynamic['hostname']}")

            if "clients" in dynamic and "svMaxclients" in dynamic:
                print(f"{Fore.CYAN}Players: {Style.RESET_ALL}{dynamic['clients']}/{dynamic['svMaxclients']}")

            if "resources" in dynamic:
                print(f"\n{Fore.CYAN}Resources ({len(dynamic['resources'])}):{Style.RESET_ALL}")
                for resource in sorted(dynamic['resources']):
                    print(f"  - {resource}")

            save = input(f"\n{Fore.CYAN}Save dynamic.json to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"dynamic_{ip}_{port}.json"
                with open(filename, 'w') as f:
                    json.dump(dynamic, f, indent=4)
                print(f"{Fore.GREEN}[+] Saved to {filename}{Style.RESET_ALL}")

            return dynamic
        else:
            print(f"{Fore.RED}[-] Failed to retrieve dynamic.json. Status code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] The server might have disabled dynamic.json access.{Style.RESET_ALL}")

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-] Request timed out. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] Connection error. The server might be offline or blocking requests.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[-] Invalid JSON response. The server might be returning non-JSON data.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return None

def server_status_checker(ip, port):
    print(f"\n{Fore.YELLOW}[*] Checking server status for {ip}:{port}...{Style.RESET_ALL}")

    try:
        url = f"http://{ip}:{port}/info.json"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Server is ONLINE{Style.RESET_ALL}")

            try:
                players_url = f"http://{ip}:{port}/players.json"
                players_response = requests.get(players_url, timeout=5)

                if players_response.status_code == 200:
                    players = players_response.json()
                    print(f"{Fore.GREEN}[+] Players online: {len(players)}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] Could not retrieve player count.{Style.RESET_ALL}")
            except:
                print(f"{Fore.YELLOW}[!] Could not retrieve player count.{Style.RESET_ALL}")

            return True
        else:
            print(f"{Fore.RED}[-] Server might be offline or blocking requests. Status code: {response.status_code}{Style.RESET_ALL}")
            return False

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-] Request timed out. The server might be offline.{Style.RESET_ALL}")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] Connection error. The server is likely offline.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return False

def search_fivem_servers(query):
    print(f"\n{Fore.YELLOW}[*] Searching FiveM servers for: {query}{Style.RESET_ALL}")

    try:
        url = "https://servers-frontend.fivem.net/api/servers/search"
        params = {
            "q": query,
            "limit": 15
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "data" in data:
                servers = data["data"]

                if not servers:
                    print(f"{Fore.YELLOW}[!] No servers found matching the query.{Style.RESET_ALL}")
                    return []

                print(f"\n{Fore.GREEN}[+] Found {len(servers)} servers:{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}{'#':<3} {'Name':<50} {'Players':<15} {'IP:Port'}{Style.RESET_ALL}")
                print("-" * 90)

                for i, server in enumerate(servers, 1):
                    name = server.get("hostname", "Unknown")
                    name = re.sub(r'\^[0-9]', '', name)

                    clients = server.get("clients", 0)
                    max_clients = server.get("svMaxclients", 0)
                    players = f"{clients}/{max_clients}"

                    endpoints = server.get("connectEndPoints", [])
                    ip_port = endpoints[0] if endpoints else "N/A"

                    print(f"{i:<3} {name[:50]:<50} {players:<15} {ip_port}")

                selection = input(f"\n{Fore.CYAN}Select a server number (or 0 to cancel): {Style.RESET_ALL}")

                if selection.isdigit() and 1 <= int(selection) <= len(servers):
                    selected = servers[int(selection) - 1]
                    endpoints = selected.get("connectEndPoints", [])

                    if endpoints:
                        ip_port = endpoints[0]
                        ip, port = ip_port.split(":")

                        print(f"\n{Fore.GREEN}[+] Selected server: {selected.get('hostname', 'Unknown')}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}IP:Port: {Style.RESET_ALL}{ip}:{port}")

                        return ip, port
                    else:
                        print(f"{Fore.RED}[-] No connection endpoints found for the selected server.{Style.RESET_ALL}")
                elif selection != "0":
                    print(f"{Fore.RED}[-] Invalid selection.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Invalid response format from FiveM API.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to search servers. Status code: {response.status_code}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

    return None, None

def fivem_tools_menu():
    ip = None
    port = None

    while True:
        clear_screen()
        print(generate_category_ascii("FIVEM TOOLS"))
        display_system_info()

        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║             FIVEM TOOLS MENU             ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

        if ip and port:
            print(f"{Fore.GREEN}Current server: {ip}:{port}{Style.RESET_ALL}")

        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} CFX Code to IP")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Search FiveM Servers")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Get players.json")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Get info.json")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Get dynamic.json")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Check Server Status")
        print(f"{Fore.CYAN}[7]{Style.RESET_ALL} Set Server IP:Port Manually")
        print(f"{Fore.CYAN}[8]{Style.RESET_ALL} Back to Main Menu")

        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

        if choice == "1":
            cfx_code = input(f"\n{Fore.CYAN}Enter CFX code (e.g., cfx.re/join/abcdef): {Style.RESET_ALL}")
            ip, port = cfx_to_ip(cfx_code)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "2":
            query = input(f"\n{Fore.CYAN}Enter search query: {Style.RESET_ALL}")
            ip, port = search_fivem_servers(query)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "3":
            if not ip or not port:
                print(f"{Fore.RED}[-] No server selected. Please use options 1, 2, or 7 first.{Style.RESET_ALL}")
            else:
                get_players_json(ip, port)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "4":
            if not ip or not port:
                print(f"{Fore.RED}[-] No server selected. Please use options 1, 2, or 7 first.{Style.RESET_ALL}")
            else:
                get_info_json(ip, port)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "5":
            if not ip or not port:
                print(f"{Fore.RED}[-] No server selected. Please use options 1, 2, or 7 first.{Style.RESET_ALL}")
            else:
                get_dynamic_json(ip, port)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "6":
            if not ip or not port:
                print(f"{Fore.RED}[-] No server selected. Please use options 1, 2, or 7 first.{Style.RESET_ALL}")
            else:
                server_status_checker(ip, port)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "7":
            ip_port = input(f"\n{Fore.CYAN}Enter server IP:Port (e.g., 123.456.789.012:30120): {Style.RESET_ALL}")
            try:
                ip, port = ip_port.split(":")
                print(f"{Fore.GREEN}[+] Server set to {ip}:{port}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}[-] Invalid format. Please use IP:Port format.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "8":
            break

        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
