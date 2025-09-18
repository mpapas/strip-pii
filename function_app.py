import azure.functions as func
import logging
import os
import json
from azure.storage.blob import BlobServiceClient, ContentSettings
from pii_detection import remove_pii_with_azure_ai

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="processTranscript", methods=["POST"])  # POST only
def processTranscript(req: func.HttpRequest) -> func.HttpResponse:
    logger = logging.getLogger("processTranscript")
    logger.info("Received request to process transcript")

    if req.method != "POST":
        return func.HttpResponse(
            json.dumps({"error": "Method not allowed. Use POST."}),
            status_code=405,
            mimetype="application/json",
            headers={"Allow": "POST"},
        )

    try:
        payload = req.get_json()
    except ValueError:
        logger.warning("Invalid JSON payload")
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON payload"}),
            status_code=400,
            mimetype="application/json",
        )

    # Validate required fields
    id_value = payload.get("id")
    transcription = payload.get("transcription")
    if not id_value or not isinstance(id_value, str):
        return func.HttpResponse(
            json.dumps({"error": "Field 'id' is required and must be a string"}),
            status_code=400,
            mimetype="application/json",
        )
    if transcription is None or not isinstance(transcription, str):
        return func.HttpResponse(
            json.dumps({"error": "Field 'transcription' is required and must be a string"}),
            status_code=400,
            mimetype="application/json",
        )

    # PII removal using Azure AI Language
    cleaned_text = remove_pii_with_azure_ai(transcription)
    if not cleaned_text:
        # raise an error if PII removal failed
        return func.HttpResponse(   
            json.dumps({"error": "Failed to remove PII from transcription"}),
            status_code=500,
            mimetype="application/json",
        )

    # Persist to Azure Blob Storage
    container_name = "cleaned-transcriptions"
    blob_name = f"{id_value}_cleaned.txt"
    try:
        conn_str = os.environ.get("AzureWebJobsStorage") or os.environ.get(
            "AZURE_STORAGE_CONNECTION_STRING"
        )
        if not conn_str:
            logger.error("Storage connection string is not configured")
            return func.HttpResponse(
                json.dumps({
                    "error": "Storage connection string not configured. Set 'AzureWebJobsStorage' in settings."
                }),
                status_code=500,
                mimetype="application/json",
            )

        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container_name)
        # Create container if it doesn't exist
        try:
            container_client.create_container()
            logger.info("Created container '%s'", container_name)
        except Exception as e:
            # If container exists, ignore specific error codes; otherwise, log and continue
            # The SDK raises ResourceExistsError for existing containers which is fine to ignore
            if getattr(e, "error_code", "").lower() != "containeralreadyexists":
                logger.debug("Container create exception detail: %s", str(e))
        content_settings = ContentSettings(content_type="text/plain; charset=utf-8")
        container_client.upload_blob(
            name=blob_name,
            data=cleaned_text.encode("utf-8"),
            overwrite=True,
            content_settings=content_settings,
        )
        logger.info("Uploaded cleaned transcript to blob '%s/%s'", container_name, blob_name)
    except Exception as e:
        logger.exception("Failed to upload cleaned transcript to Blob Storage")
        return func.HttpResponse(
            json.dumps({"error": "Failed to save cleaned transcript"}),
            status_code=500,
            mimetype="application/json",
        )

    logger.info(f"Stored cleaned transcription for id {id_value} in blob storage")

    # Success response
    return func.HttpResponse(
        json.dumps({"transcription": cleaned_text}),
        status_code=200,
        mimetype="application/json",
    )

