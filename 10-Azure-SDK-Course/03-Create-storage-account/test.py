import random
from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient

from setting import setting_fun

(
    AZURE_SUBSCRIPTION_ID,
    DATA_LAKE_CONNECTION_STRING,
    CONNECTION_STRING,
    AZURE_CLIENT_ID,
    AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET,
    STORAGE_ACCESS_KEY,
    DEFAULT_RESOURCE_GROUP,
    DEFAULT_LOCATION,
) = setting_fun()

sub_id = AZURE_SUBSCRIPTION_ID
print(sub_id)
