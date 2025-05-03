import os
import sys
import platform
import psutil
import time
import subprocess
import socket
import uuid
import json
from datetime import datetime
from colorama import init, Fore, Style

from tools.ascii_generator import generate_category_ascii, clear_screen, spinner_animation, typing_animation, display_system_info

init(autoreset=True)

def get_system_info_detailed():
    print(f"\n{Fore.YELLOW}[*] Gathering detailed system information...{Style.RESET_ALL}")
    
    try:
        info = {}
        
        # System information
        info["system"] = platform.system()
        info["node"] = platform.node()
        info["release"] = platform.release()
        info["version"] = platform.version()
        info["machine"] = platform.machine()
        info["processor"] = platform.processor()
        
        # Python information
        info["python_version"] = platform.python_version()
        info["python_compiler"] = platform.python_compiler()
        info["python_implementation"] = platform.python_implementation()
        
        # CPU information
        info["cpu_count_physical"] = psutil.cpu_count(logical=False)
        info["cpu_count_logical"] = psutil.cpu_count(logical=True)
        info["cpu_freq"] = psutil.cpu_freq()
        
        # Memory information
        memory = psutil.virtual_memory()
        info["memory_total"] = memory.total
        info["memory_available"] = memory.available
        info["memory_used"] = memory.used
        info["memory_percent"] = memory.percent
        
        # Disk information
        disk = psutil.disk_usage('/')
        info["disk_total"] = disk.total
        info["disk_used"] = disk.used
        info["disk_free"] = disk.free
        info["disk_percent"] = disk.percent
        
        # Network information
        info["hostname"] = socket.gethostname()
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
        info["mac_address"] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 48, 8)][::-1])
        
        # Boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        info["boot_time"] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Display information
        print(f"\n{Fore.GREEN}[+] System Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}System: {Style.RESET_ALL}{info['system']}")
        print(f"{Fore.CYAN}Hostname: {Style.RESET_ALL}{info['node']}")
        print(f"{Fore.CYAN}Release: {Style.RESET_ALL}{info['release']}")
        print(f"{Fore.CYAN}Version: {Style.RESET_ALL}{info['version']}")
        print(f"{Fore.CYAN}Machine: {Style.RESET_ALL}{info['machine']}")
        print(f"{Fore.CYAN}Processor: {Style.RESET_ALL}{info['processor']}")
        
        print(f"\n{Fore.GREEN}[+] Python Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Version: {Style.RESET_ALL}{info['python_version']}")
        print(f"{Fore.CYAN}Compiler: {Style.RESET_ALL}{info['python_compiler']}")
        print(f"{Fore.CYAN}Implementation: {Style.RESET_ALL}{info['python_implementation']}")
        
        print(f"\n{Fore.GREEN}[+] CPU Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Physical cores: {Style.RESET_ALL}{info['cpu_count_physical']}")
        print(f"{Fore.CYAN}Logical cores: {Style.RESET_ALL}{info['cpu_count_logical']}")
        if info['cpu_freq']:
            print(f"{Fore.CYAN}CPU frequency: {Style.RESET_ALL}{info['cpu_freq'].current:.2f} MHz")
        
        print(f"\n{Fore.GREEN}[+] Memory Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total: {Style.RESET_ALL}{info['memory_total'] / (1024 ** 3):.2f} GB")
        print(f"{Fore.CYAN}Available: {Style.RESET_ALL}{info['memory_available'] / (1024 ** 3):.2f} GB")
        print(f"{Fore.CYAN}Used: {Style.RESET_ALL}{info['memory_used'] / (1024 ** 3):.2f} GB ({info['memory_percent']}%)")
        
        print(f"\n{Fore.GREEN}[+] Disk Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total: {Style.RESET_ALL}{info['disk_total'] / (1024 ** 3):.2f} GB")
        print(f"{Fore.CYAN}Used: {Style.RESET_ALL}{info['disk_used'] / (1024 ** 3):.2f} GB ({info['disk_percent']}%)")
        print(f"{Fore.CYAN}Free: {Style.RESET_ALL}{info['disk_free'] / (1024 ** 3):.2f} GB")
        
        print(f"\n{Fore.GREEN}[+] Network Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Hostname: {Style.RESET_ALL}{info['hostname']}")
        print(f"{Fore.CYAN}IP Address: {Style.RESET_ALL}{info['ip_address']}")
        print(f"{Fore.CYAN}MAC Address: {Style.RESET_ALL}{info['mac_address']}")
        
        print(f"\n{Fore.GREEN}[+] Boot Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Boot Time: {Style.RESET_ALL}{info['boot_time']}")
        
        save = input(f"\n{Fore.CYAN}Save system information to file? (y/n): {Style.RESET_ALL}").lower()
        if save == 'y':
            filename = f"system_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(info, f, indent=4)
            print(f"{Fore.GREEN}[+] System information saved to {filename}{Style.RESET_ALL}")
        
        return info
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error gathering system information: {str(e)}{Style.RESET_ALL}")
        return None

def monitor_system_resources(duration=60, interval=1):
    print(f"\n{Fore.YELLOW}[*] Monitoring system resources for {duration} seconds (Ctrl+C to stop)...{Style.RESET_ALL}")
    
    try:
        cpu_percentages = []
        memory_percentages = []
        timestamps = []
        
        start_time = time.time()
        end_time = start_time + duration
        
        print(f"\n{Fore.CYAN}{'Time':<12} {'CPU %':<10} {'Memory %':<10} {'Disk %':<10}{Style.RESET_ALL}")
        print("-" * 50)
        
        while time.time() < end_time:
            current_time = time.time()
            elapsed = current_time - start_time
            
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            cpu_color = Fore.GREEN
            if cpu_percent > 50:
                cpu_color = Fore.YELLOW
            if cpu_percent > 80:
                cpu_color = Fore.RED
            
            memory_color = Fore.GREEN
            if memory_percent > 50:
                memory_color = Fore.YELLOW
            if memory_percent > 80:
                memory_color = Fore.RED
            
            disk_color = Fore.GREEN
            if disk_percent > 50:
                disk_color = Fore.YELLOW
            if disk_percent > 80:
                disk_color = Fore.RED
            
            print(f"{timestamp:<12} {cpu_color}{cpu_percent:<10.1f}{Style.RESET_ALL} {memory_color}{memory_percent:<10.1f}{Style.RESET_ALL} {disk_color}{disk_percent:<10.1f}{Style.RESET_ALL}")
            
            cpu_percentages.append(cpu_percent)
            memory_percentages.append(memory_percent)
            timestamps.append(timestamp)
            
            time.sleep(interval)
        
        print(f"\n{Fore.GREEN}[+] Monitoring completed.{Style.RESET_ALL}")
        
        if cpu_percentages:
            avg_cpu = sum(cpu_percentages) / len(cpu_percentages)
            max_cpu = max(cpu_percentages)
            min_cpu = min(cpu_percentages)
            
            avg_memory = sum(memory_percentages) / len(memory_percentages)
            max_memory = max(memory_percentages)
            min_memory = min(memory_percentages)
            
            print(f"\n{Fore.GREEN}[+] Summary:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}CPU Usage: {Style.RESET_ALL}Avg: {avg_cpu:.1f}%, Max: {max_cpu:.1f}%, Min: {min_cpu:.1f}%")
            print(f"{Fore.CYAN}Memory Usage: {Style.RESET_ALL}Avg: {avg_memory:.1f}%, Max: {max_memory:.1f}%, Min: {min_memory:.1f}%")
            
            save = input(f"\n{Fore.CYAN}Save monitoring data to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"system_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(filename, 'w') as f:
                    f.write("Timestamp,CPU %,Memory %\n")
                    for i in range(len(timestamps)):
                        f.write(f"{timestamps[i]},{cpu_percentages[i]:.1f},{memory_percentages[i]:.1f}\n")
                print(f"{Fore.GREEN}[+] Monitoring data saved to {filename}{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Monitoring stopped by user.{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error monitoring system resources: {str(e)}{Style.RESET_ALL}")

def list_processes():
    print(f"\n{Fore.YELLOW}[*] Listing running processes...{Style.RESET_ALL}")
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent', 'create_time']):
            try:
                proc_info = proc.info
                proc_info['create_time'] = datetime.fromtimestamp(proc_info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort processes by memory usage
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        print(f"\n{Fore.CYAN}{'PID':<10} {'Name':<30} {'User':<15} {'Memory %':<10} {'CPU %':<10} {'Created':<20}{Style.RESET_ALL}")
        print("-" * 95)
        
        for proc in processes[:50]:  # Show top 50 processes by memory usage
            memory_color = Fore.GREEN
            if proc['memory_percent'] > 1.0:
                memory_color = Fore.YELLOW
            if proc['memory_percent'] > 5.0:
                memory_color = Fore.RED
            
            cpu_color = Fore.GREEN
            if proc['cpu_percent'] > 10.0:
                cpu_color = Fore.YELLOW
            if proc['cpu_percent'] > 50.0:
                cpu_color = Fore.RED
            
            print(f"{proc['pid']:<10} {proc['name'][:30]:<30} {proc['username'][:15]:<15} {memory_color}{proc['memory_percent']:<10.2f}{Style.RESET_ALL} {cpu_color}{proc['cpu_percent']:<10.2f}{Style.RESET_ALL} {proc['create_time']:<20}")
        
        print(f"\n{Fore.GREEN}[+] Showing top 50 processes by memory usage out of {len(processes)} total processes.{Style.RESET_ALL}")
        
        save = input(f"\n{Fore.CYAN}Save process list to file? (y/n): {Style.RESET_ALL}").lower()
        if save == 'y':
            filename = f"process_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w') as f:
                f.write("PID,Name,User,Memory %,CPU %,Created\n")
                for proc in processes:
                    f.write(f"{proc['pid']},{proc['name']},{proc['username']},{proc['memory_percent']:.2f},{proc['cpu_percent']:.2f},{proc['create_time']}\n")
            print(f"{Fore.GREEN}[+] Process list saved to {filename}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error listing processes: {str(e)}{Style.RESET_ALL}")

def kill_process():
    print(f"\n{Fore.YELLOW}[*] Kill Process Tool{Style.RESET_ALL}")
    
    try:
        pid = input(f"\n{Fore.CYAN}Enter PID of process to kill (or 'list' to see processes): {Style.RESET_ALL}")
        
        if pid.lower() == 'list':
            list_processes()
            pid = input(f"\n{Fore.CYAN}Enter PID of process to kill: {Style.RESET_ALL}")
        
        if not pid.isdigit():
            print(f"{Fore.RED}[-] Invalid PID. Please enter a numeric PID.{Style.RESET_ALL}")
            return
        
        pid = int(pid)
        
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            
            confirm = input(f"{Fore.RED}[!] Are you sure you want to kill process {pid} ({process_name})? (y/n): {Style.RESET_ALL}").lower()
            
            if confirm == 'y':
                process.terminate()
                
                # Wait for process to terminate
                gone, alive = psutil.wait_procs([process], timeout=3)
                
                if process in alive:
                    print(f"{Fore.YELLOW}[!] Process did not terminate gracefully. Killing forcefully...{Style.RESET_ALL}")
                    process.kill()
                
                print(f"{Fore.GREEN}[+] Process {pid} ({process_name}) has been terminated.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Process termination cancelled.{Style.RESET_ALL}")
        
        except psutil.NoSuchProcess:
            print(f"{Fore.RED}[-] No process found with PID {pid}.{Style.RESET_ALL}")
        except psutil.AccessDenied:
            print(f"{Fore.RED}[-] Access denied. You may need administrative privileges to kill this process.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error killing process: {str(e)}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")

def network_connections():
    print(f"\n{Fore.YELLOW}[*] Listing network connections...{Style.RESET_ALL}")
    
    try:
        connections = psutil.net_connections(kind='inet')
        
        print(f"\n{Fore.CYAN}{'Protocol':<10} {'Local Address':<25} {'Remote Address':<25} {'Status':<15} {'PID':<10} {'Process':<20}{Style.RESET_ALL}")
        print("-" * 105)
        
        for conn in connections:
            try:
                protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                
                local_address = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                status = conn.status if hasattr(conn, 'status') else "N/A"
                pid = conn.pid if conn.pid else "N/A"
                
                process_name = "N/A"
                if pid != "N/A":
                    try:
                        process = psutil.Process(pid)
                        process_name = process.name()
                    except:
                        pass
                
                status_color = Fore.GREEN
                if status == "LISTEN":
                    status_color = Fore.CYAN
                elif status == "ESTABLISHED":
                    status_color = Fore.GREEN
                elif status == "TIME_WAIT":
                    status_color = Fore.YELLOW
                elif status == "CLOSE_WAIT":
                    status_color = Fore.RED
                
                print(f"{protocol:<10} {local_address:<25} {remote_address:<25} {status_color}{status:<15}{Style.RESET_ALL} {pid:<10} {process_name:<20}")
            
            except:
                pass
        
        print(f"\n{Fore.GREEN}[+] Found {len(connections)} network connections.{Style.RESET_ALL}")
        
        save = input(f"\n{Fore.CYAN}Save network connections to file? (y/n): {Style.RESET_ALL}").lower()
        if save == 'y':
            filename = f"network_connections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w') as f:
                f.write("Protocol,Local Address,Remote Address,Status,PID,Process\n")
                for conn in connections:
                    try:
                        protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                        local_address = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                        remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        status = conn.status if hasattr(conn, 'status') else "N/A"
                        pid = conn.pid if conn.pid else "N/A"
                        
                        process_name = "N/A"
                        if pid != "N/A":
                            try:
                                process = psutil.Process(pid)
                                process_name = process.name()
                            except:
                                pass
                        
                        f.write(f"{protocol},{local_address},{remote_address},{status},{pid},{process_name}\n")
                    except:
                        pass
            print(f"{Fore.GREEN}[+] Network connections saved to {filename}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[-] Error listing network connections: {str(e)}{Style.RESET_ALL}")

def system_tools_menu():
    while True:
        clear_screen()
        print(generate_category_ascii("SYSTEM TOOLS"))
        display_system_info()
        
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║           SYSTEM TOOLS MENU              ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} System Information")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Monitor System Resources")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} List Running Processes")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Kill Process")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Network Connections")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Back to Main Menu")
        
        choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")
        
        if choice == "1":
            get_system_info_detailed()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "2":
            duration = input(f"\n{Fore.CYAN}Enter monitoring duration in seconds (default: 60): {Style.RESET_ALL}")
            if not duration.isdigit():
                duration = 60
            else:
                duration = int(duration)
            
            interval = input(f"{Fore.CYAN}Enter update interval in seconds (default: 1): {Style.RESET_ALL}")
            if not interval.isdigit() or int(interval) < 1:
                interval = 1
            else:
                interval = int(interval)
            
            monitor_system_resources(duration, interval)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "3":
            list_processes()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "4":
            kill_process()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "5":
            network_connections()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "6":
            break
        
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
