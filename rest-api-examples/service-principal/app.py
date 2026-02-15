import logging
import sys
import os
import json
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

## This is my shitty canned logging function
##
def configure_logging(level="ERROR"):
    """This function sets up logging
        Args:
            level (str, optional): The logging level as a string. Defaults to "ERROR".
    """
    try:
        ## Convert the level string to uppercase so it matches what the logging library expects
        logging_level = getattr(logging, level.upper(), None)
        
        ## Validate that the level is a valid logging level
        if not isinstance(logging_level, int):
            raise ValueError(f'Invalid log level: {level}')
        
        ## Setup a logging format
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    except Exception as e:
        print(f"Failed to set up logging: {e}", file=sys.stderr)
        sys.exit(1)
   
## This function obtains an access token from Entra ID using a service principal with a client id and client secret
##
def authenticate_with_service_principal(client_id, client_credential, tenant_name, scopes):
    """This function obtains an access token from Entra ID using a service principal with a client id and client secret
        Args:
            client_id (str): The client id of the service principal
            client_credential (str): The client secret of the service principal
            tenant_name (str): The tenant id of the Entra ID tenant
            scopes (list): The scopes for which the access token is requested
        Returns:
            token: An access token that can be used to authenticate requests to Azure OpenAI
    """
    try: 
        logging.info('Attempting to obtain an access token...')
        
        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_credential,
            authority=f"https://login.microsoftonline.com/{tenant_name}"
        )
        result = app.acquire_token_for_client(scopes=scopes)

        if "access_token" in result:
            logging.info('Access token successfully acquired')
            return result['access_token']
        else:
            logging.error('Unable to obtain access token')
            logging.error(f"Error was: {result['error']}")
            logging.error(f"Error description was: {result['error_description']}")
            logging.error(f"Error correlation_id was: {result['correlation_id']}")
            raise Exception('Failed to obtain access token')
    except:
        logging.error('Failed to obtain access token: ', exc_info=True)
        sys.exit(1)

def main():

    ## Setup logging
    ##
    configure_logging("ERROR")

    ## Use dotenv library to load environmental variables from .env file.
    ## The variables loaded include AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
    ## DEPLOYMENT_NAME, OPENAI_API_VERSION, and AZURE_OPENAI_ENDPOINT
    try:
        load_dotenv('.env')
    except Exception as e:
        logging.error('Failed to load environmental variables: ', exc_info=True)
        sys.exit(1)
        
    ## Obtain an access token
    ##
    token = authenticate_with_service_principal(
        client_id = os.getenv('AZURE_CLIENT_ID'),
        client_credential = os.getenv('AZURE_CLIENT_SECRET'),
        tenant_name = os.getenv('AZURE_TENANT_ID'),
        scopes=[
            "https://cognitiveservices.azure.com/.default"
        ]
    )
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.post(
            url = f"{os.getenv("AZURE_OPENAI_ENDPOINT")}/openai/deployments/{os.getenv("DEPLOYMENT_NAME")}/chat/completions?api-version={os.getenv("OPENAI_API_VERSION")}",
            headers = headers,
            json = {
                "messages": [
                    {
                        "role": "user",
                        "content": "Tell me an interesting fact"
                    }
                ],
                "max_tokens": 100
            },
        )
        print(json.loads(response.text)['choices'][0]['message']['content'])
    except:
        logging.error('Failed to inference: ', exc_info=True)


if __name__ == "__main__":
    main()
