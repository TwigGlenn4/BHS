import csv
import socket
import os

csv_file = ".github/servers.csv"
wiki_file = "wiki/Servers.md"

def check_port(hostname, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex((hostname, port))
            return result == 0
    except socket.gaierror as e:
        print(f"Error connecting to {hostname} on port {port}: {e}")
        return False

def read_servers(csv_file):
    servers = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            servers.append(row)
    return servers

def generate_server_status(servers):
    status_lines = [
        "| SERVER NAME     | SERVER ADDRESS/IP        | SERVER PORT | WORLD SIZE | RULES     | STATUS      |",
        "|-----------------|--------------------------|-------------|------------|-----------|-------------|"
    ]

    for server in servers:
        status = "🟢 Open" if check_port(server["SERVER ADDRESS/IP"], int(server["SERVER PORT"])) else "🔴 Closed"
        status_lines.append(
            f"| {server['SERVER NAME']} | {server['SERVER ADDRESS/IP']} | {server['SERVER PORT']} | {server['WORLD SIZE']} | {server['RULES']} | {status} |"
        )

    return "\n".join(status_lines)

def read_previous_status(wiki_file):
    if not os.path.exists(wiki_file):
        return ""
    
    with open(wiki_file, "r") as file:
        content = file.read()
        return content

def update_wiki(servers, wiki_file):
    new_status = generate_server_status(servers)
    previous_status = read_previous_status(wiki_file)

    if new_status != previous_status:
        with open(wiki_file, "w") as file:
            file.write(new_status)
        print("Server statuses updated in wiki.")
        # Commit and push changes here if needed
    else:
        print("No changes in server statuses. Wiki not updated.")

if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_wiki(servers, wiki_file)
