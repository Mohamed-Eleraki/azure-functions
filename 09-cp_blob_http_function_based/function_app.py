import logging
import azure.functions as func
from cp_blob import cp_blob, list_src_blob
from csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler

app = func.FunctionApp()


@app.schedule(
    schedule="0 0 19 * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False
)
def dataconnect_cp_blob_time_trigger(myTimer: func.TimerRequest) -> func.HttpResponse:

    try:
        logging.info("Python HTTP trigger function processed a request.")

        # Extract blob names
        blob_names = list_src_blob()

        # Call the CSV reader function to get source and destination paths
        paths_list = csv_reader()

        # Call the CSV source paths
        updated_src_paths = csv_src_path_handler(paths_list, blob_names)

        # Call teh CSV destination paths
        updated_dest_paths = csv_dest_path_handler(paths_list, blob_names)

        # Call the cp_blob function to copy the blob
        cp_blob(updated_src_paths, updated_dest_paths)

        return func.HttpResponse("Blob copied successfully", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
