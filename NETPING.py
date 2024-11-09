import socket
import ipaddress
import subprocess
import platform
from colorama import Fore, init
import pyfiglet
import argparse
import sys

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

parser = argparse.ArgumentParser(description="Network ping scanner tool.")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of pings per device")
parser.add_argument("-o", "--output", type=str, help="Output file for results")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output")

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
else:
    print(Fore.RED + "Failed to retrieve the local IP address.")

network = ipaddress.ip_network(local_ip + '/24', strict=False)
ping_count = args.count
param = '-n' if platform.system().lower() == 'windows' else '-c'
output_file = None
results = []

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
        else:
            status = f"{ip_str} is unreachable (Error in ping response)"
            print(Fore.YELLOW + f"Scanning Network: {status}")

        results.append(status)

except KeyboardInterrupt:
    print(Fore.YELLOW + "\nScan interrupted by user. Saving results...")

finally:
    if output_file:
        output_file.write("\n".join(results) + "\n")
        output_file.close()
        print(Fore.CYAN + f"\nResults saved to {args.output}")
    elif not args.output and results:
        print(Fore.YELLOW + "\nResults:\n" + "\n".join(results))
    print(Fore.GREEN + "Exiting program.")
