# NETPING

**NETPING** is a miscellaneous multi-platform network tool available in both Python and Bash versions, designed for quick and efficient network diagnostics. Use NETPING to check device reachability and scan for open services across your network with ease. This tool is ideal for users who need to identify live hosts and determine the availability of specific services on common ports.

## Features:
- Automatically detects your local IP address.
- Pings devices within the same subnet (based on local IP address).
- Customizable ping count for each device.
- Colorful terminal output using `colorama` for easy readability.
- Scan common ports (e.g., 22, 80, 443, 8080) on reachable devices to check if services are open. (Support for scanning all common ports is planned in future updates.)
- Enable detailed output for easier debugging and enhanced scan insights.
- Optionally save scan results to a specified output file or decide to save after the scan.

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

## Example:
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
