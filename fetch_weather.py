from ftplib import FTP
import json
import os

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

all_files = []

# Create preview folder
os.makedirs("preview", exist_ok=True)

for folder in items:

    try:

        ftp.cwd(f"/{folder}")

        files = ftp.nlst()

        csv_files = [f for f in files if f.endswith(".csv")]

        # Latest 5 files only
        csv_files.sort(reverse=True)

        for file in csv_files[:5]:

            try:

                station_id = "UNKNOWN"

                parts = file.replace(".csv","").split("_")

                if len(parts) >= 4:
                    station_id = parts[-1]

                local_file = f"preview/{folder}_{file}"

                # Download preview copy
                with open(local_file, "wb") as lf:
                    ftp.retrbinary(f"RETR {file}", lf.write)

                all_files.append({
                    "folder": folder,
                    "file": file,
                    "station_id": station_id,
                    "preview_file": local_file
                })

            except Exception as e:
                print(e)

        ftp.cwd(ROOT_FOLDER)

    except Exception as e:

        print(f"Skipping {folder}: {e}")

        try:
            ftp.cwd(ROOT_FOLDER)
        except:
            pass

ftp.quit()

# Save index
with open("files.json", "w") as json_file:
    json.dump(all_files, json_file, indent=4)

print("Portal updated successfully")
