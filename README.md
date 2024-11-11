# NETPING

**NetPing** is a simple Python-based network ping tool designed to help users quickly check the reachability of devices within their local network. It uses ICMP echo requests (ping) to determine whether devices are responsive. The tool provides a colorful, user-friendly output, with various color codes indicating the status of each device (reachable, unreachable, or errors).

## Features:
- Automatically detects your local IP address.
- Pings devices within the same subnet (based on local IP address).
- Customizable ping count for each device.
- Colorful terminal output using `colorama` for easy readability.
- Built-in ASCII art header for a visually appealing start.

## Requirements:
- Python 3.x
- `colorama`, `pyfiglet`, and `tqdm` libraries (can be installed via `pip`).

## Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/beastplay1/NETPING.git
2. Open the folder:
   ```bash
   cd NETPING/
3. Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. for python version:
   ```bash
   cd python_version/
   ```
   for bash version:
   ```bash
   cd bash_version/
   ```
## Usage:
Run the script:
   ```bash
   python3 netping.py
   ```
or:
   ```bash
   chmod +x netping.sh
   ./netping.sh
   ```

##Example:
```
python3 .\NETPING.py
    _   __________________  _____   ________
   / | / / ____/_  __/ __ \/  _/ | / / ____/
  /  |/ / __/   / / / /_/ // //  |/ / / __
 / /|  / /___  / / / ____// // /|  / /_/ /
/_/ |_/_____/ /_/ /_/   /___/_/ |_/\____/


usage: NETPING.py [-h] [-c COUNT] [-o OUTPUT] [-v] [-p]

Network ping scanner tool.

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of pings per device (default value is 1)
  -o OUTPUT, --output OUTPUT
                        Output file for results
  -v, --verbose         Enable detailed output
  -p, --portscan        Scans common ports on devices
```
