import csv
import os
import json
from datetime import datetime
from urllib.parse import urlparse
from azure.storage.blob import ContainerClient

csv_path = os.path.join(os.path.dirname(__file__), "data_catalog_dataconnect.csv")
paths_list = []

try:
    with open(csv_path, "r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            paths_list.append({
                "src_path": row["full_source_path"],
                "src_sas" : row["src_sas"],
                "dest_path" : row["full_dest_path"],
                "dest_sas" : row["dest_sas"]
            })
                
except FileNotFoundError:
    print(f"File not found: {csv_path}")
except csv.Error as e:
    print(f"Error reading CSV file: {e}")

updated_src_paths = []
for path in paths_list:
    src_path = path["src_path"]
    src_sas = path["src_sas"]
    
    parsed = urlparse(src_path)
    account_url = f"{parsed.scheme}://{parsed.netloc}"
    container_name = parsed.path.strip("/").split("/")[0]
    # dir_name = parsed.path.strip("/").split("/")[1:]
    prefix = "/".join(parsed.path.strip("/").split("/")[1:])
    container_client = ContainerClient(account_url, container_name=container_name, credential=src_sas)
    
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_url = f"{account_url}/{container_name}/{blob.name}?{src_sas.lstrip('?')}"
        # updated_src_paths.append((blob.name, blob_url))
        updated_src_paths.append((blob_url))
# print(json.dumps(updated_src_paths, indent=4, default=str))

date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
updated_dest_paths = []
for path in paths_list:
    dest_path = path["dest_path"]
    dest_sas = path["dest_sas"]
    # if "$BLOB_NAME" in dest_path:
    #     dest_path = dest_path.replace("$BLOB_NAME", blob_name)
    dest_path = dest_path + date_now + dest_sas

    updated_dest_paths.append(dest_path)
    continue
# print(json.dumps(updated_dest_paths, indent=4, default=str))
