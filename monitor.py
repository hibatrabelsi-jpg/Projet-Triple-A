import psutil
import platform
import socket
import datetime
import os

# Récupération des données CPU
cpu = psutil.cpu_percent(interval=1)
cpu_cores = psutil.cpu_count(logical=True)
cpu_freq = psutil.cpu_freq().current # en MHz

# Récupération des données RAM
mem = psutil.virtual_memory()
ram = mem.percent
ram_total = mem.total / (1024**3) # conversion bytes en Go
ram_used = mem.used / (1024**3) # conversion bytes en Go

os_name = platform.system()
os_version = platform.release()

# Nom de la machine
hostname = socket.gethostname()

# Heure de démarrage
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

# Uptime
uptime_seconds = (datetime.datetime.now() - boot_time).total_seconds()
uptime_hours = round(uptime_seconds / 3600, 1)

# Nombre d'utilisateurs connectés 
users_count = len(psutil.users())

# Adresse IP principale
ip_address = socket.gethostbyname(hostname)

# Récupération des processus en cours
processes = []

for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    try:
        info = proc.info
        processes.append(info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        continue

# Construction de la liste des processus pour le CPU
process_list_cpu = ""
for i, p in enumerate(processes):
    if i >= 20:
        break
    process_list_cpu += f"PID {p['pid']} - {p['name']} : {p['cpu_percent']:.1f} % CPU<br>"

# Construction de la liste des processus RAM
process_list_ram = ""
for i, p in enumerate(processes):
    if i >= 20:
        break
    process_list_ram += f"PID {p['pid']} - {p['name']} : {p['memory_percent']:.1f} % RAM<br>"


# Top 3 des processus les plus gourmands (CPU + RAM)
top3 = sorted(
    processes,
    key=lambda p: (p['cpu_percent'] + p['memory_percent']),
    reverse=True
)[:3]

top_processes = ""
for p in top3:
    top_processes += (
        f"PID {p['pid']} - {p['name']} : "
        f"{p['cpu_percent']:.1f} % CPU / {p['memory_percent']:.1f} % RAM<br>"
    )


# Lecture du template HTML
with open("template.html") as f:
    template = f.read()

# Remplacement des variables dans le HTML
html = template.replace("{{cpu}}", f"{cpu:.1f}")
html = html.replace("{{cpu_cores}}", str(cpu_cores))
html = html.replace("{{cpu_freq}}", f"{cpu_freq:.1f}")

html = html.replace("{{ram}}", f"{ram:.1f}")
html = html.replace("{{ram_total}}", f"{ram_total:.1f}")
html = html.replace("{{ram_used}}", f"{ram_used:.1f}")

html = html.replace("{{os_name}}", os_name)
html = html.replace("{{os_version}}", os_version)

html = html.replace("{{hostname}}", hostname)
html = html.replace("{{boot_time}}", str(boot_time))
html = html.replace("{{uptime_hours}}", str(uptime_hours))
html = html.replace("{{users_count}}", str(users_count))
html = html.replace("{{ip_address}}", ip_address)

html = html.replace("{{process_list_cpu}}", process_list_cpu)
html = html.replace("{{process_list_ram}}", process_list_ram)
html = html.replace("{{top_processes}}", top_processes)

# Génération du fichier HTML final
with open("index.html", "w") as f:
    f.write(html)
print("Page HTML générée : index.html")
