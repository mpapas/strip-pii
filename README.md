# PII Redaction Function App

An Azure Functions HTTP endpoint that automatically detects and redacts Personally Identifiable Information (PII) from call transcripts using Azure AI Language, then stores the cleaned transcripts in Azure Blob Storage.

## 🎯 Overview

This solution provides a serverless HTTP API that:
- Receives JSON payloads with transcript data from webhooks (e.g., CallRail)
- Uses **Azure AI Language** to detect and redact PII (names, emails, phone numbers, etc.)
- Saves cleaned transcripts to **Azure Blob Storage** with dynamic naming
- Returns the redacted transcript in the HTTP response

**Key Features:**
- 🔒 **Real PII Detection**: Azure AI Language Text Analytics API
- 📦 **Modular Design**: Separate PII detection module for reusability
- 🧪 **Comprehensive Testing**: Unit tests and end-to-end tests
- 📚 **Complete Documentation**: Setup, deployment, and architecture guides

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure subscription
- [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [Azure Storage Emulator and VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Azurite.azurite)


### Local Development
1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd strip-pii
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Azure AI Language:**
   ```bash
   # Copy environment template and add your credentials
   cp .env.sample .env
   # Edit .env with your Azure AI Language endpoint and key
   ```
   - For detailed setup instructions, see [Azure AI Setup Guide](docs/AZURE_AI_SETUP.md)

3. **Start local development:**
   - Easiest way to start the storage emulator is to use the Command Palette in VS Code
   
   ```bash
   # Terminal 1: Start storage emulator
   azurite --location ./azurite
   or...
   azurite --location ./azurite --debug ./azurite/debug.log

   # Terminal 2: Start Functions host
   func host start
   ```

## 📁 Project Structure

```
strip-pii/
├── function_app.py          # Main Azure Function HTTP endpoint
├── pii_detection.py         # PII detection module using Azure AI
├── tests/                   # Test suite
│   ├── README.md           # Test documentation
│   ├── test_function.py    # End-to-end HTTP tests
│   └── test_pii_module.py  # PII module unit tests
├── run_tests.sh            # Test runner script
├── requirements.txt        # Python dependencies
├── local.settings.json     # Local configuration
├── host.json              # Functions host configuration
└── docs/                  # Documentation
    ├── DESCRIPTION.md      # Detailed architecture
    ├── DEPLOY.md          # Deployment guide
    └── AZURE_AI_SETUP.md  # AI service setup
```

## 🧪 Testing

Use the convenient test runner script:

```bash
./run_tests.sh help      # Show available commands
./run_tests.sh pii       # Test PII module only
./run_tests.sh function  # Test HTTP endpoint (requires running host)
./run_tests.sh all       # Run all tests
```

For detailed testing instructions, see [tests/README.md](tests/README.md).

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/DESCRIPTION.md](docs/DESCRIPTION.md) | **Architecture overview** - Detailed flow, components, and technical design |
| [docs/DEPLOY.md](docs/DEPLOY.md) | **Deployment guide** - Step-by-step Azure deployment with AZD |
| [docs/AZURE_AI_SETUP.md](docs/AZURE_AI_SETUP.md) | **AI service setup** - Configure Azure AI Language for PII detection |
| [tests/README.md](tests/README.md) | **Testing guide** - How to run and understand the test suite |

## 🔧 Configuration

### Required Environment Variables
- `AZURE_AI_LANGUAGE_ENDPOINT` - Azure AI Language service endpoint
- `AZURE_AI_LANGUAGE_KEY` - Azure AI Language service key
- `AzureWebJobsStorage` - Azure Storage connection string

### Local Development Files
- `.env` - Environment variables for development (copy from `.env.sample`)
- `local.settings.json` - Azure Functions local configuration (not committed to git)

## 🌐 API Usage

**Endpoint:** `POST /api/processTranscript`

**Request Body:**
```json
{
  "id": "call-123",
  "transcription": "Hi, my name is John Doe and my email is john@example.com"
}
```

**Response:**
```json
{
  "transcription": "Hi, my name is [REDACTED_PERSON] and my email is [REDACTED_EMAIL]"
}
```

**Storage:** Cleaned transcript saved as `call-123_cleaned.txt` in Azure Blob Storage.

## 🚀 Deployment

Deploy to Azure using Azure Developer CLI:

```bash
# Initialize and deploy
azd init
azd up
```

For detailed deployment instructions, see [docs/DEPLOY.md](docs/DEPLOY.md).

## 🏗️ Architecture

The system follows a simple, serverless architecture:

1. **HTTP Trigger** → Azure Function receives transcript JSON
2. **PII Detection** → Azure AI Language analyzes and redacts PII
3. **Storage** → Cleaned transcript saved to Azure Blob Storage
4. **Response** → Returns redacted transcript to caller

For detailed architecture diagrams and flow explanations, see [docs/DESCRIPTION.md](docs/DESCRIPTION.md).

## 🛠️ Tech Stack

- **Runtime:** Azure Functions (Python 3.x)
- **AI Service:** Azure AI Language (Text Analytics PII Detection)
- **Storage:** Azure Blob Storage
- **Testing:** Custom test suite with HTTP and unit tests
- **Deployment:** Azure Developer CLI (AZD)

## 📝 License

[Add license information here]

## 🤝 Contributing

[Add contributing guidelines here]

---

**Need help?** Check the [documentation](#-documentation) or review the test examples in the `tests/` folder.
