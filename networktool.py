import subprocess
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Dictionary of commands
COMMANDS = {
    "Netstat (All)": "netstat -ano",
    "Routing Table": "route print",
    "ARP Table": "arp -a",
    "DNS Resolver Cache": "ipconfig /displaydns",
    "IP Configuration": "ipconfig /all",
    "Ping Google": "ping 8.8.8.8",
    "Trace Route to Google": "tracert google.com",
    "PathPing to Google": "pathping -n 8.8.8.8",
    "Firewall Rules": "netsh advfirewall firewall show rule name=all",
    "Wireless Interfaces": "netsh wlan show interfaces",
    "Active Sessions": "net session",
    "Shared Resources": "net share",
    "Running Processes": "tasklist",
    "Event Log (System)": 'wevtutil qe System /c:10 /f:text',
}

# Run a system command and return its output
def run_cmd(title, command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return f"\n=== {title} ===\n{result.stdout}\n"
    except Exception as e:
        return f"\n=== {title} ===\nError: {str(e)}\n"

# Run and save a single command
def save_single(title):
    output = run_cmd(title, COMMANDS[title])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{title.replace(' ', '_')}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
    messagebox.showinfo("Completed", f"{title} completed.\nSaved to:\n{filename}")

# Run all commands and save to one report
def save_all():
    log = []
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/winnet_report_{timestamp}.txt"
    for title, cmd in COMMANDS.items():
        log.append(run_cmd(title, cmd))
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(log)
    messagebox.showinfo("Scan Complete", f"Full report saved to:\n{filename}")

# Show Wi-Fi passwords of saved profiles
def show_wifi_passwords():
    output = run_cmd("WiFi Profiles", "netsh wlan show profiles")
    profiles = [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]
    result = []
    for profile in profiles:
        cmd = f'netsh wlan show profile name="{profile}" key=clear'
        result.append(run_cmd(f"WiFi Profile: {profile}", cmd))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/WiFi_Passwords_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(result)
    messagebox.showinfo("Wi-Fi Passwords", f"Saved Wi-Fi password report:\n{filename}")

# Build GUI
def build_gui():
    root = tk.Tk()
    root.title("WinNet Network Forensics Tool")
    root.geometry("460x750")

    tk.Label(root, text="Select Command to Run", font=("Arial", 14)).pack(pady=10)

    for title in COMMANDS.keys():
        tk.Button(root, text=title, width=50, command=lambda t=title: save_single(t)).pack(pady=2)

    tk.Button(root, text="Run All & Save Report", bg="green", fg="white", width=50, command=save_all).pack(pady=10)
    tk.Button(root, text="Show Wi-Fi Passwords", bg="blue", fg="white", width=50, command=show_wifi_passwords).pack(pady=5)
    tk.Button(root, text="Exit", bg="red", fg="white", width=50, command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
