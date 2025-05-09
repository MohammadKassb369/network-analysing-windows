import subprocess
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Directory to save reports
os.makedirs("logs", exist_ok=True)

# Function to run a command and return its output
def run_cmd(title, command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return f"\n=== {title} ===\n{result.stdout}\n"
    except Exception as e:
        return f"\n=== {title} ===\nError: {str(e)}\n"

# Save command output to file
def save_output_to_file(title, command):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{title.replace(' ', '_')}_{now}.txt"
    output = run_cmd(title, command)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
    messagebox.showinfo("Command Executed", f"{title}\n\nOutput saved to:\n{filename}")

# Switch-like dispatcher (requires Python 3.10+)
def dispatch_command(option):
    match option:
        case "Netstat":
            save_output_to_file("Netstat", "netstat -ano")
        case "Routing Table":
            save_output_to_file("Routing Table", "route print")
        case "ARP Table":
            save_output_to_file("ARP Table", "arp -a")
        case "DNS Cache":
            save_output_to_file("DNS Cache", "ipconfig /displaydns")
        case "IP Config":
            save_output_to_file("IP Configuration", "ipconfig /all")
        case "Ping Google":
            save_output_to_file("Ping Google", "ping 8.8.8.8")
        case "Traceroute":
            save_output_to_file("Traceroute", "tracert google.com")
        case "PathPing":
            save_output_to_file("PathPing", "pathping -n 8.8.8.8")
        case "Firewall Rules":
            save_output_to_file("Firewall Rules", "netsh advfirewall firewall show rule name=all")
        case "Wireless Interfaces":
            save_output_to_file("Wireless Interfaces", "netsh wlan show interfaces")
        case "Active Sessions":
            save_output_to_file("Active Sessions", "net session")
        case "Shared Resources":
            save_output_to_file("Shared Resources", "net share")
        case "Tasklist":
            save_output_to_file("Running Processes", "tasklist")
        case "Event Log":
            save_output_to_file("Event Log", 'wevtutil qe System /c:10 /f:text')
        case _:
            messagebox.showwarning("Unknown", "Unknown command selected.")

# Build the GUI
def build_gui():
    root = tk.Tk()
    root.title("Network Forensic Tool - WinNet GUI")
    root.geometry("400x600")

    commands = [
        "Netstat", "Routing Table", "ARP Table", "DNS Cache", "IP Config",
        "Ping Google", "Traceroute", "PathPing", "Firewall Rules",
        "Wireless Interfaces", "Active Sessions", "Shared Resources",
        "Tasklist", "Event Log"
    ]

    tk.Label(root, text="Choose a command to run:", font=("Arial", 14)).pack(pady=10)

    for cmd in commands:
        tk.Button(root, text=cmd, width=30, command=lambda c=cmd: dispatch_command(c)).pack(pady=5)

    tk.Button(root, text="Exit", width=30, command=root.quit, bg="red", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
