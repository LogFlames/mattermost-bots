import os

for service in os.listdir("services"):
    os.system(f"sudo systemctl try-restart {service}")
