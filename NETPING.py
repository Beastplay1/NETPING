import socket
import ipaddress
import subprocess
import platform
from colorama import Fore, Style, init
import pyfiglet
from tqdm import tqdm
import time

#      _   __________________  _____   ________
#     / | / / ____/_  __/ __ \/  _/ | / / ____/
#    /  |/ / __/   / / / /_/ // //  |/ / / __  
#   / /|  / /___  / / / ____// // /|  / /_/ /  
#  /_/ |_/_____/ /_/ /_/   /___/_/ |_/\____/   
#
#   Author: Beast, Hades

# Initialize colorama
init(autoreset=True)

# ASCII art header
ascii_art = pyfiglet.figlet_format("NETPING", font="slant")
print(Fore.CYAN + ascii_art)

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(Fore.RED + "Could not determine the local IP address:", e)
        return None
    
local_ip = get_local_ip()
if local_ip:
    print(Fore.GREEN + f"Your local IP address: {local_ip}")
else:
    print(Fore.RED + "Failed to retrieve the local IP address.")
    
network = ipaddress.ip_network(local_ip + '/24', strict=False)

try:
    ping_count = int(input("Enter the number of pings to send to each device: "))
except ValueError:
    print(Fore.YELLOW + "Invalid input. Please enter a number.")
    ping_count = 1

print(Fore.YELLOW + "\nPinging devices...\n")

param = '-n' if platform.system().lower() == 'windows' else '-c'

for ip in network.hosts():
    ip_str = str(ip)
    result = subprocess.run(['ping', param, str(ping_count), ip_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if "Destination host unreachable" in result.stdout:
        print(Fore.RED + f"{ip_str} is unreachable (Destination host unreachable)")
    elif result.returncode == 0:
        print(Fore.GREEN + f"{ip_str} is reachable")
    else:
        print(Fore.YELLOW + f"{ip_str} is unreachable (Error in ping response)")
