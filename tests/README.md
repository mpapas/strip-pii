# Test Suite

This directory contains test scripts for the PII redaction function app.

## Test Files

| File | Description |
|------|-------------|
| `test_function.py` | End-to-end test of the HTTP function endpoint |
| `test_pii_module.py` | Unit test of the PII detection module |

## Running Tests

### Prerequisites
1. Make sure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure Azure AI Language (for real PII detection tests):
   
   **Option A: Using .env file (recommended)**
   ```bash
   # Copy the template file
   cp .env.sample .env
   
   # Edit .env and add your Azure AI Language credentials:
   # AZURE_AI_LANGUAGE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   # AZURE_AI_LANGUAGE_KEY=your_32_character_key_here
   ```
   
   **Option B: Using environment variables**
   ```bash
   export AZURE_AI_LANGUAGE_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
   export AZURE_AI_LANGUAGE_KEY="your-api-key"
   ```

### Test the PII Detection Module
```bash
cd tests
python test_pii_module.py
```

### Test the HTTP Function Endpoint
1. Start Azurite (in a separate terminal):
   ```bash
   azurite --location ./azurite --debug ./azurite/debug.log
   ```

2. Start the Functions host (in another terminal):
   ```bash
   func host start
   ```

3. Run the endpoint test:
   ```bash
   cd tests
   python test_function.py
   ```

## Test Data

Both tests use sample text containing common PII patterns:
- Personal names
- Email addresses  
- Phone numbers
- Social Security Numbers

## Expected Results

### PII Module Test
- Lists detected PII entities with categories and confidence scores
- Shows redacted text with `[REDACTED_CATEGORY]` placeholders

### Function Endpoint Test  
- Returns HTTP 200 with JSON response
- Contains `transcription` field with redacted text
- Saves cleaned transcript to Blob Storage as `TEST456_cleaned.txt`

## Troubleshooting

- **Import errors**: Make sure you're running from the `tests/` directory
- **Connection errors**: Ensure the Functions host is running on port 7071
- **PII detection failures**: Verify Azure AI Language credentials are configured
- **Storage errors**: Check that Azurite is running and connection string is correct