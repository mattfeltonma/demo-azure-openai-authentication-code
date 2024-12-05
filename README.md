# Azure OpenAI Authentication Code Samples

## Overview
This repository contains code samples of different methods to authenticate to the Azure OpenAI Service using the [Python openai library](https://pypi.org/project/openai/), Python [langchain-openai library](https://pypi.org/project/langchain-openai/), and [Python requests library](https://pypi.org/project/requests/).

The samples assume the use of the [python-dotenv library](https://pypi.org/project/python-dotenv/) for storing sensitive variables.

The following authentication examples are provided:

1. [Service Principal with LangChain](/lanchain-openai-examples/service-principal/)
2. [API Key with LangChain](/lanchain-openai-examples/api-key/)
3. [Service Principal with OpenAI SDK](/openai-library-examples/service-principal/)
4. [Managed Identity with OpenAI SDK](/openai-library-examples/managed-identity/)
5. [API Key with OpenAI SDK](/openai-library-examples/api-key/)
6. [Service Principal with REST API](/rest-api-examples/service-principal/)
7. [API Key with REST API](/rest-api-examples/api-key/)

In each example you will find a requirements.txt file with the required libraries and a sample environmental variables file that can be used with the python-dotenv library. You will need to rename it from .env-sample to .env.

