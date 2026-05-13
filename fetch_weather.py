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

        for file in csv_files[:100]:

            local_file = f"preview/{folder}_{file}"

            try:

                with open(local_file, "wb") as lf:

                    ftp.retrbinary(
                        f"RETR {file}",
                        lf.write
                    )

                station_id = "UNKNOWN"

                try:

                    station_id = file.split("_")[-1].replace(".csv","")

                except:
                    pass

                file_date = ""

                try:

                    parts = file.split("_")

                    raw = parts[1]

                    yy = raw[0:2]
                    mm = raw[2:4]
                    dd = raw[4:6]

                    file_date = f"20{yy}-{mm}-{dd}"

                except:
                    pass

                item = {
                    "folder": folder,
                    "file": file,
                    "station_id": station_id,
                    "date": file_date,
                    "preview_file": local_file
                }

                all_files.append(item)

                latest_station[station_id] = item

            except:
                pass

    except:
        pass

# SAVE HISTORY

with open("files.json", "w") as f:

    json.dump(
        all_files,
        f,
        indent=4
    )

# SAVE LATEST DASHBOARD

with open("latest.json", "w") as f:

    json.dump(
        list(latest_station.values()),
        f,
        indent=4
    )

ftp.quit()

print("Weather data updated")
