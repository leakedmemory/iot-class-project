import re
import os
import base64
from azure.storage.blob import (BlobServiceClient, ContentSettings)
from datetime import (datetime, timedelta)
CONNECTION_STRING = os.environ['AZURE_STORAGE_IMAGES_CONNECTION_STRING']
AZURE_PRIMARY_KEY = os.environ['AZURE_STORAGE_IMAGES_PRIMARY_KEY']


def upload_blob(data, filename, container):
    # Base64 string representation of data (ex: profile image sent through JSON REST request)
    filename_with_extension = f'{filename}.jpg'

    # Azure Storage Blob takes bytes-object
    coded = base64.decodebytes(data.encode())

    # Create a new instance of BlobServiceClient; we will use this to create a Blob Client
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container, blob=filename_with_extension)

    # Upload
    my_content_settings = ContentSettings(content_type="image/jpg")
    blob_client.upload_blob(coded, blob_type="BlockBlob", overwrite=True,  content_settings=my_content_settings)

    return f'https://saprojetoiotimages.blob.core.windows.net/{container}/{filename_with_extension}'
