import requests
import json

# Test the bulk leads endpoint directly
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"
base_url = "https://api.instantly.ai/api/v2"

# Use a recent campaign ID
campaign_id = "df067f19-9d26-4e8c-b10f-5203e07079fe"

print("🔍 DIRECT TEST OF BULK LEADS ENDPOINT")
print("="*60)

# Test 1: Simple bulk addition
bulk_data = {
    "leads": [
        {
            "email": "duncan.stockdale@gmail.com",
            "first_name": "Duncan",
            "last_name": "Stockdale", 
            "campaign": campaign_id
        }
    ]
}

print(f"Campaign ID: {campaign_id}")
print(f"Bulk data: {bulk_data}")

try:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"\n📤 SENDING TO: {base_url}/leads/list")
    
    response = requests.post(
        f"{base_url}/leads/list",
        headers=headers,
        json=bulk_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        
        # Check if we have items
        if 'items' in result:
            items = result['items']
            print(f"\n✅ Items found: {len(items)}")
            
            # Look for our campaign
            campaign_items = [item for item in items if item.get('campaign') == campaign_id]
            print(f"✅ Items for our campaign: {len(campaign_items)}")
            
            if campaign_items:
                for item in campaign_items:
                    print(f"   - Email: {item.get('email')}")
                    print(f"   - Lead ID: {item.get('id')}")
                    print(f"   - Campaign: {item.get('campaign')}")
                    print(f"   - Status: {item.get('status')}")
            else:
                print("⚠️ No items found for our campaign")
                
                # Check if Duncan's email exists elsewhere
                duncan_items = [item for item in items if item.get('email') == 'duncan.stockdale@gmail.com']
                if duncan_items:
                    print(f"⚠️ Duncan's email found in {len(duncan_items)} other campaigns:")
                    for item in duncan_items:
                        print(f"   - Campaign: {item.get('campaign')}")
                        print(f"   - Lead ID: {item.get('id')}")
                        print(f"   - Status: {item.get('status')}")
        else:
            print("❌ No 'items' in response")
    else:
        print(f"❌ Request failed: {response.text}")
        
    # Test 2: Let's try to get campaign leads directly
    print(f"\n🔍 CHECKING CAMPAIGN LEADS DIRECTLY...")
    leads_response = requests.get(
        f"{base_url}/campaigns/{campaign_id}/leads",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    print(f"Campaign leads status: {leads_response.status_code}")
    if leads_response.status_code == 200:
        leads_result = leads_response.json()
        print(f"Campaign leads: {leads_result}")
    else:
        print(f"Campaign leads error: {leads_response.text}")
        
except Exception as e:
    print(f"Error: {e}") 