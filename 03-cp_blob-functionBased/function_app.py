# import os
import logging

# from azure.storage.blob import BlobClient, BlobServiceClient
import azure.functions as func

# from utils.cp_blob import cp_blob
# from utils.csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler
from cp_blob import cp_blob
from csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler

# app = func.FunctionApp()
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.blob_trigger(arg_name="myblob", path="source", connection="AzureWebJobsStorage")
def data_connector_cp_blob(myblob: func.InputStream) -> None:

    # logging.info(
    #     "Python blob trigger function processed blob. "
    #     "Name: %s. Blob Size: %s bytes.",
    #     myblob.name,
    #     myblob.length,
    # )

    logging.info(
        f"Python blob trigger function processed blob"
        f"Name: {myblob.name}"
        f"Blob Size: {myblob.length} bytes"
    )

    # Extract blob name (strip off container prefix)
    blob_name = myblob.name.split("/")[-1]
    # print(blob_name)
    # logging.info(f"Extracted blob name: {blob_name}")

    # Call the CSV reader function to get source and destination paths
    paths_list = csv_reader()

    # Call the CSV source paths
    updated_src_paths = csv_src_path_handler(paths_list, blob_name)

    # Call teh CSV destination paths
    updated_dest_paths = csv_dest_path_handler(paths_list, blob_name)

    # Call the cp_blob function to copy the blob
    # connection_string = os.environ["AzureWebJobsStorage"]
    # src_container_name = myblob.name.split("/")[-0]
    # cp_blob(updated_src_paths, updated_dest_paths, connection_string, src_container_name, blob_name)
    cp_blob(updated_src_paths, updated_dest_paths)

    # return {
    #         "status": "success",
    #         "message": "Blob copy operation completed successfully.",
    #         "blob_name": blob_name,
    #         "updated_src_paths": updated_src_paths,
    #         "updated_dest_paths": updated_dest_paths,
    #     }

    # blb = myblob.name.replace("source/sourcedir01/", "")
    # connect_str = os.environ["AzureWebJobsStorage"]
    # connection_name = "source"

    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # container_client = blob_service_client.get_container_client(connection_name)
    # blob_client = container_client.get_blob_client(blb)
    # stream = blob_client.download_blob()
    # stream.readall()
