import requests
import json

# Test different approaches to adding leads
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"
base_url = "https://api.instantly.ai/api/v2"

# Use the most recent campaign ID from Duncan's test
campaign_id = "2f82665a-2d18-4c50-8c44-a5849699edd5"

print("🔍 DEBUGGING LEAD ADDITION ISSUE")
print("="*60)

try:
    # First, let's try a simpler lead addition approach
    print("\n📋 APPROACH 1: Basic lead data (minimal fields)")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Minimal lead data
    basic_lead_data = {
        "email": "duncan.stockdale@gmail.com",
        "first_name": "Duncan",
        "last_name": "Stockdale",
        "campaign": campaign_id
    }
    
    print(f"Lead data: {basic_lead_data}")
    
    response = requests.post(
        f"{base_url}/leads",
        headers=headers,
        json=basic_lead_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code != 200:
        print("\n📋 APPROACH 2: Trying different lead endpoint")
        
        # Try alternative endpoint structure
        alt_response = requests.post(
            f"{base_url}/campaigns/{campaign_id}/leads",
            headers=headers,
            json=basic_lead_data
        )
        
        print(f"Alternative endpoint status: {alt_response.status_code}")
        print(f"Alternative response: {alt_response.text}")
        
        if alt_response.status_code != 200:
            print("\n📋 APPROACH 3: Trying bulk lead addition")
            
            # Try bulk lead addition
            bulk_data = {
                "leads": [basic_lead_data]
            }
            
            bulk_response = requests.post(
                f"{base_url}/leads/list",
                headers=headers,
                json=bulk_data
            )
            
            print(f"Bulk endpoint status: {bulk_response.status_code}")
            print(f"Bulk response: {bulk_response.text}")
            
            if bulk_response.status_code != 200:
                print("\n📋 APPROACH 4: Testing with different email")
                
                # Try with a completely different email
                test_lead_data = {
                    "email": "test.lead@example.com",
                    "first_name": "Test",
                    "last_name": "Lead",
                    "campaign": campaign_id
                }
                
                test_response = requests.post(
                    f"{base_url}/leads",
                    headers=headers,
                    json=test_lead_data
                )
                
                print(f"Test email status: {test_response.status_code}")
                print(f"Test email response: {test_response.text}")
    
    # Let's also check what campaigns exist and their structure
    print(f"\n🔍 CHECKING CAMPAIGN DETAILS")
    campaign_response = requests.get(
        f"{base_url}/campaigns/{campaign_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    print(f"Campaign status: {campaign_response.status_code}")
    if campaign_response.status_code == 200:
        campaign_data = campaign_response.json()
        print(f"Campaign status: {campaign_data.get('status')}")
        print(f"Campaign name: {campaign_data.get('name')}")
        print(f"Email list: {campaign_data.get('email_list')}")
    else:
        print(f"Campaign error: {campaign_response.text}")
    
except Exception as e:
    print(f"Error: {e}") 