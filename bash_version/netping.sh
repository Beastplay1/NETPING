#!/bin/bash

GREEN='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
RESET='\033[0m'

echo -e "${GREEN}"
echo "   _   __________________  _____   ________ "
echo "  / | / / ____/_  __/ __ \/  _/ | / / ____/ "
echo " /  |/ / __/   / / / /_/ // //  |/ / / __   "
echo "/ /|  / /___  / / / ____// // /|  / /_/ /   "
echo "/_/ |_/_____/ /_/ /_/   /___/_/ |_/\____/   "
echo
echo "   Network Ping Scanner Tool by Beast, Hades"
echo -e "${RESET}"

if [[ "$#" -eq 0 ]]; then
    echo -e "${CYAN}Usage: $0 [-c count] [-o output_file] [-v] [-p]${RESET}"
    echo "Options:"
    echo "  -c, --count       Number of pings per device (default: 1)"
    echo "  -o, --output      Output file to save results"
    echo "  -v, --verbose     Enable detailed output"
    echo "  -p, --portscan    Scan common ports on devices"
    echo "  -h, --help        Show this help message"
    exit 0
fi

ping_count=1
output_file=""
verbose=0
portscan=0
common_ports=(22 80 443 8080)

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--count) ping_count="$2"; shift ;;
        -o|--output) output_file="$2"; shift ;;
        -v|--verbose) verbose=1 ;;
        -p|--portscan) portscan=1 ;;
        -h|--help)
            echo -e "${CYAN}Usage: $0 [-c count] [-o output_file] [-v] [-p]${RESET}"
            echo "Options:"
            echo "  -c, --count       Number of pings per device (default: 1)"
            echo "  -o, --output      Output file to save results"
            echo "  -v, --verbose     Enable detailed output"
            echo "  -p, --portscan    Scan common ports on devices"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *) echo -e "${RED}Unknown option: $1${RESET}"; exit 1 ;;
    esac
    shift
done

local_ip=$(hostname -I | awk '{print $1}')
if [[ -z "$local_ip" ]]; then
    echo -e "${RED}Could not determine the local IP address.${RESET}"
    exit 1
fi
echo -e "${GREEN}Your local IP address: ${local_ip}${RESET}"
network="${local_ip%.*}.0/24"

function scan_host {
    local ip="$1"
    if ping -c "$ping_count" -W 1 "$ip" > /dev/null 2>&1; then
        echo -e "${GREEN}Scanning Network: ${ip} is reachable${RESET}"
        results+=("$ip is reachable")

        if [[ "$portscan" -eq 1 ]]; then
            for port in "${common_ports[@]}"; do
                (echo >/dev/tcp/"$ip"/"$port") &>/dev/null
                if [[ $? -eq 0 ]]; then
                    echo -e "${GREEN}Port Scan: Port $port is open on $ip${RESET}"
                    results+=("Port $port is open on $ip")
                else
                    echo -e "${RED}Port Scan: Port $port is closed on $ip${RESET}"
                    results+=("Port $port is closed on $ip")
                fi
            done
        fi
    else
        echo -e "${YELLOW}Scanning Network: ${ip} is unreachable${RESET}"
        results+=("$ip is unreachable")
    fi
}

results=()
for ip in $(nmap -n -sn "$network" | grep "Nmap scan report" | awk '{print $5}'); do
    scan_host "$ip"
done

if [[ -n "$output_file" ]]; then
    echo -e "${CYAN}Saving results to $output_file...${RESET}"
    printf "%s\n" "${results[@]}" > "$output_file"
elif [[ ${#results[@]} -gt 0 ]]; then
    echo -e "${YELLOW}\nResults:\n${RESET}"
    printf "%s\n" "${results[@]}"

    while true; do
        read -rp $'\e[36m\nWould you like to save the results to a file? (y/n): \e[0m' save
        case $save in
            [Yy]* )
                read -rp $'\e[36mEnter filename to save results: \e[0m' filename
                echo -e "${YELLOW}Saving results to $filename...${RESET}"
                printf "%s\n" "${results[@]}" > "$filename"
                break
                ;;
            [Nn]* ) echo -e "${CYAN}Results not saved.${RESET}"; break ;;
            * ) echo -e "${RED}Please type only 'y' or 'n'.${RESET}" ;;
        esac
    done
fi

echo -e "${GREEN}Exiting program...${RESET}"
