import logging
import sys
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
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
   
def main():
    ## Setup logging
    ##
    configure_logging("ERROR")

    ## Use dotenv library to load environmental variables from .env file.
    ## The variables loaded include FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_API_KEY, and
    ## DEPLOYMENT_NAME
    try:
        load_dotenv('.env')
    except Exception as e:
        logging.error('Failed to load environmental variables: ', exc_info=True)
        sys.exit(1)

    ## Obtain an access token
    ##
    ## If using a user-assigned managed identity include the client_id
    if os.getenv("MANAGED_IDENTITY_CLIENT_ID"):
        credential = DefaultAzureCredential(managed_identity_client_id=os.getenv("MANAGED_IDENTITY_CLIENT_ID"))
    else:
        credential = DefaultAzureCredential()

    ## Setup a project client
    project_client = AIProjectClient(
        endpoint=os.getenv('FOUNDRY_PROJECT_ENDPOINT'),
        credential=credential
    )
    models = project_client.get_openai_client(os.getenv('OEPNAI_API_VERSION'))

    ## Perform a chat completion Foundry API
    ##
    try:

        client = ChatCompletionsClient(
            endpoint=f"{os.getenv('FOUNDRY_ENDPOINT')}/openai/deployments/{os.getenv('DEPLOYMENT_NAME')}",
            credential=DefaultAzureCredential(),
            credential_scopes=["https://cognitiveservices.azure.com/.default"]
    
        )

        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="Tell me an interesting fact."),
            ],
            max_tokens=100,
            model=os.getenv("DEPLOYMENT_NAME")
        )
        print(response.choices[0].message.content)
    except:
        logging.error('Failed chat completion: ', exc_info=True)

if __name__ == "__main__":
    main()
