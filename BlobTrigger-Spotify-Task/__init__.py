import logging
from azure.storage.blob import BlockBlobService
import os
import json
import azure.functions as func
from datetime import datetime


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    blob_data=myblob.read() 
    blob_data = blob_data.decode('utf-8')
    # Convert the JSON string to a dictionary
    json_dict = json.loads(blob_data) 
    albums=[]
    singles=[]
    compilations=[]
    for i in json_dict['tracks']['items']:
        if i['album']['album_type']=='album':
            albums.append(i)
        elif i['album']['album_type']=='single':
            singles.append(i)
        else:
            compilations.append(i)
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Parse the connection string from the environment variable.
    storage_connection_string = os.environ["AzureWebJobsStorage"]

    # Create a BlockBlobService object from the connection string.
    block_blob_service = BlockBlobService(connection_string=storage_connection_string)

    containers = ["album-container","singles-container","compilation-container"]
    for container_name in containers:
        block_blob_service.create_container(container_name)
    try:
        block_blob_service.create_blob_from_text(containers[0],"Album_"+str(timestamp),str(albums))
        block_blob_service.create_blob_from_text(containers[1],"Singles_"+str(timestamp),str(singles))
        block_blob_service.create_blob_from_text(containers[2],"Compilations_"+str(timestamp),str(compilations))
    except Exception as e:
        logging.info(e) 

    logging.info(f"Files saved to {containers}")
