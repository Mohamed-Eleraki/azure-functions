"""Module to manage file transfer to/from Azure Blob Storage."""

import logging
from azure.storage.blob import BlobClient, ContainerClient

# from urllib.parse import urlparse


def list_src_blob():

    blob_names = []
    account_url = "https://STORAGE_ACCOUNT.blob.core.windows.net"
    container_name = "source"
    sas_token = "sas"  # Can be None if using account key or other auth

    # Initialize the ContainerClient
    container_client = ContainerClient(
        account_url, container_name=container_name, credential=sas_token
    )

    # List blobs in the container
    # print(f"Listing blobs in container '{container_name}':")
    for blob in container_client.list_blobs():
        blob_name = blob.name
        blob_name = blob_name.split("/", -1)
        if len(blob_name) > 1:
            blob_names.append(blob_name[-1])

    return blob_names


# blob_names = list_src_blob()
# for blob in blob_names:
#     print(blob)
# for item in list_blobs:
#     print(item[-1])


# def cp_blob(updated_src_paths, updated_dest_paths, connection_string, src_container_name, blob_names):
def cp_blob(updated_src_paths, updated_dest_paths):
    """cp_blob function.
    Copies blobs from source to destination using Azure Blob Storage URLs.

    This function takes lists of fully-formed source and destination blob URLs
    (including SAS tokens), creates `BlobClient` instances, and initiates
    asynchronous blob copy operations from source to destination.

    For each pair of source and destination paths:
    - Logs the paths.
    - Checks if the source blob exists.
    - Starts the copy process.
    - Logs the copy ID if the operation starts successfully.

    Args:
        updated_src_paths (list[str]): List of complete source blob URLs with SAS tokens.
        updated_dest_paths (list[str]): List of complete destination blob URLs with SAS tokens.

    Returns:
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

            # dest_blob_client = BlobClient.from_connection_string(
            #     conn_str=connection_string,
            #     container_name=dest_path.split("?")[-0],
            #     blob_names=blob_names)

            # src_blob_client = BlobClient.from_connection_string(
            #     conn_str=connection_string,
            #     container_name=src_container_name,
            #     blob_names=blob_names)

            if src_blob_client.exists():
                # copy_props = dest_blob_client.start_copy_from_url(src_path)
                copy_props = dest_blob_client.start_copy_from_url(src_path)
                logging.info("copy started. copy ID %s.", copy_props["copy_id"])
                continue

        except Exception as e:
            logging.error("An error occurred while copying the blob: %s", e)
