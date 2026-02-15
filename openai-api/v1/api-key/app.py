import logging
import sys
import os
from openai import OpenAI
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
    configure_logging("DEBUG")

    ## Use dotenv library to load environmental variables from .env file.
    ## The variables loaded include FOUNDRY_API_KEY, FOUNDRY_ENDPOINT, and 
    ## DEPLOYMENT_NAME
    try:
        load_dotenv('.env')
    except Exception as e:
        logging.error('Failed to load environmental variables: ', exc_info=True)
        sys.exit(1)

    ## Perform a chat completion using Azure OpenAI v1 API
    ##
    try:
        client = OpenAI(
            base_url = f"{os.getenv('FOUNDRY_ENDPOINT')}/openai/v1",
            api_key=os.getenv('FOUNDRY_API_KEY')
        )
        response = client.chat.completions.create(
            model=os.getenv('DEPLOYMENT_NAME'),
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
    
    ## Use the responses API

    except:
        logging.error('Failed chat completion: ', exc_info=True)

if __name__ == "__main__":
    main()
