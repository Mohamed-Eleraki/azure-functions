"""Module to read CSV files and return its values."""

import csv
import os
import json
from datetime import datetime
from urllib.parse import urlparse
from azure.storage.blob import ContainerClient

def csv_reader():
    """csv reader function.
    Reads a CSV file containing source and destination paths with SAS tokens.

    The function reads data from a file named 'data_catalog.csv' located in a parent
    directory relative to the current file. It parses each row into a dictionary
    with keys: 'src_path', 'src_sas', 'dest_path', and 'dest_sas'.

    Returns:
        list[dict]: A list of dictionaries, each containing:
            - src_path (str): Full source path.
            - src_sas (str): Source SAS token.
            - dest_path (str): Full destination path.
            - dest_sas (str): Destination SAS token.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        csv.Error: If there is an error parsing the CSV file.
        Exception: For any other unexpected errors.
    """
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
    return paths_list

# paths_list = csv_reader()
# print(json.dumps(paths_list, indent=4, default=str), end="\n\n\n")






def list_src_blobs_urls(paths_list):
    """list blobs from dir url function."""
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
        # return updated_src_paths
        # print(f"print blob entries: {json.dumps(updated_src_paths, indent=4, default=str)}", end="\n\n\n\n\n\n")
        
        # only_blob_paths = []
        # for blob_list in updated_src_paths:
        #     only_blob_paths.append(blob_list[1])
        #     only_blob_paths.append(blob_list)

        # updated_src_paths.append(updated_src_paths)
        continue
    return updated_src_paths
    # print(f"lastly: updated src paths: {json.dumps(updated_src_paths, indent=4, default=str)}")
    # for objects in updated_src_paths:
    #     object = objects[0]
    #     print(f"object: {object}")

    #     print(f"object name: {object.split("/")[-1]}")
    

# list_src_blobs_urls(paths_list)




def csv_dest_path_handler(paths_list):
    """ csv_des_path_handler function.
    Replaces placeholders in destination paths with a blob name and appends SAS tokens.

    This function processes a list of destination path entries, replaces the
    `$BLOB_NAME` placeholder in each destination path with the provided `blob_name`,
    appends the corresponding SAS token, and returns the updated destination paths.

    Args:
        paths_list (list[dict]): A list of dictionaries, each containing:
            - 'dest_path' (str): The destination path, potentially containing `$BLOB_NAME`.
            - 'dest_sas' (str): The SAS token to append.
        blob_name (str): The name of the blob to replace the `$BLOB_NAME` placeholder with.

    Returns:
        list[str]: A list of updated destination paths with placeholders replaced and SAS 
        tokens appended.
    """
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
    return updated_dest_paths

    # print("\n\ndestination paths: ")
    # print(json.dumps(updated_dest_paths, indent=4, default=str))
# csv_dest_path_handler(paths_list)


# def list_dest_blobs_urls(paths_list):
#     """list blobs from dir url function."""
#     updated_dest_paths = []
#     for path in paths_list:
#         dest_path = path["dest_path"]
#         dest_sas = path["dest_sas"]
        
#         parsed = urlparse(dest_path)
#         account_url = f"{parsed.scheme}://{parsed.netloc}"
#         container_name = parsed.path.strip("/").split("/")[0]
#         # dir_name = parsed.path.strip("/").split("/")[1:]
#         prefix = "/".join(parsed.path.strip("/").split("/")[1:])
#         container_client = ContainerClient(account_url, container_name=container_name, credential=dest_sas)
        
#         for blob in container_client.list_blobs(name_starts_with=prefix):
#             blob_url = f"{account_url}/{container_name}/{blob.name}?{dest_sas.lstrip('?')}"
#             # updated_src_paths.append((blob.name, blob_url))
#             updated_dest_paths.append((blob_url))
#         # return updated_src_paths
#         # print(f"print blob entries: {json.dumps(updated_src_paths, indent=4, default=str)}", end="\n\n\n\n\n\n")
        
#         # only_blob_paths = []
#         # for blob_list in updated_src_paths:
#         #     only_blob_paths.append(blob_list[1])
#         #     only_blob_paths.append(blob_list)

#         # updated_src_paths.append(updated_src_paths)
#         continue
#     # return updated_dest_paths
#     print(f"lastly: updated dest paths: {json.dumps(updated_dest_paths, indent=4, default=str)}")
#     # for objects in updated_src_paths:
#     #     object = objects[0]
#     #     print(f"object: {object}")

#     #     print(f"object name: {object.split("/")[-1]}")
# list_dest_blobs_urls(paths_list)




def csv_src_path_handler(paths_list):
    """ csv_src_path_handler function.
    Replaces wildcards in source paths with a blob name and appends SAS tokens.

    This function processes a list of source path entries (each with a SAS token),
    replaces any asterisk (`*`) in the source path with the given `blob_name`, appends
    the SAS token, and returns the fully resolved source paths.

    Args:
        paths_list (list[dict]): A list of dictionaries, each containing:
            - 'src_path' (str): The source path, potentially with a wildcard (*).
            - 'src_sas' (str): The SAS token to append.
        blob_name (str): The name of the blob to replace the wildcard with.

    Returns:
        list[str]: A list of updated source paths with wildcards replaced and SAS tokens appended.
    """

    updated_src_paths = []
    for path in paths_list:
        src_path = path["src_path"]
        src_sas = path["src_sas"]

        # if "*" in src_path:
        #     src_path = src_path.replace("*", blob_name)

        src_path = src_path + src_sas
        updated_src_paths.append(src_path)
        continue
    return updated_src_paths

def csv_dest_path_handler_old(paths_list):
    """ csv_des_path_handler function.
    Replaces placeholders in destination paths with a blob name and appends SAS tokens.

    This function processes a list of destination path entries, replaces the
    `$BLOB_NAME` placeholder in each destination path with the provided `blob_name`,
    appends the corresponding SAS token, and returns the updated destination paths.

    Args:
        paths_list (list[dict]): A list of dictionaries, each containing:
            - 'dest_path' (str): The destination path, potentially containing `$BLOB_NAME`.
            - 'dest_sas' (str): The SAS token to append.
        blob_name (str): The name of the blob to replace the `$BLOB_NAME` placeholder with.

    Returns:
        list[str]: A list of updated destination paths with placeholders replaced and SAS 
        tokens appended.
    """

    updated_dest_paths = []
    for path in paths_list:
        dest_path = path["dest_path"]
        dest_sas = path["dest_sas"]
        # if "$BLOB_NAME" in dest_path:
        #     dest_path = dest_path.replace("$BLOB_NAME", blob_name)
        dest_path = dest_path + dest_sas

        updated_dest_paths.append(dest_path)
        continue
    return updated_dest_paths
