# Azure AI Language Setup

This document explains how to configure Azure AI Language for PII detection in your function app.

## Prerequisites

1. **Azure Subscription**: You need an active Azure subscription
2. **Azure AI Language Resource**: Create through Azure Portal or Azure AI Foundry

## Setup Steps

### 1. Create Azure AI Language Resource

#### Option A: Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Language Service" 
4. Select "Language Service" by Microsoft
5. Click "Create"
6. Fill in the required details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region (e.g., East US, West US 2)
   - **Name**: Unique name for your resource
   - **Pricing Tier**: Choose based on your needs (F0 for free tier, S for standard)

#### Option B: Azure AI Foundry
1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Create a new project or use existing
3. Add Language Service to your project
4. Configure the service settings

### 2. Get Connection Details

After creating the resource:

1. Go to your Language Service resource in Azure Portal
2. Navigate to "Keys and Endpoint" (left sidebar)
3. Copy the following:
   - **Endpoint**: The URL (e.g., `https://your-resource.cognitiveservices.azure.com/`)
   - **Key**: Either Key 1 or Key 2

### 3. Configure Local Development

Update your `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_AI_LANGUAGE_ENDPOINT": "https://your-resource.cognitiveservices.azure.com/",
    "AZURE_AI_LANGUAGE_KEY": "your-api-key-here"
  }
}
```

### 4. Configure Production Deployment

For Azure Functions deployed to Azure:

1. Go to your Function App in Azure Portal
2. Navigate to "Configuration" → "Application settings"
3. Add the following application settings:
   - `AZURE_AI_LANGUAGE_ENDPOINT`: Your endpoint URL
   - `AZURE_AI_LANGUAGE_KEY`: Your API key

### 5. Test the Integration

The function will automatically:
- Try to use Azure AI Language if credentials are configured
- Fall back to simple regex-based PII removal if Azure AI Language is not available
- Log the detection results and any errors

## PII Categories Detected

Azure AI Language can detect and redact these PII categories:
- Person names
- Email addresses
- Phone numbers
- Addresses
- Social Security Numbers
- Credit card numbers
- Passport numbers
- Driver's license numbers
- Bank account numbers
- And many more...

## Pricing

- **Free Tier (F0)**: 5,000 text records per month
- **Standard Tier (S)**: Pay per use, see [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)

## Troubleshooting

- **"Azure AI Language credentials not configured"**: Check your environment variables
- **"Failed to process text with Azure AI Language service"**: Check your endpoint URL and API key
- **Network errors**: Ensure your function app can reach the Azure AI endpoint

The function includes comprehensive error handling and will fall back to regex-based PII removal if Azure AI Language is unavailable.