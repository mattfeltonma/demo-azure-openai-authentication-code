import logging
import sys
import os
import json
import requests
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
        
    try:
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("AZURE_API_KEY")
        }
        response = requests.post(
            url = f"{os.getenv("AZURE_OPENAI_ENDPOINT")}openai/deployments/{os.getenv("DEPLOYMENT_NAME")}/chat/completions?api-version={os.getenv("OPENAI_API_VERSION")}",
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
