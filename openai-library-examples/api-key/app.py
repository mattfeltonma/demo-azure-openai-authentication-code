import logging
import sys
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

## This function sets up logging
##
def configure_logging(level="ERROR"):
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
    ## The variables loaded include AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
    ## DEPLOYMENT_NAME, OPENAI_API_VERSION, and AZURE_OPENAI_ENDPOINT
    try:
        load_dotenv('.env')
    except Exception as e:
        logging.error('Failed to load environmental variables: ', exc_info=True)
        sys.exit(1)

    ## Perform a chat completion
    ##
    try:
        client = AzureOpenAI(
            api_version = os.getenv('OPENAI_API_VERSION'),
            azure_endpoint= os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_API_KEY')
        )
        response = client.chat.completions.create(
            model=os.getenv('DEPLOYMENT_NAME'),
            messages=[
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
