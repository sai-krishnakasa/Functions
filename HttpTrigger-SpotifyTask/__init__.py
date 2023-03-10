import logging
import requests
import azure.functions as func
from azure.storage.blob import BlockBlobService
import requests
import datetime
import json
import os 
import random

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')
        id=req.params.get('id',None)
        if id is not None:
            response=requests.get(f"https://jsonplaceholder.typicode.com/todos/{id}")
        else:
            response=requests.get(f"https://jsonplaceholder.typicode.com/todos/{random.choice(range(100))}")
            
        # loads to convert a json to python datatype
        # json_response=json.loads(response.content.decode("utf-8"))

        # dumps to convert a python object back to json
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename="response"+"_"+str(timestamp)                                         
        # with open(filename , "w") as f:
        #     json.dump(json_response,f)
        
        # configuring the storage account

        # Parse the connection string from the environment variable.
        storage_connection_string = os.environ["AzureWebJobsStorage"]

        # Create a BlockBlobService object from the connection string.
        block_blob_service = BlockBlobService(connection_string=storage_connection_string)


        container_name = "mycontainer"
        block_blob_service.create_container(container_name)

        # Upload the JSON file to the container.
        block_blob_service.create_blob_from_bytes(container_name, filename, response.content)

        return func.HttpResponse(f"Response saved to file {filename} and uploaded to container {container_name}. and this the path to see the output https://myblobstorageeacc.blob.core.windows.net/mycontainer/{filename}")
    except Exception as e:
        logging.info(str(e))
        return func.HttpResponse(f"An Error Occurred")


    
