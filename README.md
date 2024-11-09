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

## Usage:
Run the script:
   ```bash
   python3 netping.py
   ```

