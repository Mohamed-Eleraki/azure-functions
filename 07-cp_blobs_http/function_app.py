import logging
import azure.functions as func
from cp_blob import cp_blob
from csv_reader import (
    csv_dest_path_handler,
    csv_reader,
    csv_src_path_handler,
    list_src_blobs_urls,
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="cp_blob_http_function_based")
def cp_blob_http_function_based(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Python HTTP trigger function processed a request.")

    # Extract blob name (strip off container prefix)
    # blob_name = myblob.name.split("/")[-1]
    # blob_name = "dummy.txt"

    # Call the CSV reader function to get source and destination paths
    paths_list = csv_reader()

    # Call the CSV source paths handler
    updated_src_paths = list_src_blobs_urls(paths_list)

    # Call the CSV dest paths handler
    updated_dest_paths = csv_dest_path_handler(paths_list)
    # Call the CSV source paths
    # updated_src_paths = csv_src_path_handler(paths_list)

    # Call teh CSV destination paths
    # updated_dest_paths = csv_dest_path_handler(paths_list)

    # Call the cp_blob function to copy the blob
    cp_blob(updated_src_paths, updated_dest_paths)

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
