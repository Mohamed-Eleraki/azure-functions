"""Module to manage file transfer to/from Azure Blob Storage."""

import logging
from azure.storage.blob import BlobClient, ContainerClient
from csv_reader import csv_reader


def list_src_blob() -> list[str]:
    """list_src_blob function.
    Lists blobs in the source Azure Blob Storage container.
    """
    paths_list = csv_reader()
    for src_token in paths_list:
        src_sas_token = src_token["src_sas_token"]
    # cleaned_src_sas = srs_sas.replace("?", "")  # Remove the '?' from the SAS token if present

    blob_names = []
    account_url = "https://storage_account.blob.core.windows.net"
    container_name = "source"
    # sas_token = "3D"  # Can be None if using account key or other auth
    sas_token = src_sas_token  # Use the SAS token from the CSV reader

    # Initialize the ContainerClient
    container_client = ContainerClient(
        account_url, container_name=container_name, credential=sas_token
    )

    # List blobs in the container
    for blob in container_client.list_blobs():
        blob_name = blob.name
        blob_name = blob_name.split("/", -1)
        if len(blob_name) > 1:
            blob_names.append(blob_name[-1])

    return blob_names


def cp_blob(updated_src_paths, updated_dest_paths):
    """cp_blob function.

    None
    """

    for src_path, dest_path in zip(updated_src_paths, updated_dest_paths):
        try:
            logging.info(
                "Source Path: %s, Destination Path: %s.",
                src_path,
                dest_path,
            )

            dest_blob_client = BlobClient.from_blob_url(dest_path)

            src_blob_client = BlobClient.from_blob_url(src_path)

            if src_blob_client.exists():
                copy_props = dest_blob_client.start_copy_from_url(src_path)
                logging.info("copy started. copy ID %s.", copy_props["copy_id"])
                continue

        except Exception as e:
            logging.error("An error occurred while copying the blob: %s", e)
