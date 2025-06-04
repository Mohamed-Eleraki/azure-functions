from azure.identity import *
from azure.mgmt.resource import ResourceManagementClient
from settings import *
import json

# import os
# from dotenv import load_dotenv

# load_dotenv((os.path.join(".env")))
# AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
print(AZURE_SUBSCRIPTION_ID)
print(os.getcwd())

environment_cre_attr = dir(EnvironmentCredential())
print(json.dumps(environment_cre_attr, indent=4, default=str))
