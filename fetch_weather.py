from ftplib import FTP
import os
import json

FTP_HOST = os.environ['FTP_HOST']
FTP_USER = os.environ['FTP_USER']
FTP_PASS = os.environ['FTP_PASS']

ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

folders = [
    "FREMAANHP02",
    "NHPASSAM"
]

all_files = []
latest_station = {}

os.makedirs("preview", exist_ok=True)

for folder in folders:

    try:

        ftp.cwd(f"/NHPASSAM/{folder}")

        files = ftp.nlst()

        csv_files = [
            f for f in files
            if f.endswith(".csv")
        ]

        csv_files.sort(reverse=True)

        for file in csv_files[:200]:

            local_file = f"preview/{folder}_{file}"

            try:

                with open(local_file, "wb") as lf:

                    ftp.retrbinary(
                        f"RETR {file}",
                        lf.write
                    )

                station_id = "UNKNOWN"
                csv_date = ""

                try:

                    with open(local_file, "r", errors="ignore") as rf:

                        lines = rf.readlines()

                        for line in lines:

                            if "&" in line:

                                parts = line.strip().split(",")

                                if len(parts) >= 2:

                                    station_id = (
                                        parts[0]
                                        .replace("&","")
                                        .strip()
                                    )

                                    raw_date = parts[1].strip()

                                    try:

                                        d,m,y = raw_date.split(" ")[0].split("/")

                                    except:

                                        try:
                                            d,m,y = raw_date.split(" ")[0].split("-")
                                        except:
                                            continue

                                    csv_date = f"20{y}-{m}-{d}"

                                    break

                except:
                    pass

                item = {
                    "folder": folder,
                    "file": file,
                    "station_id": station_id,
                    "date": csv_date,
                    "preview_file": local_file
                }

                all_files.append(item)

                latest_station[station_id] = item

            except:
                pass

    except:
        pass

with open("files.json", "w") as f:

    json.dump(
        all_files,
        f,
        indent=4
    )

with open("latest.json", "w") as f:

    json.dump(
        list(latest_station.values()),
        f,
        indent=4
    )

ftp.quit()

print("Weather data updated")
