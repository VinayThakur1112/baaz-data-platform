import os
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from schemas import SCHEMAS

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")
CONTAINER = "datalake"
SOURCE = "northwind"

blob_service = BlobServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
    credential=ACCOUNT_KEY
)

def process_dataset(dataset):
    landing_prefix = f"landing/{SOURCE}/{dataset}/"
    raw_prefix = f"raw/{SOURCE}/{dataset}/ingest_date={datetime.now().date()}/"

    container_client = blob_service.get_container_client(CONTAINER)

    blobs = container_client.list_blobs(name_starts_with=landing_prefix)

    for blob in blobs:
        file_name = os.path.basename(blob.name)

        if not file_name.endswith(".csv"):
            continue

        blob_client = container_client.get_blob_client(blob.name)
        data = blob_client.download_blob().readall()

        df = pd.read_csv(
            pd.io.common.BytesIO(data),
            dtype=str
        )

        expected_cols = SCHEMAS[dataset]
        if list(df.columns) != expected_cols:
            raise Exception(f"Schema mismatch for {dataset}")

        # Add metadata columns
        df["ingest_ts"] = datetime.utcnow().isoformat()
        df["source"] = SOURCE
        df["dataset"] = dataset
        df["file_name"] = file_name

        raw_blob_path = raw_prefix + file_name.replace(".csv", ".parquet")

        raw_blob_client = container_client.get_blob_client(raw_blob_path)
        raw_blob_client.upload_blob(
            df.to_parquet(index=False),
            overwrite=True
        )

        # Archive original file
        archive_path = blob.name.replace("landing/", "landing_archive/")
        archive_client = container_client.get_blob_client(archive_path)
        archive_client.upload_blob(data, overwrite=True)
        blob_client.delete_blob()