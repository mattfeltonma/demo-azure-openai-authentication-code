import logging
import sys
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
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
   
## This function obtains an access token from Entra ID using a managed identity and optionally accepts a client id if a user-assigned managed identity is used
##
def authenticate_with_managed_identity(scope,mi_client_id=None):
    """This function obtains an access token from Entra ID using a managed identity and optionally accepts a client id if a user-assigned managed identity is used
        Args:
            scope (str): The scope for which the access token is requested
            mi_client_id (str, optional): The client id of the user-assigned managed identity. If not provided, the function will attempt to authenticate using the system-assigned managed identity. Defaults to None.
        Returns:
            token_provider: A token provider that can be used to obtain access tokens for the specified scope
    """
    try:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(
                managed_identity_client_id=mi_client_id),
            scope
        ) 
        return token_provider
    except:
        logging.error('Failed to obtain access token: ', exc_info=True)
        sys.exit(1)
        
def main():
    ## Setup logging
    ##
    configure_logging("ERROR")
    
    ## Use dotenv library to load environmental variables from .env file.
    ## The variables loaded include FOUNDRY_ENDPOINT, DEPLOYMENT_NAME, and optionally 
    ## MANAGED_IDENTITY_CLIENT_ID if using a user-assigned managed identity
    try:
        load_dotenv('.env')
    except Exception as e:
        logging.error('Failed to load environmental variables: ', exc_info=True)
        sys.exit(1)
        
    ## Obtain an access token
    ##
    ## If using a user-assigned managed identity include the client_id
    if os.getenv("MANAGED_IDENTITY_CLIENT_ID"):
        token_provider = authenticate_with_managed_identity(scope="https://cognitiveservices.azure.com/.default",mi_client_id=os.getenv("MANAGED_IDENTITY_CLIENT_ID"))
    else:
        token_provider = authenticate_with_managed_identity(scope="https://cognitiveservices.azure.com/.default")


    ## Perform a chat completion
    ##
    try:
        client = OpenAI(
            base_url = f"{os.getenv('FOUNDRY_ENDPOINT')}/openai/v1",
            api_key=token_provider
        )
        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME"),
            messages=[
                {
                    "role":"system",
                    "content":"You are a helpful assistant that provides interesting facts."
                },
                {
                    "role": "user",
                   "content": "Tell me an interesting fact"
                }
            ],
            max_tokens=100
        )
        print(response.choices[0].message.content)
        
    except:
        logging.error('Failed chat completion: ', exc_info=True)

if __name__ == "__main__":
    main()
