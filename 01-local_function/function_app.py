import azure.functions as func
import datetime
import json
import logging
import pandas as pd

app = func.FunctionApp()


# @app.route(route="localHTTPfunc", auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="students_req", auth_level=func.AuthLevel.ANONYMOUS)
def localHTTPfunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()  # use postman to send json body
        logging.info(req_body)

    except ValueError:
        return func.HttpResponse(
            "Json body requirement for this function to work!", status_code=500
        )
    
    df = pd.DataFrame(req_body['students'])
    df = df.explode('courses').reset_index(drop=True)
    df = pd.merge(df, pd.json_normalize(df['courses']), left_index=True, right_index=True)
    res = df.to_csv()

    return func.HttpResponse(
        # req_body,
        # f"Successfully loaded the json body! {df}",
        res,
        status_code=200,
    )
