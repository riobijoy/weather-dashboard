from ftplib import FTP
import json
from datetime import datetime
import os

# FTP Credentials
HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_USER")
PASSWORD = os.getenv("FTP_PASS")

# Connect FTP
ftp = FTP(HOST)
ftp.login(USER, PASSWORD)

# Go to folder
ftp.cwd("/NHPASSAM")

# Get all files
files = ftp.nlst()

# Keep only CSV files
csv_files = [f for f in files if f.endswith(".csv")]

# Sort latest file
csv_files.sort(reverse=True)

# Latest file
latest_file = csv_files[0]

print("Latest File:", latest_file)

# Download latest file
with open(latest_file, "wb") as file:
    ftp.retrbinary(f"RETR {latest_file}", file.write)

ftp.quit()

# Read CSV content
with open(latest_file, "r") as file:
    raw_data = file.read()

# Create JSON
data = {
    "latest_file": latest_file,
    "updated_time": str(datetime.now()),
    "raw_weather_data": raw_data
}

# Save JSON
with open("latest.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Weather data updated successfully")
