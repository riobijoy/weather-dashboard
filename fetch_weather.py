from ftplib import FTP
import json
from datetime import datetime
import os

# FTP Credentials from GitHub Secrets
HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_USER")
PASSWORD = os.getenv("FTP_PASS")
PORT = int(os.getenv("FTP_PORT", 21))

# Connect FTP
ftp = FTP()
ftp.connect(HOST, PORT)
ftp.login(USER, PASSWORD)

print("Connected Successfully")

# Root folder
ROOT_FOLDER = "/"

# Go root
ftp.cwd(ROOT_FOLDER)

# Get all folders/files
items = ftp.nlst()

all_data = []

for item in items:

    try:

        print(f"Checking: {item}")

        ftp.cwd(f"/{item}")

        files = ftp.nlst()

        csv_files = [f for f in files if f.endswith(".csv")]

        if not csv_files:
            ftp.cwd(ROOT_FOLDER)
            continue

        csv_files.sort(reverse=True)

        latest_file = csv_files[0]

        print(f"Latest File: {latest_file}")

        # Download latest file
        with open(latest_file, "wb") as file:
            ftp.retrbinary(f"RETR {latest_file}", file.write)

        # Read CSV
        with open(latest_file, "r", encoding="utf-8", errors="ignore") as file:
            raw_data = file.read()

        all_data.append({
            "folder": item,
            "latest_file": latest_file,
            "updated_time": str(datetime.now()),
            "raw_weather_data": raw_data[:2000]
        })

        ftp.cwd(ROOT_FOLDER)

    except Exception as e:

        print(f"Skipping {item}: {e}")

        try:
            ftp.cwd(ROOT_FOLDER)
        except:
            pass

ftp.quit()

# Save JSON
with open("latest.json", "w") as json_file:
    json.dump(all_data, json_file, indent=4)

print("Weather data updated successfully")
