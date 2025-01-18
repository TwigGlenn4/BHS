import csv
import socket
import os

csv_file = "data/servers.csv"
readme_file = "README.md"

def check_port(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((hostname, port))
        return result == 0

def read_servers(csv_file):
    servers = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            servers.append(row)
    return servers

def update_readme(readme_file, servers):
    with open(readme_file, "r") as file:
        content = file.read()

    for server in servers:
        status = "🟢 Online" if check_port(server["SERVER ADDRESS/IP"], int(server["SERVER PORT"])) else "🔴 Offline"
        content = content.replace("Loading...", status, 1)

    with open(readme_file, "w") as file:
        file.write(content)

if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_readme(readme_file, servers)
    print("Server statuses updated.")
