import requests
import json

# Test data
test_data = {
    "approved_emails": [
        {
            "to": "test@example.com",
            "name": "Test User",
            "subject": "Test Email - Fixed Version",
            "body": "This is a test email to verify the campaign schedule fix.",
            "company": "Test Company"
        }
    ],
    "campaign_name": "Test_Fixed_Campaign",
    "send_mode": "instantly"
}

try:
    response = requests.post(
        "http://localhost:8000/send-emails/",
        headers={"Content-Type": "application/json"},
        json=test_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nSuccess! Campaign details:")
        print(f"Total processed: {result.get('total_processed')}")
        print(f"Successful: {result.get('successful_sends')}")
        print(f"Failed: {result.get('failed_sends')}")
        print(f"Mode: {result.get('mode')}")
        if result.get('campaigns_created'):
            print(f"Campaign IDs: {result.get('campaigns_created')}")
    
except Exception as e:
    print(f"Error: {e}") 