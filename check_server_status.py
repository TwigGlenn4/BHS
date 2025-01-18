import socket
import os

index_file = "servers.txt"
readme_file = "README.md"

def check_port(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((hostname, port))
        return result == 0

def read_servers(index_file):
    servers = []
    with open(index_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                servers.append((parts[0], int(parts[1])))
    return servers

def update_readme(readme_file, server_statuses):
    with open(readme_file, "r") as f:
        content = f.read()
    
    status_lines = "\n".join([f"{server[0]} port {server[1]} {'🟢 Open' if status else '🔴 Closed'}" for server, status in server_statuses])
    new_content = content.replace("{{SERVER_STATUS}}", status_lines)

    with open(readme_file, "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    servers = read_servers(index_file)
    server_statuses = [(server, check_port(server[0], server[1])) for server in servers]
    update_readme(readme_file, server_statuses)
    print("Server statuses updated.")
