# import os
import logging

# from azure.storage.blob import BlobClient, BlobServiceClient
import azure.functions as func

# from utils.cp_blob import cp_blob
# from utils.csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler
from cp_blob import cp_blob
from csv_reader import csv_dest_path_handler, csv_reader, csv_src_path_handler

app = func.FunctionApp()


# @app.schedule(schedule="0 0 7 * * *", arg_name="myTimer", run_on_startup=True,
#               use_monitor=False)
@app.schedule(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False
)
def DataConnect_cp_blob_timer_trigger(myTimer: func.TimerRequest) -> None:

    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function executed.")

    # Extract blob name (strip off container prefix)
    # blob_name = myblob.name.split("/")[-1]
    blob_name = "dummy.txt"

    # Call the CSV reader function to get source and destination paths
    paths_list = csv_reader()

    # Call the CSV source paths
    updated_src_paths = csv_src_path_handler(paths_list, blob_name)

    # Call teh CSV destination paths
    updated_dest_paths = csv_dest_path_handler(paths_list, blob_name)

    # Call the cp_blob function to copy the blob
    cp_blob(updated_src_paths, updated_dest_paths)
