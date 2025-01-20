import csv
import socket
import os
import datetime
from geopy.geocoders import Nominatim

csv_file = ".github/servers.csv"
wiki_file = "wiki/Servers.md"
log_file = ".github/uptime_log.csv"

geolocator = Nominatim(user_agent="server-status-checker")

def check_udp_port(hostname, port):
    """Check if a specific UDP port is open and returns any response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(b'ping', (hostname, port))
        data, _ = sock.recvfrom(1024)
        sock.close()
        if data:
            return True
    except Exception as e:
        print(f"Error with {hostname} on UDP port {port}: {e}")
        return False

def read_servers(file_path):
    """Read server details from a CSV file and return them as a list of dictionaries."""
    with open(file_path, "r") as file:
        return list(csv.DictReader(file))

def log_status(hostname, status):
    """Log the server status to a CSV file."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(log_file, "a", newline='') as file:
        csv.writer(file).writerow([timestamp, hostname, status])

def calculate_uptime(hostname):
    """Calculate the uptime percentage for a server."""
    if not os.path.exists(log_file):
        return 0

    total_checks, online_checks = 0, 0
    with open(log_file, "r") as file:
        for row in csv.reader(file):
            if row[1] == hostname:
                total_checks += 1
                if row[2] == "online":
                    online_checks += 1

    return (online_checks / total_checks) * 100 if total_checks else 0

def get_country_and_flag(ip_or_hostname):
    """Get the country and flag emoji for a given IP/hostname."""
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

def generate_server_status(servers):
    """Generate the server status table as a string."""
    server_statuses = []

    for server in servers:
        is_online = check_udp_port(server["ADDRESS/IP"], int(server["PORT"]))
        status = "online" if is_online else "offline"
        display_status = "🟢 Online" if is_online else "🔴 Offline"
        country_code, flag_emoji = get_country_and_flag(server["ADDRESS/IP"])
        uptime = calculate_uptime(server["ADDRESS/IP"])

        server_statuses.append({
            'NAME': server['NAME'],
            'ADDRESS/IP': server['ADDRESS/IP'],
            'PORT': server['PORT'],
            'SIZE': server['SIZE'],
            'RULES': server['RULES'],
            'STATUS': display_status,
            'COUNTRY': f"{flag_emoji} {country_code}",
            'UPTIME': uptime
        })
        log_status(server["ADDRESS/IP"], status)

    sorted_statuses = sorted(server_statuses, key=lambda x: x['UPTIME'], reverse=True)
    return "".join(
        f"<tr><td>{server['NAME']}</td><td>{server['ADDRESS/IP']}</td><td>{server['PORT']}</td>"
        f"<td>{server['SIZE']}</td><td>{server['RULES']}</td><td>{server['STATUS']}</td>"
        f"<td>{server['COUNTRY']}</td><td>{server['UPTIME']:.2f}%</td></tr>"
        for server in sorted_statuses
    )

def read_previous_status(wiki_file):
    """Read the previous server status from the wiki file."""
    if not os.path.exists(wiki_file):
        return ""
    with open(wiki_file, "r") as file:
        return file.read()

def update_wiki(servers, wiki_file):
    """Update the wiki page with current server statuses."""
    new_status = generate_server_status(servers)
    previous_status = read_previous_status(wiki_file)

    if new_status != previous_status:
        os.makedirs(os.path.dirname(wiki_file), exist_ok=True)
        content = f"""# Server List
<table>
    <thead>
        <tr><th>NAME</th><th>ADDRESS/IP</th><th>PORT</th><th>SIZE</th><th>RULES</th><th>STATUS</th><th>COUNTRY</th><th>UPTIME</th></tr>
    </thead>
    <tbody>{new_status}</tbody>
</table>"""
        with open(wiki_file, "w") as file:
            file.write(content)
        print("Server statuses updated in wiki.")
    else:
        print("No changes in server statuses. Wiki not updated.")

# Main Execution
if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_wiki(servers, wiki_file)
    print("Server statuses updated.")
