import socket
import requests
import json
import subprocess
import threading
import time
import sys
import os
import random
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info

init(autoreset=True)

def ip_lookup(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()

        if data["status"] == "success":
            print(f"\n{Fore.GREEN}[+] IP Information for {ip_address}:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Country: {Style.RESET_ALL}{data.get('country', 'N/A')}")
            print(f"{Fore.CYAN}Region: {Style.RESET_ALL}{data.get('regionName', 'N/A')}")
            print(f"{Fore.CYAN}City: {Style.RESET_ALL}{data.get('city', 'N/A')}")
            print(f"{Fore.CYAN}ZIP: {Style.RESET_ALL}{data.get('zip', 'N/A')}")
            print(f"{Fore.CYAN}Latitude: {Style.RESET_ALL}{data.get('lat', 'N/A')}")
            print(f"{Fore.CYAN}Longitude: {Style.RESET_ALL}{data.get('lon', 'N/A')}")
            print(f"{Fore.CYAN}ISP: {Style.RESET_ALL}{data.get('isp', 'N/A')}")
            print(f"{Fore.CYAN}Organization: {Style.RESET_ALL}{data.get('org', 'N/A')}")
            print(f"{Fore.CYAN}AS: {Style.RESET_ALL}{data.get('as', 'N/A')}")
        else:
            print(f"\n{Fore.RED}[-] Failed to retrieve information for {ip_address}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def port_scanner(target, port_range=None):
    if port_range is None:
        port_range = range(1, 1025)
    elif isinstance(port_range, str):
        try:
            if "-" in port_range:
                start, end = map(int, port_range.split("-"))
                port_range = range(start, end + 1)
            else:
                port_range = [int(port_range)]
        except:
            print(f"{Fore.RED}[-] Invalid port range. Using default (1-1024).{Style.RESET_ALL}")
            port_range = range(1, 1025)

    open_ports = []
    total_ports = len(list(port_range))
    scanned = 0

    print(f"\n{Fore.YELLOW}[*] Starting port scan on {target}...{Style.RESET_ALL}")

    def scan_port(port):
        nonlocal scanned
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = "Unknown"
            try:
                service = socket.getservbyport(port)
            except:
                pass
            open_ports.append((port, service))
            print(f"{Fore.GREEN}[+] Port {port}: Open - {service}{Style.RESET_ALL}")
        sock.close()
        scanned += 1
        sys.stdout.write(f"\r{Fore.CYAN}[*] Progress: {scanned}/{total_ports} ports scanned ({int(scanned/total_ports*100)}%){Style.RESET_ALL}")
        sys.stdout.flush()

    threads = []
    for port in port_range:
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    print(f"\n\n{Fore.YELLOW}[*] Scan completed. Found {len(open_ports)} open ports.{Style.RESET_ALL}")

    if open_ports:
        print(f"\n{Fore.GREEN}[+] Open Ports Summary:{Style.RESET_ALL}")
        for port, service in open_ports:
            print(f"{Fore.CYAN}Port {port}: {Style.RESET_ALL}{service}")

    return open_ports

def domain_checker(domain):
    print(f"\n{Fore.YELLOW}[*] Checking domain information for {domain}...{Style.RESET_ALL}")

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}[+] Domain resolves to IP: {ip_address}{Style.RESET_ALL}")

        try:
            import whois
            w = whois.whois(domain)
            if w.domain_name:
                print(f"{Fore.GREEN}[+] Domain is registered{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Registrar: {Style.RESET_ALL}{w.registrar}")
                print(f"{Fore.CYAN}Creation Date: {Style.RESET_ALL}{w.creation_date}")
                print(f"{Fore.CYAN}Expiration Date: {Style.RESET_ALL}{w.expiration_date}")
                print(f"{Fore.CYAN}Name Servers: {Style.RESET_ALL}{', '.join(w.name_servers) if isinstance(w.name_servers, list) else w.name_servers}")
            else:
                print(f"{Fore.RED}[-] Domain is not registered{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.YELLOW}[!] Python-whois module not installed. WHOIS information not available.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error retrieving WHOIS information: {str(e)}{Style.RESET_ALL}")

        try:
            http_response = requests.get(f"http://{domain}", timeout=5)
            print(f"{Fore.GREEN}[+] HTTP Status: {http_response.status_code}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[-] HTTP connection failed{Style.RESET_ALL}")

        try:
            https_response = requests.get(f"https://{domain}", timeout=5)
            print(f"{Fore.GREEN}[+] HTTPS Status: {https_response.status_code}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[-] HTTPS connection failed{Style.RESET_ALL}")

        try:
            import dns.resolver

            print(f"\n{Fore.CYAN}DNS Records:{Style.RESET_ALL}")

            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    print(f"{Fore.GREEN}[+] {record_type} Records:{Style.RESET_ALL}")
                    for rdata in answers:
                        print(f"  {rdata}")
                except:
                    print(f"{Fore.YELLOW}[!] No {record_type} records found{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.YELLOW}[!] Dnspython module not installed. DNS records not available.{Style.RESET_ALL}")

    except socket.gaierror:
        print(f"{Fore.RED}[-] Domain does not exist or cannot be resolved{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def ping_tool(target, count=4):
    print(f"\n{Fore.YELLOW}[*] Pinging {target}...{Style.RESET_ALL}")

    try:
        param = '-n' if sys.platform.lower() == 'win32' else '-c'
        command = ['ping', param, str(count), target]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"{Fore.GREEN}[+] Ping successful:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')
            for line in output.splitlines():
                if "time=" in line or "time<" in line:
                    print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")

            if "Average" in output:
                for line in output.splitlines():
                    if "Average" in line:
                        print(f"\n{Fore.GREEN}[+] {line}{Style.RESET_ALL}")
            elif "min/avg/max" in output:
                for line in output.splitlines():
                    if "min/avg/max" in line:
                        print(f"\n{Fore.GREEN}[+] {line}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Ping failed. Target may be down or blocking ICMP.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def nmap_scan(target, scan_type="basic"):
    print(f"\n{Fore.YELLOW}[*] Starting Nmap scan on {target}...{Style.RESET_ALL}")

    try:
        try:
            subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print(f"{Fore.RED}[-] Nmap is not installed or not in PATH. Please install Nmap first.{Style.RESET_ALL}")
            return

        scan_types = {
            "basic": ["-sV", "-T4"],
            "quick": ["-T4", "-F"],
            "comprehensive": ["-sS", "-sV", "-sC", "-A", "-T4"],
            "vuln": ["--script", "vuln", "-T4"],
            "all_ports": ["-p-", "-T4"]
        }

        if scan_type not in scan_types:
            print(f"{Fore.RED}[-] Invalid scan type. Using basic scan.{Style.RESET_ALL}")
            scan_type = "basic"

        command = ["nmap"] + scan_types[scan_type] + [target]
        print(f"{Fore.CYAN}[*] Running command: {' '.join(command)}{Style.RESET_ALL}")

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
            print(f"\n{Fore.GREEN}[+] Nmap scan completed successfully:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')

            for line in output.splitlines():
                if "PORT" in line and "STATE" in line:
                    print(f"\n{Fore.CYAN}{line}{Style.RESET_ALL}")
                elif "open" in line and "tcp" in line:
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
            print(f"\n{Fore.RED}[-] Nmap scan failed.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def traceroute(target):
    print(f"\n{Fore.YELLOW}[*] Running traceroute to {target}...{Style.RESET_ALL}")

    try:
        command = 'tracert' if sys.platform.lower() == 'win32' else 'traceroute'
        process = subprocess.Popen([command, target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        spinner = ['|', '/', '-', '\\']
        i = 0
        while process.poll() is None:
            sys.stdout.write(f"\r{Fore.CYAN}[*] Tracing route {spinner[i % len(spinner)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"\n{Fore.GREEN}[+] Traceroute completed:{Style.RESET_ALL}")
            output = stdout.decode('utf-8', errors='ignore')

            for line in output.splitlines():
                if "ms" in line and not line.startswith("Tracing") and not line.startswith("Trace"):
                    parts = line.split()
                    hop_num = parts[0].strip()

                    colored_line = line
                    for part in parts:
                        if "ms" in part:
                            try:
                                time_ms = float(part.replace("ms", ""))
                                if time_ms < 50:
                                    colored_part = f"{Fore.GREEN}{part}{Style.RESET_ALL}"
                                elif time_ms < 100:
                                    colored_part = f"{Fore.YELLOW}{part}{Style.RESET_ALL}"
                                else:
                                    colored_part = f"{Fore.RED}{part}{Style.RESET_ALL}"
                                colored_line = colored_line.replace(part, colored_part)
                            except:
                                pass

                    print(colored_line)
                else:
                    print(line)
        else:
            print(f"\n{Fore.RED}[-] Traceroute failed.{Style.RESET_ALL}")
            if stderr:
                print(f"{Fore.RED}Error: {stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def dns_lookup(domain, record_type="A"):
    print(f"\n{Fore.YELLOW}[*] Looking up {record_type} records for {domain}...{Style.RESET_ALL}")

    try:
        import dns.resolver

        valid_types = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "SRV", "PTR"]
        if record_type not in valid_types:
            print(f"{Fore.RED}[-] Invalid record type. Valid types are: {', '.join(valid_types)}{Style.RESET_ALL}")
            return

        answers = dns.resolver.resolve(domain, record_type)

        print(f"{Fore.GREEN}[+] {record_type} Records for {domain}:{Style.RESET_ALL}")
        for rdata in answers:
            print(f"  {Fore.CYAN}{rdata}{Style.RESET_ALL}")

    except ImportError:
        print(f"{Fore.RED}[-] Dnspython module not installed. Please install it with 'pip install dnspython'.{Style.RESET_ALL}")
    except dns.resolver.NXDOMAIN:
        print(f"{Fore.RED}[-] Domain does not exist.{Style.RESET_ALL}")
    except dns.resolver.NoAnswer:
        print(f"{Fore.RED}[-] No {record_type} records found for {domain}.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def ip_tools_menu():
    while True:
        clear_screen()
        print(generate_category_ascii("IP TOOLS"))
        display_system_info()

        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║             IP TOOLS MENU                ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} IP Lookup")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Port Scanner")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Domain Checker")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Ping Tool")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Nmap Scanner")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Traceroute")
        print(f"{Fore.CYAN}[7]{Style.RESET_ALL} DNS Lookup")
        print(f"{Fore.CYAN}[8]{Style.RESET_ALL} Back to Main Menu")

        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

        if choice == "1":
            ip = input(f"\n{Fore.CYAN}Enter IP address: {Style.RESET_ALL}")
            ip_lookup(ip)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "2":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            port_range = input(f"{Fore.CYAN}Enter port range (e.g., 1-100) or leave empty for default (1-1024): {Style.RESET_ALL}")
            if not port_range:
                port_range = None
            port_scanner(target, port_range)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "3":
            domain = input(f"\n{Fore.CYAN}Enter domain name: {Style.RESET_ALL}")
            domain_checker(domain)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "4":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            count = input(f"{Fore.CYAN}Enter number of pings (default: 4): {Style.RESET_ALL}")
            if not count.isdigit():
                count = 4
            else:
                count = int(count)
            ping_tool(target, count)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "5":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Scan Types:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Basic (Version Detection)")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Quick (Fast Scan)")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Comprehensive (Service, OS, Scripts)")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Vulnerability Scan")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} All Ports")

            scan_choice = input(f"\n{Fore.CYAN}Select scan type (default: 1): {Style.RESET_ALL}")
            scan_type = "basic"

            if scan_choice == "2":
                scan_type = "quick"
            elif scan_choice == "3":
                scan_type = "comprehensive"
            elif scan_choice == "4":
                scan_type = "vuln"
            elif scan_choice == "5":
                scan_type = "all_ports"

            nmap_scan(target, scan_type)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "6":
            target = input(f"\n{Fore.CYAN}Enter target IP/domain: {Style.RESET_ALL}")
            traceroute(target)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "7":
            domain = input(f"\n{Fore.CYAN}Enter domain name: {Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Record Types:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} A (IPv4)")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} AAAA (IPv6)")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} CNAME (Canonical Name)")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} MX (Mail Exchange)")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} NS (Name Server)")
            print(f"{Fore.CYAN}[6]{Style.RESET_ALL} TXT (Text)")
            print(f"{Fore.CYAN}[7]{Style.RESET_ALL} SOA (Start of Authority)")
            print(f"{Fore.CYAN}[8]{Style.RESET_ALL} SRV (Service)")
            print(f"{Fore.CYAN}[9]{Style.RESET_ALL} PTR (Pointer)")

            record_choice = input(f"\n{Fore.CYAN}Select record type (default: 1): {Style.RESET_ALL}")
            record_type = "A"

            if record_choice == "2":
                record_type = "AAAA"
            elif record_choice == "3":
                record_type = "CNAME"
            elif record_choice == "4":
                record_type = "MX"
            elif record_choice == "5":
                record_type = "NS"
            elif record_choice == "6":
                record_type = "TXT"
            elif record_choice == "7":
                record_type = "SOA"
            elif record_choice == "8":
                record_type = "SRV"
            elif record_choice == "9":
                record_type = "PTR"

            dns_lookup(domain, record_type)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "8":
            break

        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
