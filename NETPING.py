import socket
import ipaddress
import subprocess
import platform
from colorama import Fore, init
import pyfiglet
from tqdm import tqdm
import argparse
import sys

# ASCII art author block
#      _   __________________  _____   ________
#     / | / / ____/_  __/ __ \/  _/ | / / ____/
#    /  |/ / __/   / / / /_/ // //  |/ / / __  
#   / /|  / /___  / / / ____// // /|  / /_/ /  
#  /_/ |_/_____/ /_/ /_/   /___/_/ |_/\____/   
#
#   Author: Beast, Hades

init(autoreset=True)
ascii_art = pyfiglet.figlet_format("NETPING", font="slant")
print(Fore.CYAN + ascii_art)

parser = argparse.ArgumentParser(description="Network ping scanner and port scanner tool.")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of pings per device")
parser.add_argument("-o", "--output", type=str, help="Output file for results")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output")
parser.add_argument("-p", "--portscan", action="store_true", help="Enable port scanning automatically without prompt (Scans only common ports)")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

args = parser.parse_args()

popular_ports = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 161, 389, 443, 445, 465, 
    587, 993, 995, 1080, 1433, 1521, 1723, 3306, 3389, 5432, 5900, 8080, 8443
]

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(Fore.RED + "Could not determine the local IP address:", e)
        return None

def scan_ports(ip):
    open_ports = []
    for port in popular_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

local_ip = get_local_ip()
if local_ip:
    print(Fore.GREEN + f"Your local IP address: {local_ip}")
else:
    print(Fore.RED + "Failed to retrieve the local IP address.")

network = ipaddress.ip_network(local_ip + '/24', strict=False)
ping_count = args.count
param = '-n' if platform.system().lower() == 'windows' else '-c'
output_file = None
reachable_ips = []

try:
    if args.output:
        output_file = open(args.output, "w")

    for ip in tqdm(network.hosts(), desc="Scanning Network"):
        ip_str = str(ip)
        result = subprocess.run(['ping', param, str(ping_count), ip_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if "Destination host unreachable" in result.stdout:
            status = f"{ip_str} is unreachable (Destination host unreachable)"
            if args.verbose:
                print(Fore.RED + status)
        elif result.returncode == 0:
            status = f"{ip_str} is reachable"
            reachable_ips.append(ip_str)
            if args.verbose:
                print(Fore.GREEN + status)
        else:
            status = f"{ip_str} is unreachable (Error in ping response)"
            if args.verbose:
                print(Fore.YELLOW + status)

except KeyboardInterrupt:
    print(Fore.YELLOW + "\nScan interrupted by user.")
    if args.portscan:
        print(Fore.CYAN + "\nStarting port scan on reachable devices...\n")
    else:
        user_choice = input("Do you want to perform a port scan on reachable devices? (y/n): ").strip().lower()
        if user_choice != 'y':
            print(Fore.GREEN + "Exiting program.")
            sys.exit()

finally:
    full_results = []
    if args.portscan or (reachable_ips and user_choice == 'y'):
        for ip in reachable_ips:
            open_ports = scan_ports(ip)
            if open_ports:
                port_info = f"{ip} | Open Ports: {', '.join(map(str, open_ports))}"
                print(Fore.CYAN + port_info)
                full_results.append(port_info)
            else:
                port_info = f"{ip} has no open popular ports"
                print(Fore.YELLOW + port_info)
                full_results.append(port_info)

    if not args.output:
        save_choice = input("Do you want to save the results to a file? (y/n): ").strip().lower()
        if save_choice == 'y':
            output_filename = input("Enter the filename to save the results: ").strip()
            with open(output_filename, "w") as f:
                f.write("\n".join(full_results) + "\n")
            print(Fore.CYAN + f"\nResults saved to {output_filename}")
        elif full_results:
            print(Fore.YELLOW + "\nResults:\n" + "\n".join(full_results))
    elif args.output and full_results:
        output_file.write("\n".join(full_results) + "\n")
        output_file.close()
        print(Fore.CYAN + f"\nResults saved to {args.output}")
    
    print(Fore.GREEN + "Exiting program.")
