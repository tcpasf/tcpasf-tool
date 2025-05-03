import os
import sys
import subprocess
import platform
import time
from colorama import init, Fore, Style

init(autoreset=True)

def check_command_exists(command):
    try:
        if sys.platform == 'win32':
            result = subprocess.run(['where', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

def install_nmap():
    print(f"{Fore.CYAN}[*] Checking for Nmap installation...{Style.RESET_ALL}")
    
    if check_command_exists('nmap'):
        print(f"{Fore.GREEN}[+] Nmap is already installed.{Style.RESET_ALL}")
        
        try:
            version_output = subprocess.check_output(['nmap', '--version'], stderr=subprocess.STDOUT, text=True)
            version_line = version_output.split('\n')[0]
            print(f"{Fore.GREEN}[+] {version_line}{Style.RESET_ALL}")
        except:
            pass
        
        return True
    
    print(f"{Fore.YELLOW}[!] Nmap is not installed. Attempting to install...{Style.RESET_ALL}")
    
    try:
        if sys.platform == 'win32':
            print(f"{Fore.CYAN}[*] Downloading Nmap installer for Windows...{Style.RESET_ALL}")
            
            import urllib.request
            import tempfile
            
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, "nmap-setup.exe")
            
            url = "https://nmap.org/dist/nmap-7.94-setup.exe"
            
            print(f"{Fore.CYAN}[*] Downloading from: {url}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] This may take a few minutes...{Style.RESET_ALL}")
            
            urllib.request.urlretrieve(url, installer_path)
            
            print(f"{Fore.GREEN}[+] Download complete. Running installer...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Please follow the installation prompts.{Style.RESET_ALL}")
            
            subprocess.run([installer_path], check=True)
            
            print(f"{Fore.GREEN}[+] Nmap installation completed.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] You may need to restart your terminal or computer for the PATH to update.{Style.RESET_ALL}")
            
        elif sys.platform == 'darwin':  # macOS
            print(f"{Fore.CYAN}[*] Installing Nmap via Homebrew...{Style.RESET_ALL}")
            
            if not check_command_exists('brew'):
                print(f"{Fore.RED}[-] Homebrew is not installed. Please install Homebrew first.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Visit https://brew.sh/ for installation instructions.{Style.RESET_ALL}")
                return False
            
            subprocess.run(['brew', 'install', 'nmap'], check=True)
            print(f"{Fore.GREEN}[+] Nmap installation completed.{Style.RESET_ALL}")
            
        else:  # Linux
            distro = ""
            
            if os.path.exists('/etc/debian_version'):
                print(f"{Fore.CYAN}[*] Detected Debian/Ubuntu. Installing via apt...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'nmap'], check=True)
                distro = "debian"
            elif os.path.exists('/etc/fedora-release'):
                print(f"{Fore.CYAN}[*] Detected Fedora. Installing via dnf...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'nmap'], check=True)
                distro = "fedora"
            elif os.path.exists('/etc/arch-release'):
                print(f"{Fore.CYAN}[*] Detected Arch Linux. Installing via pacman...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'nmap'], check=True)
                distro = "arch"
            else:
                print(f"{Fore.RED}[-] Unsupported Linux distribution.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Please install Nmap manually.{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}[+] Nmap installation completed on {distro}.{Style.RESET_ALL}")
        
        # Verify installation
        if check_command_exists('nmap'):
            print(f"{Fore.GREEN}[+] Nmap is now installed and available.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Nmap installation verification failed.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] You may need to restart your terminal or add Nmap to your PATH.{Style.RESET_ALL}")
            return False
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error installing Nmap: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please install Nmap manually.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Visit https://nmap.org/download.html for installation instructions.{Style.RESET_ALL}")
        return False

def install_wireshark():
    print(f"{Fore.CYAN}[*] Checking for Wireshark installation...{Style.RESET_ALL}")
    
    if check_command_exists('wireshark') or check_command_exists('tshark'):
        print(f"{Fore.GREEN}[+] Wireshark is already installed.{Style.RESET_ALL}")
        return True
    
    print(f"{Fore.YELLOW}[!] Wireshark is not installed. Attempting to install...{Style.RESET_ALL}")
    
    try:
        if sys.platform == 'win32':
            print(f"{Fore.CYAN}[*] Downloading Wireshark installer for Windows...{Style.RESET_ALL}")
            
            import urllib.request
            import tempfile
            
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, "wireshark-setup.exe")
            
            url = "https://1.as.dl.wireshark.org/win64/Wireshark-win64-latest.exe"
            
            print(f"{Fore.CYAN}[*] Downloading from: {url}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] This may take a few minutes...{Style.RESET_ALL}")
            
            urllib.request.urlretrieve(url, installer_path)
            
            print(f"{Fore.GREEN}[+] Download complete. Running installer...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Please follow the installation prompts.{Style.RESET_ALL}")
            
            subprocess.run([installer_path], check=True)
            
            print(f"{Fore.GREEN}[+] Wireshark installation completed.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] You may need to restart your terminal or computer for the PATH to update.{Style.RESET_ALL}")
            
        elif sys.platform == 'darwin':  # macOS
            print(f"{Fore.CYAN}[*] Installing Wireshark via Homebrew...{Style.RESET_ALL}")
            
            if not check_command_exists('brew'):
                print(f"{Fore.RED}[-] Homebrew is not installed. Please install Homebrew first.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Visit https://brew.sh/ for installation instructions.{Style.RESET_ALL}")
                return False
            
            subprocess.run(['brew', 'install', 'wireshark'], check=True)
            print(f"{Fore.GREEN}[+] Wireshark installation completed.{Style.RESET_ALL}")
            
        else:  # Linux
            distro = ""
            
            if os.path.exists('/etc/debian_version'):
                print(f"{Fore.CYAN}[*] Detected Debian/Ubuntu. Installing via apt...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'wireshark'], check=True)
                distro = "debian"
            elif os.path.exists('/etc/fedora-release'):
                print(f"{Fore.CYAN}[*] Detected Fedora. Installing via dnf...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'wireshark'], check=True)
                distro = "fedora"
            elif os.path.exists('/etc/arch-release'):
                print(f"{Fore.CYAN}[*] Detected Arch Linux. Installing via pacman...{Style.RESET_ALL}")
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'wireshark-qt'], check=True)
                distro = "arch"
            else:
                print(f"{Fore.RED}[-] Unsupported Linux distribution.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Please install Wireshark manually.{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}[+] Wireshark installation completed on {distro}.{Style.RESET_ALL}")
        
        # Verify installation
        if check_command_exists('wireshark') or check_command_exists('tshark'):
            print(f"{Fore.GREEN}[+] Wireshark is now installed and available.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Wireshark installation verification failed.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] You may need to restart your terminal or add Wireshark to your PATH.{Style.RESET_ALL}")
            return False
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error installing Wireshark: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please install Wireshark manually.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Visit https://www.wireshark.org/download.html for installation instructions.{Style.RESET_ALL}")
        return False

def software_installer_menu():
    while True:
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║         SOFTWARE INSTALLER MENU          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Install Nmap")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Install Wireshark")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Back to Main Menu")
        
        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
        
        if choice == "1":
            install_nmap()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == "2":
            install_wireshark()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == "3":
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
