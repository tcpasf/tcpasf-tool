
import sys
import os
import time
import datetime
import platform
import threading
from colorama import init, Fore, Style, Back
import requests

init(autoreset=True)

def generate_gradient_colors(num_colors, start_color=(0, 0, 255), end_color=(255, 255, 255)):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color

    colors = []
    for i in range(num_colors):
        t = i / (num_colors - 1)
        r = int(r1 * (1 - t) + r2 * t)
        g = int(g1 * (1 - t) + g2 * t)
        b = int(b1 * (1 - t) + b2 * t)
        colors.append((r, g, b))

    return colors

def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def print_gradient_text(text, start_color=(0, 0, 255), end_color=(255, 255, 255)):
    colors = generate_gradient_colors(len(text), start_color, end_color)

    colored_text = ""
    for char, color in zip(text, colors):
        r, g, b = color
        colored_text += f"{rgb_to_ansi(r, g, b)}{char}"

    return colored_text + Style.RESET_ALL

def generate_category_ascii(category_name):
    ascii_art = ""

    if category_name.upper() == "IP TOOLS":
        ascii_art = r"""
 ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
 ██║██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
 ██║██╔═══╝        ██║   ██║   ██║██║   ██║██║     ╚════██║
 ██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """
    elif category_name.upper() == "FIVEM TOOLS":
        ascii_art = r"""
 ███████╗██╗██╗   ██╗███████╗███╗   ███╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ██╔════╝██║██║   ██║██╔════╝████╗ ████║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
 █████╗  ██║██║   ██║█████╗  ██╔████╔██║       ██║   ██║   ██║██║   ██║██║     ███████╗
 ██╔══╝  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
 ██║     ██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """
    elif category_name.upper() == "DISCORD TOOLS":
        ascii_art = r"""
 ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
 ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
 ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
 ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """
    elif category_name.upper() == "USER MANAGEMENT":
        ascii_art = r"""
 ██╗   ██╗███████╗███████╗██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗███╗   ███╗███████╗███╗   ██╗████████╗
 ██║   ██║██╔════╝██╔════╝██╔══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
 ██║   ██║███████╗█████╗  ██████╔╝    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║
 ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║
 ╚██████╔╝███████║███████╗██║  ██║    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║
  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝
        """
    elif category_name.upper() == "NETWORK SECURITY":
        ascii_art = r"""
 ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
 ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
 ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝     ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝
 ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗     ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝
 ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝
        """
    elif category_name.upper() == "SYSTEM TOOLS":
        ascii_art = r"""
 ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
 ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║       ██║   ██║   ██║██║   ██║██║     ███████╗
 ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
 ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """
    elif category_name.upper() == "CRYPTO TOOLS":
        ascii_art = r"""
  ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
 ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
 ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
 ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """
    else:
        ascii_art = r"""
 ████████╗ ██████╗██████╗  █████╗ ███████╗███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
 ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██║   ██║     ██████╔╝███████║███████╗█████╗         ██║   ██║   ██║██║   ██║██║     ███████╗
    ██║   ██║     ██╔═══╝ ██╔══██║╚════██║██╔══╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║   ╚██████╗██║     ██║  ██║███████║██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝    ╚═════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
        """

    colored_lines = []
    lines = ascii_art.split('\n')

    for line in lines:
        if line.strip():
            colored_line = ""
            colors = generate_gradient_colors(len(line), (0, 0, 255), (255, 255, 255))

            for char, color in zip(line, colors):
                r, g, b = color
                colored_line += f"{rgb_to_ansi(r, g, b)}{char}"

            colored_lines.append(colored_line + Style.RESET_ALL)
        else:
            colored_lines.append(line)

    return '\n'.join(colored_lines)

def spinner_animation(duration=3, message="Loading", color=Fore.CYAN):
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0

    try:
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {spinner_chars[i % len(spinner_chars)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()

def typing_animation(text, delay=0.03, color=Fore.CYAN):
    for char in text:
        sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def progress_bar(duration=3, width=50, message="Loading", color=Fore.CYAN):
    for i in range(width + 1):
        progress = i / width
        bar = '█' * i + '░' * (width - i)
        percentage = int(progress * 100)

        sys.stdout.write(f"\r{color}{message} |{bar}| {percentage}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(duration / width)

    sys.stdout.write("\n")
    sys.stdout.flush()

def get_system_info():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    system = platform.system()
    version = "v1.0.0"

    return {
        "date": date_str,
        "time": time_str,
        "system": system,
        "version": version
    }

def display_system_info(color=Fore.CYAN):
    info = get_system_info()

    print(f"{color}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{color}║ TCPASF Advanced Security System          ║{Style.RESET_ALL}")
    print(f"{color}║ Date: {info['date']}  Time: {info['time']}     ║{Style.RESET_ALL}")
    print(f"{color}║ System: {info['system']:<10} Version: {info['version']}      ║{Style.RESET_ALL}")
    print(f"{color}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

def animated_login_attempt(username, success=True, duration=2):
    print(f"\n{Fore.CYAN}Authenticating user: {username}{Style.RESET_ALL}")

    for i in range(3):
        sys.stdout.write(f"\r{Fore.YELLOW}Verifying credentials{'.' * (i + 1)}{' ' * (2 - i)}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(duration / 3)

    if success:
        sys.stdout.write(f"\r{Fore.GREEN}Authentication successful!{' ' * 10}{Style.RESET_ALL}\n")
    else:
        sys.stdout.write(f"\r{Fore.RED}Authentication failed!{' ' * 10}{Style.RESET_ALL}\n")

    sys.stdout.flush()
    time.sleep(0.5)

def clear_screen():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def check_token(token):
    if token.startswith("Bot "):
        return "Bot " + token
    elif token.startswith("Bearer "):
        return "Bearer " + token
    else:
        return None

def nuke_server(token, server_id):
    token = check_token(token)
    if token is None:
        return "Invalid token"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.post(f"https://discord.com/api/v9/guilds/{server_id}/delete", headers=headers)
    if response.status_code == 200:
        return "Server nuked"
    else:
        return "Failed to nuke server"

def nuke_account(token, user_id):
    token = check_token(token)
    if token is None:
        return "Invalid token"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.post(f"https://discord.com/api/v9/users/{user_id}/delete", headers=headers)
    if response.status_code == 200:
        return "Account nuked"
    else:
        return "Failed to nuke account"




