import azure.functions as func
import datetime
import json
import logging
import pandas as pd
import subprocess
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import csv

app = func.FunctionApp()
@app.blob_trigger(arg_name="myblob", path="source/{name}",  # fire when a blob is created in the source container
                               connection="AzureWebJobsStorage")
def DataConnector_cBlob_1001(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")

    # Extract blob name (strip off container prefix)
    blob_name = myblob.name.split("/")[-1]
    
    # load mapping CSV
    csv_path = os.path.join(os.path.dirname(__file__), "data_catalog.csv")
    try:
        with open(csv_path, "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                src_path = row["full_source_path"]
                dest_path = row["full_dest_path"]
                # dest_path = dest_path + blob_name
 
                if "*" in src_path:
                    src_path = src_path.replace("*", blob_name)
                    
                dest_blob_client = BlobClient.from_blob_url(dest_path)
                # copy_props = dest_blob_client.start_copy_from_url(src_path)
                src_blob_client = BlobClient.from_blob_url(src_path)
                
                if src_blob_client.exists():
                    copy_props = dest_blob_client.start_copy_from_url(src_path)
                    logging.info(f"copy started. copy ID {copy_props['copy_id']}")
                else:
                    logging.warning(f"Source blob does not exist yet: {src_path}")
                    
                logging.info(f"copy started. copy ID {copy_props['copy_id']}")

                # cmd = [
                #     "azcopy",
                #     "copy",
                #     src_path,
                #     dest_path
                #     # "--recursive=true",
                #     # "--overwrite=true"
                # ]
                # logging.info(f"Running AzCopy: {' '.join(cmd)}")
                # subprocess.run(cmd, check=True, capture_output=True, text=True)
                # # logging.info(f"AzCopy stdout: {result.stdout}")
                # # logging.error(f"AzCopy stderr: {result.stderr}")
                # logging.info(f"Successfully copied {blob_name} to destination container.")

    except subprocess.CalledProcessError as e:
        logging.error(f"AzCopy failed: {e}")
    
    # # Construct source blob URL (including SAS token)
    # src_container_url = os.environ["SRC_CONTAINER_URL"].rstrip("/")
    # src_sas_token = os.environ["SRC_SAS_TOKEN"].lstrip("?")

    # # Full source blob URL
    # src_blob_url = f"{src_container_url}/{blob_name}?{src_sas_token}"

    # # Construct destination blob URL
    # dest_container_url = os.environ["DEST_CONTAINER_URL"].rstrip("/")  # With SAS token

    # # Full destination blob path
    # dest_blob_url = f"{dest_container_url}/{blob_name}"

    # try:
    #     cmd = [
    #         "azcopy",
    #         "copy",
    #         src_blob_url,
    #         dest_blob_url,
    #         "--recursive=true",
    #         "--overwrite=true"
    #     ]

    #     logging.info(f"Running AzCopy: {' '.join(cmd)}")
    #     subprocess.run(cmd, check=True)
    #     logging.info(f"Successfully copied {blob_name} to destination container.")

    # except subprocess.CalledProcessError as e:
    #     logging.error(f"AzCopy failed: {e}")