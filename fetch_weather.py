from ftplib import FTP
import json
from datetime import datetime
import os

# FTP Credentials from GitHub Secrets
HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_USER")
PASSWORD = os.getenv("FTP_PASS")

# Connect FTP
ftp = FTP(HOST)
ftp.login(USER, PASSWORD)

# ROOT folder
ROOT_FOLDER = "/"

# Go to root
ftp.cwd(ROOT_FOLDER)

# Get all folders
folders = ftp.nlst()

all_data = []

# Loop through folders
for folder in folders:

    try:
        print(f"Checking Folder: {folder}")

        # Enter folder
        ftp.cwd(f"/{folder}")

        # List files
        files = ftp.nlst()

        # CSV files only
        csv_files = [f for f in files if f.endswith(".csv")]

        # Skip empty folders
        if not csv_files:
            ftp.cwd(ROOT_FOLDER)
            continue

        # Latest file
        csv_files.sort(reverse=True)
        latest_file = csv_files[0]

        print(f"Latest File: {latest_file}")

        # Download latest file
        with open(latest_file, "wb") as file:
            ftp.retrbinary(f"RETR {latest_file}", file.write)

        # Read file
        with open(latest_file, "r") as file:
            raw_data = file.read()

        # Store data
        all_data.append({
            "folder": folder,
            "latest_file": latest_file,
            "updated_time": str(datetime.now()),
            "raw_weather_data": raw_data
        })

        # Go back root
        ftp.cwd(ROOT_FOLDER)

    except Exception as e:

        print(f"Skipping {folder}: {e}")

        try:
            ftp.cwd(ROOT_FOLDER)
        except:
            pass

# Close FTP
ftp.quit()

# Save combined JSON
with open("latest.json", "w") as json_file:
    json.dump(all_data, json_file, indent=4)

print("All weather data updated successfully")
