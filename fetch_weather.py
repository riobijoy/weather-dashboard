from ftplib import FTP
import json
from datetime import datetime
import os
import csv

# FTP Credentials
HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_USER")
PASSWORD = os.getenv("FTP_PASS")
PORT = int(os.getenv("FTP_PORT", 21))

# Connect FTP
ftp = FTP()
ftp.connect(HOST, PORT)
ftp.login(USER, PASSWORD)

print("Connected Successfully")

ROOT_FOLDER = "/"

ftp.cwd(ROOT_FOLDER)

items = ftp.nlst()

all_data = []

for item in items:

    try:

        ftp.cwd(f"/{item}")

        files = ftp.nlst()

        csv_files = [f for f in files if f.endswith(".csv")]

        if not csv_files:
            ftp.cwd(ROOT_FOLDER)
            continue

        csv_files.sort(reverse=True)

        latest_file = csv_files[0]

        temp_file = f"temp_{latest_file}"

        with open(temp_file, "wb") as file:
            ftp.retrbinary(f"RETR {latest_file}", file.write)

        with open(temp_file, "r", encoding="utf-8", errors="ignore") as file:

            lines = file.readlines()

        os.remove(temp_file)

        clean_lines = [line.strip().replace("&", "") for line in lines if line.strip()]

        latest_row = clean_lines[-1]

        values = latest_row.split(",")

        station_id = values[0] if len(values) > 0 else "--"
        datetime_value = values[1] if len(values) > 1 else "--"
        battery = values[3] if len(values) > 3 else "--"
        water_level = values[4] if len(values) > 4 else "--"
        hourly_rain = values[5] if len(values) > 5 else "--"
        daily_rain = values[6] if len(values) > 6 else "--"
        temperature = values[7] if len(values) > 7 else "--"

        all_data.append({
            "folder": item,
            "station_id": station_id,
            "datetime": datetime_value,
            "battery": battery,
            "water_level": water_level,
            "hourly_rain": hourly_rain,
            "daily_rain": daily_rain,
            "temperature": temperature,
            "latest_file": latest_file,
            "updated_time": str(datetime.now())
        })

        ftp.cwd(ROOT_FOLDER)

    except Exception as e:

        print(f"Skipping {item}: {e}")

        try:
            ftp.cwd(ROOT_FOLDER)
        except:
            pass

ftp.quit()

with open("latest.json", "w") as json_file:
    json.dump(all_data, json_file, indent=4)

print("Weather dashboard updated successfully")
