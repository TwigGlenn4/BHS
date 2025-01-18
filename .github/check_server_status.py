import csv
import socket
import os
import time
from datetime import datetime

csv_file = ".github/servers.csv"
wiki_file = "wiki/Servers.md"

def check_port(hostname, port):
    """Check if a specific port is open on a given hostname and return ping time if open."""
    try:
        with socket.create_connection((hostname, port), timeout=2) as conn:
            start_time = time.time()
            conn.send(b'')
            ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            return True, ping_time
    except Exception as e:
        print(f"Error connecting to {hostname} on port {port}: {e}")
        return False, None

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
        is_online, ping_time = check_port(server["SERVER ADDRESS/IP"], int(server["SERVER PORT"]))
        status = "🟢 Online" if is_online else "🔴 Offline"
        ping_display = f"{ping_time:.2f} ms" if ping_time else "N/A"
        status_lines.append(
            f"<tr>"
            f"<td>{server['SERVER NAME']}</td>"
            f"<td>{server['SERVER ADDRESS/IP']}</td>"
            f"<td>{server['SERVER PORT']}</td>"
            f"<td>{server['WORLD SIZE']}</td>"
            f"<td>{server['RULES']}</td>"
            f"<td>{status}</td>"
            f"<td>{ping_display}</td>"
            f"</tr>"
        )

    return "\n".join(status_lines)

def format_datetime():
    """Format the current datetime to a specific string format."""
    dt = datetime.utcnow()
    return dt.strftime("%A, the %dth day of %B %Y at %H:%M:%S")

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
    last_updated = format_datetime()

    if new_status != previous_status:
        content = f"""# Blockhead Servers

Welcome to the Blockhead Server List. Here you'll find the current status of our servers, last updated on:
<div id="last-updated"></div>

<button onclick="sortTable(0)">Sort by Name 🠕</button>
<button onclick="sortTable(1)">Sort by Status 🠕</button>
<button id="toggle-sort" onclick="toggleSortOrder()">Switch to Z-A</button>

<table id="servers-table">
  <thead>
    <tr>
      <th>SERVER NAME</th>
      <th>SERVER ADDRESS/IP</th>
      <th>SERVER PORT</th>
      <th>WORLD SIZE</th>
      <th>RULES</th>
      <th>STATUS</th>
      <th>PING TIME</th>
    </tr>
  </thead>
  <tbody>
    {new_status}
  </tbody>
</table>

<script>
  let sortOrder = 'asc';

  function sortTable(n) {{
    const table = document.getElementById("servers-table");
    let rows = Array.prototype.slice.call(table.tBodies[0].rows);

    rows.sort((a, b) => {{
      let x = a.cells[n].innerText.toLowerCase();
      let y = b.cells[n].innerText.toLowerCase();
      if (x < y) {{ return sortOrder==='asc' ? -1 : 1; }}
      if (x > y) {{ return sortOrder==='asc' ? 1 : -1; }}
      return 0;
    }});

    rows.forEach(row => table.tBodies[0].appendChild(row));
  }}

  function toggleSortOrder() {{
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    document.getElementById('toggle-sort').innerText = sortOrder === 'asc' ? 'Switch to Z-A' : 'Switch to A-Z';
  }}

  const lastUpdatedUTC = "{last_updated} UTC";
  const lastUpdatedDate = new Date(lastUpdatedUTC + ' UTC');
  document.getElementById('last-updated').innerText = lastUpdatedDate.toLocaleString();
</script>

<style>
  table {{
    width: 100%;
    border-collapse: collapse;
  }}
  th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }}
  th {{
    background-color: #f2f2f2;
  }}
  tr:nth-child(even) {{
    background-color: #f9f9f9;
  }}
  tr:hover {{
    background-color: #f1f1f1;
  }}
</style>"""
        with open(wiki_file, "w") as file:
            file.write(content)
        print("Server statuses updated in wiki.")
        # Commit and push changes here if needed
    else:
        print("No changes in server statuses. Wiki not updated.")

if __name__ == "__main__":
    servers = read_servers(csv_file)
    update_wiki(servers, wiki_file)
    print("Server statuses updated.")
