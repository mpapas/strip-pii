# Deploying with AZD (Azure Developer CLI)

This guide explains how to deploy your Azure Function app (with Azure AI Language PII detection) using the Azure Developer CLI (`azd`).

---

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) installed and logged in
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) installed
- An Azure subscription with permission to create resources
- (Optional) [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite?tabs=visual-studio) for local development

---

## 1. Initialize the Project for AZD

If you haven't already, initialize the project:

```bash
azd init
```

- Follow prompts

---

## 2. Update Infrastructure for AI Language

**Ensure your Bicep/Terraform files provision:**
- An Azure Function App (Python)
- A Storage Account (for blob storage)
- An Azure AI Language resource (Cognitive Services Language)

If you need to add the AI Language resource, add a Bicep module like:

```bicep
resource language 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'your-language-resource'
  location: resourceGroup().location
  kind: 'Language'
  sku: {
    name: 'S' // or 'F0' for free tier
  }
  properties: {
    apiProperties: {
      statisticsEnabled: true
    }
  }
}
```

---

## 3. Configure Application Settings

Your Function App needs these settings:
- `AZURE_AI_LANGUAGE_ENDPOINT`: The endpoint of your Language resource
- `AZURE_AI_LANGUAGE_KEY`: The API key for your Language resource

**In Bicep:**
```bicep
resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  // ...existing config...
  properties: {
    siteConfig: {
      appSettings: [
        // ...existing settings...
        {
          name: 'AZURE_AI_LANGUAGE_ENDPOINT'
          value: language.properties.endpoint
        }
        {
          name: 'AZURE_AI_LANGUAGE_KEY'
          value: listKeys(language.id, language.apiVersion).key1
        }
      ]
    }
  }
}
```

---

## 4. Deploy to Azure

Run the following command to provision resources and deploy code:

```bash
azd up
```

- This will prompt for environment name, location, and subscription if not already set.
- It will deploy all infrastructure and your function code.

---

## 5. Verify Deployment

- After deployment, `azd` will output the Function App URL.
- Test your endpoint:

```bash
curl -X POST "<your-function-url>/api/processTranscript" \
  -H "Content-Type: application/json" \
  -d @requestPayload.json
```

---

## 6. Updating Configuration

To update app settings after deployment:

```bash
az functionapp config appsettings set \
  --name <function-app-name> \
  --resource-group <resource-group> \
  --settings AZURE_AI_LANGUAGE_ENDPOINT=<endpoint> AZURE_AI_LANGUAGE_KEY=<key>
```

Or update your Bicep/Terraform and re-run `azd up`.

---

## 7. Clean Up

To remove all resources created by this project:

```bash
azd down
```

---

## Troubleshooting
- Ensure your Azure AI Language resource is in the same region as your Function App for best performance.
- Check the Azure Portal for deployment errors or logs.
- Use `azd env get-values` to see current environment variables.
- Logs are available in Application Insights if enabled.

---

## References
- [Azure Developer CLI Docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure Functions Python Quickstart](https://learn.microsoft.com/azure/azure-functions/create-first-function-vs-code-python)
- [Azure AI Language Docs](https://learn.microsoft.com/azure/ai-services/language-service/overview)
