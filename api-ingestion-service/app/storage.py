import os
from azure.storage.blob import BlobServiceClient

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")
CONTAINER = "datalake"

blob_service = BlobServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
    credential=ACCOUNT_KEY
)

def upload_to_landing(partner, dataset, filename, data):
    blob_path = f"landing/{partner}/{dataset}/{filename}"
    blob_client = blob_service.get_blob_client(
        container=CONTAINER,
        blob=blob_path
    )
    blob_client.upload_blob(data, overwrite=True)
    return blob_path