import subprocess
import os
from datetime import datetime

def run_cmd(title, command):
    print(f"\n=== {title} ===")
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(result.stdout)
        return f"\n=== {title} ===\n{result.stdout}\n"
    except Exception as e:
        return f"\n=== {title} ===\nError: {str(e)}\n"

def main():
    log = []
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"winnet_report_{now}.txt"

    commands = [
        ("Netstat (All)", "netstat -ano"),
        ("Routing Table", "route print"),
        ("ARP Table", "arp -a"),
        ("DNS Resolver Cache", "ipconfig /displaydns"),
        ("IP Configuration", "ipconfig /all"),
        ("Ping Google", "ping 8.8.8.8"),
        ("Trace Route to Google", "tracert google.com"),
        ("PathPing to Google", "pathping -n 8.8.8.8"),
        ("Firewall Rules", "netsh advfirewall firewall show rule name=all"),
        ("Wireless Interfaces", "netsh wlan show interfaces"),
        ("Active Sessions", "net session"),
        ("Shared Resources", "net share"),
        ("ARP Cache", "arp -a"),
        ("Running Processes", "tasklist"),
        ("Event Log (System)", 'wevtutil qe System /c:10 /f:text'),
    ]

    print("Starting network forensic scan...")

    for title, cmd in commands:
        output = run_cmd(title, cmd)
        log.append(output)

    with open(filename, "w", encoding='utf-8') as f:
        f.writelines(log)

    print(f"\nReport saved to: {filename}")

if __name__ == "__main__":
    main()
