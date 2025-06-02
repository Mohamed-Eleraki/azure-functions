import os
from azure.storage.blob import BlobClient, BlobServiceClient
import logging
import azure.functions as func

# from utils.cp_blob import cp_blob
# from utils.csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler
from cp_blob import cp_blob
from csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler


app = func.FunctionApp()


@app.route(route="http_trigger_blob_name", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger_blob_name(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )


@app.blob_trigger(arg_name="myblob", path="source", connection="AzureWebJobsStorage")
def data_connector_cp_blob(myblob: func.InputStream) -> None:

    logging.info(
        "Python blob trigger function processed blob. "
        "Name: %s. Blob Size: %s bytes.",
        myblob.name,
        myblob.length,
    )

    # Extract blob name (strip off container prefix)
    blob_name = myblob.name.split("/")[-1]
    print(blob_name)
    logging.info("Extracted blob name: %s", blob_name)

    # Call the CSV reader function to get source and destination paths
    # paths_list = csv_reader()

    # Call the CSV source paths
    # updated_src_paths = csv_src_path_handler(paths_list, blob_name)

    # Call teh CSV destination paths
    # updated_dest_paths = csv_dest_path_handler(paths_list, blob_name)

    # Call the cp_blob function to copy the blob
    # connection_string = os.environ["AzureWebJobsStorage"]
    # src_container_name = myblob.name.split("/")[-0]
    # cp_blob(updated_src_paths, updated_dest_paths, connection_string, src_container_name, blob_name)
    # cp_blob(updated_src_paths, updated_dest_paths)

    # blb = myblob.name.replace("source/sourcedir01/", "")
    # connect_str = os.environ["AzureWebJobsStorage"]
    # connection_name = "source"

    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # container_client = blob_service_client.get_container_client(connection_name)
    # blob_client = container_client.get_blob_client(blb)
    # stream = blob_client.download_blob()
    # stream.readall()
