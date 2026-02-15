import logging
import sys
import os
import msal
from azure.identity import OnBehalfOfCredential, get_bearer_token_provider
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

def acquire_user_assertion(client_id, tenant_id, initial_scope):
    """Acquire a user token via the device code flow to use as the user assertion in the OBO flow.
        This prompts the user to sign in via browser.
        Args:
            client_id (str): The client ID of the middle-tier app registration
            tenant_id (str): The Entra ID tenant ID
            initial_scope (str): The scope for the initial token (the middle-tier app's scope)
        Returns:
            str: The access token to use as the user assertion in the OBO flow
    """
    try:
        ## Create a public client app for the device code flow
        ## Service principal's app registration must suppport public client flow
        app = msal.PublicClientApplication(
            client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
        )

        ## Initiate the device code flow
        flow = app.initiate_device_flow(scopes=[initial_scope])
        if "user_code" not in flow:
            logging.error(f"Failed to initiate device code flow: {flow.get('error_description')}")
            sys.exit(1)

        ## Display the message to the user so they can authenticate
        print(flow["message"])

        ## Wait for the user to complete the authentication
        result = app.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            return result["access_token"]
        else:
            logging.error(f"Failed to acquire user token: {result.get('error_description')}")
            sys.exit(1)
    except Exception:
        logging.error('Failed to acquire user assertion: ', exc_info=True)
        sys.exit(1)

def authenticate_obo(tenant_id, client_id, client_secret, user_assertion, scope):
    """Exchange a user assertion for an access token using the On-Behalf-Of flow via azure.identity.
        Args:
            tenant_id (str): The Entra ID tenant ID
            client_id (str): The service principal client ID
            client_secret (str): The service principal client secret
            user_assertion (str): The incoming access token to exchange
            scope (str): The scope for the downstream resource (e.g., Azure OpenAI)
        Returns:
            token_provider: A token provider that can be used to obtain access tokens for the specified scope
    """
    try:
        credential = OnBehalfOfCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            user_assertion=user_assertion
        )
        token_provider = get_bearer_token_provider(credential, scope)
        return token_provider
    except Exception:
        logging.error('Failed to acquire OBO token: ', exc_info=True)
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

    ## Set environmental variables
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    tenant_id = os.getenv('AZURE_TENANT_ID')

    ## Acquire a user assertion
    initial_scope = os.getenv('INITIAL_SCOPE', f'{client_id}/.default')
    user_assertion = acquire_user_assertion(client_id, tenant_id, initial_scope)

    ## Exchange the assertion for an access token
    ##
    token_provider = authenticate_obo(
        tenant_id, client_id, client_secret,
        user_assertion,
        scope="https://cognitiveservices.azure.com/.default"
    )

    ## Perform a chat completion
    ##
    try:
        client = OpenAI(
            base_url = f"{os.getenv('FOUNDRY_ENDPOINT')}/openai/v1",
            api_key=token_provider
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
        
    except:
        logging.error('Failed chat completion: ', exc_info=True)

if __name__ == "__main__":
    main()
