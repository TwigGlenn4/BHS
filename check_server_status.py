import socket
import os

readme_file = "README.md"

def check_port(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((hostname, port))
        return result == 0

def update_readme(readme_file):
    with open(readme_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "offline/online" in line:
            parts = line.split()
            hostname = parts[1]
            port = int(parts[2])
            status = "🟢 Online" if check_port(hostname, port) else "🔴 Offline"
            new_lines.append(f"- {hostname} {port} {status}\n")
        else:
            new_lines.append(line)

    with open(readme_file, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    update_readme(readme_file)
    print("Server statuses updated.")
