import socket
import ipaddress
import subprocess
import platform
from colorama import Fore, init, Style
import pyfiglet
import argparse
import sys
import time

#TODO
#1. Add a function to check if the target is online
#2. Add a function to check if the target is vulnerable to a specific exploit
#3. Add all common ports



#      _   __________________  _____   ________
#     / | / / ____/_  __/ __ \/  _/ | / / ____/
#    /  |/ / __/   / / / /_/ // //  |/ / / __  
#   / /|  / /___  / / / ____// // /|  / /_/ /  
#  /_/ |_/_____/ /_/ /_/   /___/_/ |_/\____/   
#
#   Author: Beast, Hades

init(autoreset=True)
ascii_art = pyfiglet.figlet_format("NETPING", font="slant")
print(Fore.LIGHTGREEN_EX + ascii_art)

parser = argparse.ArgumentParser(description="Network ping scanner tool.")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of pings per device (default value is 1)")
parser.add_argument("-o", "--output", type=str, help="Output file for results")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output")
parser.add_argument("-p", "--portscan", action="store_true", help="Scans common ports on devices")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

args = parser.parse_args()

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(Fore.RED + "Could not determine the local IP address:", e)
        return None

local_ip = get_local_ip()
if local_ip:
    print(Fore.GREEN + f"Your local IP address: {local_ip}")
    network = ipaddress.ip_network(local_ip + '/24', strict=False)  
else:
    print(Fore.RED + "Failed to retrieve the local IP address.")
    sys.exit()

ping_count = args.count
param = '-n' if platform.system().lower() == 'windows' else '-c'
output_file = None
results = []
common_ports = [22,80,443,8080]

try:
    if args.output:
        output_file = open(args.output, "w")

    for ip in network.hosts():
        ip_str = str(ip)
        result = subprocess.run(['ping', param, str(ping_count), ip_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if "Destination host unreachable" in result.stdout:
            status = f"{ip_str} is unreachable"
            print(Fore.RED + f"Scanning Network: {status}")
        elif result.returncode == 0:
            status = f"{ip_str} is reachable"
            print(Fore.GREEN + f"Scanning Network: {status}")
            
            if args.portscan:
                port_results = []
                for port in common_ports:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(1)
                            result = sock.connect_ex((ip_str, port))
                            if result == 0:
                                port_status = f"Port {port} is open on {ip_str}"
                                print(Fore.GREEN + f"Port Scan: {port_status}")
                            else:
                                port_status = f"Port {port} is closed on {ip_str}"
                                print(Fore.RED + f"Port Scan: {port_status}")
                            port_results.append(port_status)
                    except Exception as e:
                        port_status = f"Port {port} scan failed on {ip_str}: {e}"
                        print(Fore.RED + f"Port Scan: {port_status}")
                        port_results.append(port_status)
                    results.extend(port_results)
        else:
            status = f"{ip_str} is unreachable (Error in ping response)"
            print(Fore.YELLOW + f"Scanning Network: {status}")

        results.append(status)

except KeyboardInterrupt:
    print(Fore.YELLOW + "\nScan interrupted by user!")
    

finally:
    if output_file:
        output_file.write("\n".join(results) + "\n")
        output_file.close()
        print(Fore.CYAN + f"\nResults saved to {args.output}")
    elif not args.output and results:
        print(Fore.YELLOW + "\nResults:\n" + "\n".join(results))
        while True:
            save = input(Fore.CYAN + "\nWould you like to save the results to a file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input(Fore.CYAN + "Enter filename to save results: ").strip()  
                print(Fore.YELLOW + f"Saving results to {filename}...")
                for _ in range(3):
                    print(Fore.CYAN + ".", end="", flush=True)
                    time.sleep(1.2)
                print()
                with open(filename, "w") as f:
                    f.write("\n".join(results) + "\n")
                break
            elif save == 'n':
                print(Fore.CYAN + "Results not saved.")
                break
            else:
                print(Fore.RED + "Please type only 'y' or 'n'.")
    print(Fore.GREEN + "Exiting program...")
    time.sleep(1)
