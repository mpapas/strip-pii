"""
PII Detection and Redaction Module

This module provides functionality to detect and redact personally identifiable
information (PII) from text using Azure AI Language service.
"""

import logging
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def remove_pii_with_azure_ai(text: str) -> str:
    """Remove PII using Azure AI Language service.
    
    Uses Azure Cognitive Services Text Analytics to detect and redact
    personally identifiable information from the input text.
    
    Args:
        text (str): The input text to scan for PII
        
    Returns:
        str: The text with PII entities replaced by [REDACTED_<CATEGORY>] placeholders
        
    Raises:
        Exception: If Azure AI Language service is not configured or fails
    """
    if not text:
        return text
    
    logger = logging.getLogger("pii_detection.remove_pii_with_azure_ai")
    
    try:
        # Get Azure AI Language credentials from environment
        ai_endpoint = os.environ.get("AZURE_AI_LANGUAGE_ENDPOINT")
        ai_key = os.environ.get("AZURE_AI_LANGUAGE_KEY")
        
        if not ai_endpoint or not ai_key:
            raise Exception("Azure AI Language credentials not configured")
        
        # Initialize the Text Analytics client
        credential = AzureKeyCredential(ai_key)
        text_analytics_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
        
        # Use the PII detection feature
        documents = [text]
        response = text_analytics_client.recognize_pii_entities(documents, language="en")
        
        if not response or len(response) == 0:
            raise Exception("No response from Azure AI Language service")
        
        result = response[0]
        if result.is_error:
            raise Exception(f"Failed to process text with Azure AI Language service")
        
        # Build redacted text by replacing PII entities
        cleaned_text = text
        
        # Sort entities by offset in reverse order to preserve positions during replacement
        entities = sorted(result.entities, key=lambda x: x.offset, reverse=True)
        
        for entity in entities:
            start = entity.offset
            end = start + entity.length
            # Replace with a redaction placeholder that includes the entity category
            redaction = f"[REDACTED_{entity.category.upper()}]"
            cleaned_text = cleaned_text[:start] + redaction + cleaned_text[end:]
            logger.info(f"Redacted {entity.category} entity: {entity.text[:20]}...")
        
        logger.info(f"Successfully processed text with Azure AI Language. Found {len(entities)} PII entities.")
        logger.info(f"Cleaned text: {cleaned_text}")
        
        return cleaned_text
        
    except Exception as e:
        logger.exception(f"Failed to process text with Azure AI Language service: {str(e)}")
        return ""


def get_pii_entities(text: str) -> list:
    """Get PII entities from text without redacting (for analysis purposes).
    
    Args:
        text (str): The input text to scan for PII
        
    Returns:
        list: List of detected PII entities with metadata
        
    Raises:
        Exception: If Azure AI Language service is not configured or fails
    """
    if not text:
        return []
    
    logger = logging.getLogger("pii_detection.get_pii_entities")
    
    try:
        # Get Azure AI Language credentials from environment
        ai_endpoint = os.environ.get("AZURE_AI_LANGUAGE_ENDPOINT")
        ai_key = os.environ.get("AZURE_AI_LANGUAGE_KEY")
        
        if not ai_endpoint or not ai_key:
            raise Exception("Azure AI Language credentials not configured")
        
        # Initialize the Text Analytics client
        credential = AzureKeyCredential(ai_key)
        text_analytics_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
        
        # Use the PII detection feature
        documents = [text]
        response = text_analytics_client.recognize_pii_entities(documents, language="en")
        
        if not response or len(response) == 0:
            raise Exception("No response from Azure AI Language service")
        
        result = response[0]
        if result.is_error:
            raise Exception(f"Failed to process text with Azure AI Language service")
        
        # Return entity metadata
        entities = []
        for entity in result.entities:
            entities.append({
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
                "confidence_score": entity.confidence_score,
                "offset": entity.offset,
                "length": entity.length
            })
        
        logger.info(f"Found {len(entities)} PII entities in text")
        return entities
        
    except Exception as e:
        logger.exception(f"Failed to analyze text with Azure AI Language service: {str(e)}")
        raise