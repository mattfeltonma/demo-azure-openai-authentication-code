# Microsoft Foundry Authentication Code Samples

## Overview
This repository contains code samples of different methods to authenticate to the Microsoft Foundry (and Azure OpenAI Service and Azure AI Service) using the [Python openai library](https://pypi.org/project/openai/) with both the legacy API and the Azure OpenAI v1 API, Python [Azure AI Inference library](https://pypi.org/project/azure-ai-inference/), Python [langchain-openai library](https://pypi.org/project/langchain-openai/), and [Python requests library](https://pypi.org/project/requests/). Each example uses the ChatCompletions operation.

The samples assume the use of the [python-dotenv library](https://pypi.org/project/python-dotenv/) for storing sensitive variables.

The following authentication examples are provided:

1. [Managed Identity with Azure AI Inference SDK](/azure-ai-inference/managed-identity/)
2. [Service Principal with Azure AI Inference SDK](/azure-ai-inference/service-principal/)
3. [API Key with LangChain](/lanchain-openai-examples/api-key/)
4. [Service Principal with LangChain](/lanchain-openai-examples/service-principal/)
5. [API Key with OpenAI SDK with legacy API](/openai-api/legacy/api-key/)
6. [Managed Identity with OpenAI SDK with legacy API](/openai-library-examples/legacy/managed-identity/)
7. [Service Principal with OpenAI SDK with legacy API using Client Credentials Flow](/openai-api/legacy/service-principal/client-credentials/))
8. [Service Principal with OpenAI SDK with legacy API using OBO Flow](/openai-api/legacy/service-principal/on-behalf-of/))
9. [API Key with OpenAI SDK with v1 API](/openai-api/legacy/api-key/)
10. [Managed Identity with OpenAI SDK with v1 API](/openai-library-examples/legacy/managed-identity/)
11. [Service Principal with OpenAI SDK with v1 API using Client Credentials Flow](/openai-api/legacy/service-principal/client-credentials/))
12. [Service Principal with OpenAI SDK with v1 API using OBO Flow](/openai-api/legacy/service-principal/on-behalf-of/))
13. [API Key with REST API](/rest-api-examples/api-key/)
14. [Service Principal with REST API](/rest-api-examples/service-principal/)

In each example you will find a requirements.txt file with the required libraries and a sample environmental variables file that can be used with the python-dotenv library. You will need to rename it from .env-sample to .env.

When using the on-behalf-of flow, you will need to property configure the application registration to support [public client flows](https://learn.microsoft.com/en-us/entra/identity-platform/msal-client-applications).

