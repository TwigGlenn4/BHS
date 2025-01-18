import csv
import socket

csv_file = ".github/servers.csv"
readme_file = "README.md"

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

def update_readme(readme_file, servers):
    with open(readme_file, "r") as file:
        content = file.read()

    status_lines = [
        "| SERVER NAME     | SERVER ADDRESS/IP        | SERVER PORT | WORLD SIZE | RULES     | STATUS      |",
        "|-----------------|--------------------------|-------------|------------|-----------|-------------|"
    ]

    for server in servers:
        status = "🟢 Open" if check_port(server["SERVER ADDRESS/IP"], int(server["SERVER PORT"])) else "🔴 Closed"
        status_lines.append(
            f"| {server['SERVER NAME']} | {server['SERVER ADDRESS/IP']} | {server['SERVER PORT']} | {server['WORLD SIZE']} | {server['RULES']} | {status} |"
        )

    new_content = content.replace("{{SERVER_STATUS}}", "\n".join(status_lines))

    with open(readme_file, "w") as file:
        file.write(new_content)

if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_readme(readme_file, servers)
    print("Server statuses updated.")
