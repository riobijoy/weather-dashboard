from ftplib import FTP
import os
import json

FTP_HOST = os.environ['FTP_HOST']
FTP_USER = os.environ['FTP_USER']
FTP_PASS = os.environ['FTP_PASS']

ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

print("Connected FTP")

folders = [
    "FREMAANHP02",
    "NHPASSAM"
]

all_files = []
latest_station = {}

os.makedirs("preview", exist_ok=True)

# LIST ROOT
print("ROOT:")
print(ftp.nlst())

for folder in folders:

    try:

        print(f"Opening folder: {folder}")

        # IMPORTANT CHANGE
        ftp.cwd(folder)

        files = ftp.nlst()

        print(files[:5])

        csv_files = [
            f for f in files
            if f.lower().endswith(".csv")
        ]

        csv_files.sort(reverse=True)

        for file in csv_files[:50]:

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

                        text = rf.read()

                        lines = text.splitlines()

                        for line in lines:

                            if "," in line and "&" in line:

                                parts = line.split(",")

                                if len(parts) >= 2:

                                    station_id = (
                                        parts[0]
                                        .replace("&","")
                                        .strip()
                                    )

                                    raw_date = parts[1].strip()

                                    csv_date = raw_date

                                    break

                except Exception as e:

                    print("CSV Read Error:", e)

                item = {
                    "folder": folder,
                    "file": file,
                    "station_id": station_id,
                    "date": csv_date,
                    "preview_file": local_file
                }

                all_files.append(item)

                latest_station[station_id] = item

                print(item)

            except Exception as e:

                print("Download Error:", e)

        ftp.cwd("..")

    except Exception as e:

        print("Folder Error:", e)

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

print("DONE")
