import csv
import socket
import os
from geopy.geocoders import Nominatim

csv_file = ".github/servers.csv"
wiki_file = "wiki/Servers.md"

geolocator = Nominatim(user_agent="server-check")

def check_udp_port(hostname, port):
    """Check if a specific UDP port is open on a given hostname."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b'', (hostname, port))
        sock.recvfrom(1024)  # Try to receive data
        sock.close()
        return True
    except Exception as e:
        print(f"Error with {hostname} on UDP port {port}: {e}")
        return False

def get_country_and_flag(ip_or_hostname):
    """Get the country and flag emoji for a given IP address or hostname."""
    try:
        ip = socket.gethostbyname(ip_or_hostname)
        location = geolocator.geocode(ip)
        if location:
            country = location.address.split(",")[-1].strip()
            country_code = location.raw["address"]["country_code"].upper()
            flag_emoji = chr(ord('🇦') + (ord(country_code[0]) - ord('A'))) + chr(ord('🇦') + (ord(country_code[1]) - ord('A')))
            return country_code, flag_emoji
    except Exception as e:
        print(f"Error resolving {ip_or_hostname}: {e}")
        return "Unknown", ""

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
        is_online = check_udp_port(server["ADDRESS/IP"], int(server["PORT"]))
        status = "🟢 Online" if is_online else "🔴 Offline"
        country_code, flag_emoji = get_country_and_flag(server["ADDRESS/IP"])
        status_lines.append(
            f"<tr><td>{server['NAME']}</td><td>{server['ADDRESS/IP']}</td><td>{server['PORT']}</td><td>{server['SIZE']}</td><td>{server['RULES']}</td><td>{status}</td><td>{flag_emoji} {country_code}</td></tr>"
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
      <th>COUNTRY</th>
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
