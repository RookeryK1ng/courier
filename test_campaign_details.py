import requests
import json

campaign_id = "9b7afb03-38bf-42d7-9690-a5533eca9d56"
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"  # From the logs
base_url = "https://api.instantly.ai/api/v2"

try:
    # Get campaign details first
    print("🔍 Getting campaign details...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(
        f"{base_url}/campaigns/{campaign_id}",
        headers=headers
    )
    
    print(f"Campaign Status: {response.status_code}")
    if response.status_code == 200:
        campaign_data = response.json()
        print(f"Campaign Response: {json.dumps(campaign_data, indent=2)}")
        
        # Now try to activate it WITHOUT Content-Type header
        print("\n🚀 Trying to activate campaign...")
        activation_headers = {
            "Authorization": f"Bearer {api_key}"
            # No Content-Type header
        }
        activation_response = requests.post(
            f"{base_url}/campaigns/{campaign_id}/activate", 
            headers=activation_headers
        )
        
        print(f"Activation Status: {activation_response.status_code}")
        print(f"Activation Response: {activation_response.text}")
        
    else:
        print(f"Failed to get campaign: {response.text}")
    
except Exception as e:
    print(f"Error: {e}") 