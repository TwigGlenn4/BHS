import csv
import socket
import os
import datetime  # Directly imported datetime

csv_file = ".github/servers.csv"
wiki_file = "wiki/Servers.md"

def check_udp_port(hostname, port):
    """Check if a specific UDP port is open on a given hostname."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b'', (hostname, port))
        start_time = datetime.datetime.now()
        
        sock.recvfrom(1024)  # Try to receive data
        ping_time = (datetime.datetime.now() - start_time).total_seconds() * 1000  # Convert to milliseconds
        sock.close()
        return True, ping_time
    except socket.timeout:
        sock.close()
        return True, None  # If it's a timeout, it might still be open
    except Exception as e:
        print(f"Error with {hostname} on UDP port {port}: {e}")
        return False, None  # Other exceptions mean it's probably closed

def read_servers(csv_file):
    """Read server details from a CSV file and return them as a list of dictionaries."""
    servers = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            servers.append(row)
    return servers

def generate_server_status(servers):
    """Generate the server status table as a string."""
    status_lines = []

    for server in servers:
        is_online, ping_time = check_udp_port(server["ADDRESS/IP"], int(server["PORT"]))
        status = "🟢 Online" if is_online else "🔴 Offline"
        ping_display = f"{ping_time:.2f} ms" if ping_time else "N/A"
        status_lines.append(
            f"<tr><td>{server['NAME']}</td><td>{server['ADDRESS/IP']}</td><td>{server['PORT']}</td><td>{server['SIZE']}</td><td>{server['RULES']}</td><td>{status}</td><td>{ping_display}</td></tr>"
        )

    return "".join(status_lines)  # Combine without joining using newlines

def read_previous_status(wiki_file):
    """Read the previous server status from the wiki file."""
    if not os.path.exists(wiki_file):
        return ""
    
    with open(wiki_file, "r") as file:
        content = file.read()
        return content

def update_wiki(servers, wiki_file):
    """Update the wiki page with the current server statuses."""
    new_status = generate_server_status(servers)
    previous_status = read_previous_status(wiki_file)

    if new_status != previous_status:
        os.makedirs(os.path.dirname(wiki_file), exist_ok=True)  # Ensure directory exists
        content = f"""# Server List

<table>
  <thead>
    <tr>
      <th>NAME</th>
      <th>ADDRESS/IP</th>
      <th>PORT</th>
      <th>SIZE</th>
      <th>RULES</th>
      <th>STATUS</th>
      <th>PING</th>
    </tr>
  </thead>
  <tbody>
    {new_status}
  </tbody>
</table>
"""
        with open(wiki_file, "w") as file:
            file.write(content)
        print("Server statuses updated in wiki.")
    else:
        print("No changes in server statuses. Wiki not updated.")

if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_wiki(servers, wiki_file)
    print("Server statuses updated.")
