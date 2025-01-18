import socket
import os

hostname = "theblackswan.devon.social
port = 5151
status_file = "Server_Status.md"

def check_port(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((hostname, port))
        return result == 0

def get_current_status(status_file):
    if not os.path.exists(status_file):
        return None
    with open(status_file, "r") as f:
        content = f.read().strip()
        return "🟢 Online" if "🟢 Online" in content else "🔴 Offline"

def update_status_file(status_file, status_indicator):
    with open(status_file, "w") as f:
        f.write(f"## Server Status\n\n- {status_indicator}\n")

if __name__ == "__main__":
    current_status = get_current_status(status_file)
    new_status = "🟢 Online" if check_port(hostname, port) else "🔴 Offline"

    if current_status != new_status:
        update_status_file(status_file, new_status)
        print(f"Status changed to {new_status}. File updated.")
    else:
        print("Status unchanged. No update needed.")
