"""Module to manage file transfer to/from Azure Blob Storage."""

import logging
from azure.storage.blob import BlobClient

def cp_blob(updated_src_paths, updated_dest_paths):
    """ cp_blob function.
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
                dest_path,)

            dest_blob_client = BlobClient.from_blob_url(dest_path)

            # Get the source blob client full URL
            src_blob_client = BlobClient.from_blob_url(src_path)

            if src_blob_client.exists():
                copy_props = dest_blob_client.start_copy_from_url(src_path)
                logging.info("copy started. copy ID %s.", copy_props['copy_id'])
                continue
            else:
                logging.warning("Source blob does not exist: %s", src_path)

            logging.info("copy started. copy ID %s", copy_props['copy_id'])

        except Exception as e:
            logging.error("An error occurred while copying the blob: %s", e)
