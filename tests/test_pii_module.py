#!/usr/bin/env python3
"""
Test script for the PII detection module.
Tests the standalone pii_detection module functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path so we can import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from pii_detection import remove_pii_with_azure_ai, get_pii_entities

# Sample test data with PII
test_text = "Hi, my name is John Doe and my email is john.doe@example.com. My phone number is +1-555-123-4567."

def test_pii_detection():
    """Test the PII detection module."""
    
    print("Testing PII Detection Module...")
    print(f"Input text: {test_text}")
    print("-" * 60)
    
    # Check if Azure AI Language is configured
    ai_endpoint = os.environ.get("AZURE_AI_LANGUAGE_ENDPOINT")
    ai_key = os.environ.get("AZURE_AI_LANGUAGE_KEY")
    
    if not ai_endpoint or not ai_key:
        print("❌ Azure AI Language not configured")
        print("Please set AZURE_AI_LANGUAGE_ENDPOINT and AZURE_AI_LANGUAGE_KEY in:")
        print("  1. Environment variables, OR")
        print("  2. .env file in the project root, OR") 
        print("  3. local.settings.json for the function app")
        print("\nTo create .env file, copy .env.sample and fill in your values:")
        print("  cp .env.sample .env")
        return
    
    try:
        # Test PII removal
        print("🔍 Testing PII removal...")
        cleaned_text = remove_pii_with_azure_ai(test_text)
        
        if cleaned_text:
            print("✅ PII removal successful!")
            print(f"Cleaned text: {cleaned_text}")
        else:
            print("❌ PII removal failed (returned empty string)")
            return
            
        print("-" * 60)
        
        # Test PII entity extraction
        print("🔍 Testing PII entity extraction...")
        entities = get_pii_entities(test_text)
        
        if entities:
            print(f"✅ Found {len(entities)} PII entities:")
            for i, entity in enumerate(entities, 1):
                print(f"  {i}. {entity['category']} ({entity['subcategory']}): '{entity['text'][:20]}...' (confidence: {entity['confidence_score']:.2f})")
        else:
            print("ℹ️ No PII entities detected in the text")
            
    except Exception as e:
        print(f"❌ Error testing PII detection: {e}")

if __name__ == "__main__":
    test_pii_detection()