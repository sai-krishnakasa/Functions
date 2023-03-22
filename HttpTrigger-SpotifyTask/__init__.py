import logging
import requests
import azure.functions as func
from azure.storage.blob import BlockBlobService
import requests
from  base64 import b64encode
import datetime
import json
import os 
import random


# Set the client ID and client secrety
client_id = '60caf6ff44c841d5849076609d24b0fe'
client_secret = 'cb2510f0cdb34085bde1f5e628856062'

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Is It Updated
    # Spotify API endpoint for retrieving access token 
    url = 'https://accounts.spotify.com/api/token'

    # Base64-encoded string that contains the client ID and secret key
    auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()

    # Parameters for the POST request
    data = {
        'grant_type': 'client_credentials'
    }

    # Headers for the POST request
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Send the POST request to retrieve the access token
    response = requests.post(url, data=data, headers=headers)

    # Get the access token from the response JSON
    access_token = response.json()['access_token']

    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    # search for tracks with "Billie Jean" in the name
    response = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params={'q': 'Billie Jean', 'type': 'track'})
    logging.info(response)
    
    try:
        logging.info('Python HTTP trigger function processed a request.')
        id=req.params.get('id',None)
            
        # loads to convert a json to python datatype
        # json_response=json.loads(response.content.decode("utf-8"))

        # dumps to convert a python object back to json
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename="response"+"_"+str(timestamp)                                         
       
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
        logging.info(e,exc_info=True)
        return func.HttpResponse(f"An Error Occurred")


    
