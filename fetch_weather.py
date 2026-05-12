from ftplib import FTP
import json
from datetime import datetime
import os

# FTP Credentials from GitHub Secrets
HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_USER")
PASSWORD = os.getenv("FTP_PASS")

# FTP Connection
ftp = FTP(HOST)
ftp.login(USER, PASSWORD)

# Weather file name
filename = "weather.txt"

# Download file
with open(filename, "wb") as file:
    ftp.retrbinary(f"RETR {filename}", file.write)

ftp.quit()

# Read weather data
with open(filename, "r") as file:
    raw_data = file.read()

# Create JSON
data = {
    "station": "Assam Weather Station",
    "weather_data": raw_data,
    "updated_time": str(datetime.now())
}

# Save JSON
with open("latest.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Weather updated successfully")
