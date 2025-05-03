import socket
import subprocess
import threading
import time
import sys
import os
import random
import requests
import json
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info
from tools.utils.software_installer import check_command_exists, install_nmap

init(autoreset=True)

def advanced_port_scan(target, port_range=None, scan_type="SYN"):
    if not check_command_exists('nmap'):
        print(f"{Fore.RED}[-] Nmap is required for advanced port scanning.{Style.RESET_ALL}")
        install = input(f"{Fore.CYAN}Do you want to install Nmap now? (y/n): {Style.RESET_ALL}").lower()
        if install == 'y':
            if not install_nmap():
                return
        else:
            return
    
    print(f"\n{Fore.YELLOW}[*] Starting advanced port scan on {target}...{Style.RESET_ALL}")
    
    scan_types = {
        "SYN": "-sS",
        "TCP": "-sT",
        "UDP": "-sU",
        "FIN": "-sF",
        "NULL": "-sN",
        "XMAS": "-sX",
        "ACK": "-sA"
    }
    
    if scan_type not in scan_types:
        print(f"{Fore.RED}[-] Invalid scan type. Using SYN scan.{Style.RESET_ALL}")
        scan_type = "SYN"
    
    nmap_args = [scan_types[scan_type], "-T4"]
    
    if port_range:
        nmap_args.append(f"-p{port_range}")
    
    command = ["nmap"] + nmap_args + [target]
    print(f"{Fore.CYAN}[*] Running command: {' '.join(command)}{Style.RESET_ALL}")
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        spinner = ['|', '/', '-', '\\']
        i = 0
        while process.poll() is None:
            sys.stdout.write(f"\r{Fore.CYAN}[*] Scanning {spinner[i % len(spinner)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"\n{Fore.GREEN}[+] Scan completed successfully:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')
            
            for line in output.splitlines():
                if "PORT" in line and "STATE" in line:
                    print(f"\n{Fore.CYAN}{line}{Style.RESET_ALL}")
                elif "open" in line and ("tcp" in line or "udp" in line):
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                elif "filtered" in line:
                    print(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
                elif "closed" in line:
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                elif any(header in line for header in ["SERVICE", "VERSION", "TRACEROUTE", "SCRIPT"]):
                    print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
                else:
                    print(line)
        else:
            print(f"\n{Fore.RED}[-] Scan failed.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def vulnerability_scan(target):
    if not check_command_exists('nmap'):
        print(f"{Fore.RED}[-] Nmap is required for vulnerability scanning.{Style.RESET_ALL}")
        install = input(f"{Fore.CYAN}Do you want to install Nmap now? (y/n): {Style.RESET_ALL}").lower()
        if install == 'y':
            if not install_nmap():
                return
        else:
            return
    
    print(f"\n{Fore.YELLOW}[*] Starting vulnerability scan on {target}...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] This may take several minutes...{Style.RESET_ALL}")
    
    command = ["nmap", "-sV", "--script", "vuln", "-T4", target]
    print(f"{Fore.CYAN}[*] Running command: {' '.join(command)}{Style.RESET_ALL}")
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        spinner = ['|', '/', '-', '\\']
        i = 0
        while process.poll() is None:
            sys.stdout.write(f"\r{Fore.CYAN}[*] Scanning for vulnerabilities {spinner[i % len(spinner)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"\n{Fore.GREEN}[+] Vulnerability scan completed:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')
            
            vulnerabilities_found = False
            
            for line in output.splitlines():
                if "VULNERABLE" in line:
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                    vulnerabilities_found = True
                elif "CVE" in line:
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                    vulnerabilities_found = True
                elif "PORT" in line and "STATE" in line:
                    print(f"\n{Fore.CYAN}{line}{Style.RESET_ALL}")
                elif "open" in line and "tcp" in line:
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                elif "|" in line and "VULNERABLE" not in line and "CVE" not in line:
                    print(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
                else:
                    print(line)
            
            if not vulnerabilities_found:
                print(f"\n{Fore.GREEN}[+] No obvious vulnerabilities found.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[-] Scan failed.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def network_mapping(target_network):
    if not check_command_exists('nmap'):
        print(f"{Fore.RED}[-] Nmap is required for network mapping.{Style.RESET_ALL}")
        install = input(f"{Fore.CYAN}Do you want to install Nmap now? (y/n): {Style.RESET_ALL}").lower()
        if install == 'y':
            if not install_nmap():
                return
        else:
            return
    
    print(f"\n{Fore.YELLOW}[*] Mapping network: {target_network}...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] This may take several minutes...{Style.RESET_ALL}")
    
    command = ["nmap", "-sn", target_network]
    print(f"{Fore.CYAN}[*] Running command: {' '.join(command)}{Style.RESET_ALL}")
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        spinner = ['|', '/', '-', '\\']
        i = 0
        while process.poll() is None:
            sys.stdout.write(f"\r{Fore.CYAN}[*] Mapping network {spinner[i % len(spinner)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"\n{Fore.GREEN}[+] Network mapping completed:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')
            
            hosts = []
            current_ip = None
            
            for line in output.splitlines():
                if "Nmap scan report for" in line:
                    if "(" in line and ")" in line:
                        parts = line.split("(")
                        hostname = parts[0].replace("Nmap scan report for", "").strip()
                        ip = parts[1].replace(")", "").strip()
                    else:
                        hostname = ""
                        ip = line.replace("Nmap scan report for", "").strip()
                    
                    current_ip = ip
                    hosts.append({"ip": ip, "hostname": hostname, "status": ""})
                
                if "Host is up" in line and current_ip:
                    for host in hosts:
                        if host["ip"] == current_ip:
                            host["status"] = "up"
                            break
                
                if "Host is down" in line and current_ip:
                    for host in hosts:
                        if host["ip"] == current_ip:
                            host["status"] = "down"
                            break
            
            print(f"\n{Fore.CYAN}{'IP Address':<20} {'Hostname':<30} {'Status'}{Style.RESET_ALL}")
            print("-" * 60)
            
            for host in hosts:
                status_color = Fore.GREEN if host["status"] == "up" else Fore.RED
                print(f"{host['ip']:<20} {host['hostname']:<30} {status_color}{host['status']}{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}[+] Found {len([h for h in hosts if h['status'] == 'up'])} active hosts out of {len(hosts)} total.{Style.RESET_ALL}")
            
            save = input(f"\n{Fore.CYAN}Save results to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"network_map_{target_network.replace('/', '_')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Network Mapping Results for {target_network}\n")
                    f.write(f"{'IP Address':<20} {'Hostname':<30} {'Status'}\n")
                    f.write("-" * 60 + "\n")
                    for host in hosts:
                        f.write(f"{host['ip']:<20} {host['hostname']:<30} {host['status']}\n")
                print(f"{Fore.GREEN}[+] Results saved to {filename}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[-] Network mapping failed.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def packet_capture():
    if not check_command_exists('tshark'):
        print(f"{Fore.RED}[-] Wireshark/tshark is required for packet capture.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please install Wireshark manually.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Visit https://www.wireshark.org/download.html for installation instructions.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}[*] Starting packet capture...{Style.RESET_ALL}")
    
    interfaces = []
    
    try:
        if sys.platform == 'win32':
            output = subprocess.check_output(['tshark', '-D'], text=True)
            for line in output.splitlines():
                if line.strip():
                    interfaces.append(line)
        else:
            output = subprocess.check_output(['tshark', '-D'], text=True)
            for line in output.splitlines():
                if line.strip():
                    interfaces.append(line)
        
        print(f"\n{Fore.CYAN}Available Interfaces:{Style.RESET_ALL}")
        for i, interface in enumerate(interfaces, 1):
            print(f"{Fore.CYAN}[{i}]{Style.RESET_ALL} {interface}")
        
        interface_choice = input(f"\n{Fore.CYAN}Select interface number: {Style.RESET_ALL}")
        
        if not interface_choice.isdigit() or int(interface_choice) < 1 or int(interface_choice) > len(interfaces):
            print(f"{Fore.RED}[-] Invalid interface selection.{Style.RESET_ALL}")
            return
        
        selected_interface = interfaces[int(interface_choice) - 1].split('.')[0]
        
        capture_filter = input(f"\n{Fore.CYAN}Enter capture filter (e.g., 'port 80' or 'host 192.168.1.1') or leave empty: {Style.RESET_ALL}")
        
        duration = input(f"\n{Fore.CYAN}Enter capture duration in seconds (default: 30): {Style.RESET_ALL}")
        if not duration.isdigit():
            duration = 30
        else:
            duration = int(duration)
        
        packet_count = input(f"\n{Fore.CYAN}Enter maximum number of packets to capture (default: 1000): {Style.RESET_ALL}")
        if not packet_count.isdigit():
            packet_count = 1000
        else:
            packet_count = int(packet_count)
        
        output_file = f"packet_capture_{time.strftime('%Y%m%d_%H%M%S')}.pcap"
        
        command = ['tshark', '-i', selected_interface, '-w', output_file, '-c', str(packet_count)]
        
        if capture_filter:
            command.extend(['-f', capture_filter])
        
        print(f"\n{Fore.YELLOW}[*] Starting packet capture with command: {' '.join(command)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Capturing for {duration} seconds or {packet_count} packets...{Style.RESET_ALL}")
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        start_time = time.time()
        end_time = start_time + duration
        
        try:
            while time.time() < end_time and process.poll() is None:
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                sys.stdout.write(f"\r{Fore.CYAN}[*] Capturing packets... {int(elapsed)}s elapsed, {int(remaining)}s remaining{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
            
            if process.poll() is None:
                process.terminate()
            
            stdout, stderr = process.communicate()
            
            print(f"\n\n{Fore.GREEN}[+] Packet capture completed.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Capture saved to: {output_file}{Style.RESET_ALL}")
            
            analyze = input(f"\n{Fore.CYAN}Analyze captured packets? (y/n): {Style.RESET_ALL}").lower()
            if analyze == 'y':
                print(f"\n{Fore.YELLOW}[*] Analyzing packet capture...{Style.RESET_ALL}")
                
                analyze_command = ['tshark', '-r', output_file, '-T', 'fields', '-e', 'frame.number', '-e', 'ip.src', '-e', 'ip.dst', '-e', 'ip.proto', '-E', 'header=y']
                
                analyze_process = subprocess.Popen(analyze_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                analyze_stdout, analyze_stderr = analyze_process.communicate()
                
                if analyze_process.returncode == 0:
                    print(f"\n{Fore.GREEN}[+] Packet Analysis:{Style.RESET_ALL}")
                    print(analyze_stdout.decode('utf-8', errors='ignore'))
                else:
                    print(f"\n{Fore.RED}[-] Analysis failed.{Style.RESET_ALL}")
                    if analyze_stderr:
                        print(f"{Fore.RED}Error: {analyze_stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            if process.poll() is None:
                process.terminate()
            print(f"\n\n{Fore.YELLOW}[!] Packet capture stopped by user.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Capture saved to: {output_file}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def network_security_tools_menu():
    while True:
        clear_screen()
        print(generate_category_ascii("NETWORK SECURITY"))
        display_system_info()
        
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║       NETWORK SECURITY TOOLS MENU        ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Advanced Port Scanner")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Vulnerability Scanner")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Network Mapping")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Packet Capture (Requires Wireshark)")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Install Security Tools")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Back to Main Menu")
        
        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
        
        if choice == "1":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            port_range = input(f"{Fore.CYAN}Enter port range (e.g., 1-1000) or leave empty for default: {Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Scan Types:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} SYN Scan (Stealthy, Default)")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} TCP Connect Scan (Full TCP handshake)")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} UDP Scan")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} FIN Scan (Stealthy)")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} NULL Scan (Stealthy)")
            print(f"{Fore.CYAN}[6]{Style.RESET_ALL} XMAS Scan (Stealthy)")
            print(f"{Fore.CYAN}[7]{Style.RESET_ALL} ACK Scan (Firewall rule detection)")
            
            scan_choice = input(f"\n{Fore.CYAN}Select scan type (default: 1): {Style.RESET_ALL}")
            
            scan_type = "SYN"
            if scan_choice == "2":
                scan_type = "TCP"
            elif scan_choice == "3":
                scan_type = "UDP"
            elif scan_choice == "4":
                scan_type = "FIN"
            elif scan_choice == "5":
                scan_type = "NULL"
            elif scan_choice == "6":
                scan_type = "XMAS"
            elif scan_choice == "7":
                scan_type = "ACK"
            
            advanced_port_scan(target, port_range, scan_type)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "2":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            vulnerability_scan(target)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "3":
            target_network = input(f"\n{Fore.CYAN}Enter target network (e.g., 192.168.1.0/24): {Style.RESET_ALL}")
            network_mapping(target_network)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "4":
            packet_capture()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "5":
            from tools.utils.software_installer import software_installer_menu
            software_installer_menu()
        
        elif choice == "6":
            break
        
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
