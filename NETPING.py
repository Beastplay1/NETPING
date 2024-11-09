import socket
import ipaddress
import subprocess
import platform
from colorama import Fore, Style, init
import pyfiglet
from tqdm import tqdm
import argparse

# Initialize colorama
init(autoreset=True)

# ASCII art header
ascii_art = pyfiglet.figlet_format("NETPING", font="slant")
print(Fore.CYAN + ascii_art)

# Set up argparse for count, output file, and verbose mode
parser = argparse.ArgumentParser(description="A network ping scanner tool for checking device reachability within a subnet.")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of pings to send to each device (default: 1)")
parser.add_argument("-o", "--output", type=str, help="Specify an output file to save the results")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode for detailed output")
args = parser.parse_args()

def get_local_ip():
    """Determine the local IP address of the current machine."""
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

# Determine network based on the local IP
network = ipaddress.ip_network(local_ip + '/24', strict=False)
ping_count = args.count

print(Fore.YELLOW + "\nPinging devices...\n")

# Choose the appropriate ping parameter based on the OS
param = '-n' if platform.system().lower() == 'windows' else '-c'

# Prepare for storing output results
output_file = None
results = []

try:
    # Open output file if specified
    if args.output:
        output_file = open(args.output, "w")

    # Ping each device in the subnet
    for ip in tqdm(network.hosts(), desc="Scanning Network"):
        ip_str = str(ip)
        result = subprocess.run(['ping', param, str(ping_count), ip_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if "Destination host unreachable" in result.stdout:
            status = f"{ip_str} is unreachable (Destination host unreachable)"
            print(Fore.RED + status) if args.verbose else None
        elif result.returncode == 0:
            status = f"{ip_str} is reachable"
            print(Fore.GREEN + status) if args.verbose else None
        else:
            status = f"{ip_str} is unreachable (Error in ping response)"
            print(Fore.YELLOW + status) if args.verbose else None

        # Append result to the list
        results.append(status)

except KeyboardInterrupt:
    print(Fore.YELLOW + "\nScan interrupted by user. Saving results...")

finally:
    # Write results to output file if specified
    if output_file:
        output_file.write("\n".join(results) + "\n")
        output_file.close()
        print(Fore.CYAN + f"\nResults saved to {args.output}")
    elif not args.output and results:
        print(Fore.YELLOW + "\nResults:\n" + "\n".join(results))
    print(Fore.GREEN + "Exiting program.")
