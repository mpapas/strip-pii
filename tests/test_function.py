#!/usr/bin/env python3
"""
Test script for the processTranscript function.
Tests Azure AI Language integration with the HTTP endpoint.
"""

import json
import requests
import sys
import os

# Add parent directory to path so we can import modules  
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Sample test data - multiple payloads to test different scenarios
test_payloads = [
    {
        "id": "TEST456",
        "transcription": "Hi, my name is John Doe and my email is john.doe@example.com. My phone number is +1-555-123-4567 and my SSN is 123-45-6789."
    },
    {
        "id": "TEST456",
        "transcription": "Hi, my name is John Doe and my email is john.doe@example.com. My phone number is +1 555 123-4567 and my SSN is 123-45-6789."
    },
    {
        "id": "CALL789",
        "transcription": "Good morning, this is Sarah Johnson from ABC Corp. You can reach me at sarah.johnson@abccorp.com or call me at (555) 987-6543."
    },
    {
        "id": "SIMPLE001", 
        "transcription": "This is a simple transcript with no personal information to redact."
    },
    {
        "id": "COMPLEX123",
        "transcription": "My name is Dr. Michael Smith, license number MD-98765. Please send the medical records to 123 Main Street, Anytown, CA 90210. Patient DOB: 01/15/1985. Insurance ID: ABC123456789."
    },
    {
        "id": "ACCIDENT2022",
        "transcription": "Mateo Gomez, 28-year-old man, suffered a car accident driving near his home on Hollywood Boulevard on August 17th, 2022, and was admitted to Contoso General Hospital in Los Angeles California at 7:45 PM. The patient showed signs of chest trauma indicating possible rib fracture and had difficulty breathing. A chest CT scan and AP X-ray were performed to determine the damage to ribs and lungs. Results showed a pseudoaneurysm of the thoracic aorta with minor fracture to the first and third right ribs. Patient was kept in the ICU where treatment was initiated. A Stent was surgically placed to stabilize the hemorrhage until the blood oxygen level reached 95 percent. The patient was discharged on September 1st, 2022, under the supervision of his caretaker Nickolaus Schulz, passport number: B12345678."
    }
]

def test_function():
    """Test the processTranscript function locally with multiple payloads."""
    
    url = "http://localhost:7071/api/processTranscript"
    headers = {"Content-Type": "application/json"}
    
    print("Testing processTranscript function with multiple payloads...")
    print(f"URL: {url}")
    print(f"Total test cases: {len(test_payloads)}")
    print("=" * 70)
    
    success_count = 0
    total_count = len(test_payloads)
    
    for i, test_payload in enumerate(test_payloads, 1):
        print(f"\n📋 Test Case {i}/{total_count}: {test_payload['id']}")
        print(f"Input: {test_payload['transcription']}")
        print("-" * 50)
        
        try:
            response = requests.post(url, json=test_payload, headers=headers, timeout=30)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS!")
                print(f"Output: {result.get('transcription', 'N/A')}")
                success_count += 1
            else:
                print("❌ ERROR!")
                try:
                    error_details = response.json()
                    print(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    print(f"Raw response: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR!")
            print("Make sure the Azure Functions host is running:")
            print("  func host start")
            break  # No point continuing if we can't connect
            
        except requests.exceptions.Timeout:
            print("⏱️ TIMEOUT!")
            print("The request took too long. Check function logs.")
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 TEST SUMMARY: {success_count}/{total_count} tests passed")
    if success_count == total_count:
        print("🎉 All tests completed successfully!")
    else:
        print(f"⚠️  {total_count - success_count} test(s) failed")
    print("=" * 70)

if __name__ == "__main__":
    test_function()