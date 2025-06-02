"""Module to read CSV files and return its values."""

import csv
import os

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

def csv_src_path_handler(paths_list, blob_names):
    """ csv_src_path_handler function.
    Replaces wildcards in source paths with a blob name and appends SAS tokens.

    This function processes a list of source path entries (each with a SAS token),
    replaces any asterisk (`$BLOB_NAME`) in the source path with the given `blob_name`, appends
    the SAS token, and returns the fully resolved source paths.

    Args:
        paths_list (list[dict]): A list of dictionaries, each containing:
            - 'src_path' (str): The source path, potentially with a wildcard ($BLOB_NAME).
            - 'src_sas' (str): The SAS token to append.
        blob_name (str): The name of the blob to replace the wildcard with.

    Returns:
        list[str]: A list of updated source paths with wildcards replaced and SAS tokens appended.
    """
    updated_src_paths = []
    for blob_name in blob_names:
        for path in paths_list:
            src_path = path["src_path"]
            src_sas = path["src_sas"]

            if "$BLOB_NAME" in src_path:
                src_path = src_path.replace("$BLOB_NAME", blob_name)

            src_path = src_path + src_sas
            updated_src_paths.append(src_path)
            continue
    return updated_src_paths

def csv_dest_path_handler(paths_list, blob_names):
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
    for blob_name in blob_names:
        for path in paths_list:
            dest_path = path["dest_path"]
            dest_sas = path["dest_sas"]
            if "$BLOB_NAME" in dest_path:
                dest_path = dest_path.replace("$BLOB_NAME", blob_name)
            dest_path = dest_path + dest_sas

            updated_dest_paths.append(dest_path)
            continue
    return updated_dest_paths
