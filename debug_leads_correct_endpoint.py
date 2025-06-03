import requests
import json

# Test the lead retrieval using the CORRECT endpoint
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"
base_url = "https://api.instantly.ai/api/v2"

print("🔍 DEBUGGING LEADS WITH CORRECT API ENDPOINT")
print("="*60)

# Use the most recent campaign from our tests
test_campaign_id = "1cd17813-4d00-4a1e-809e-5e99f7350ba8"

try:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"📋 STEP 1: Checking campaign {test_campaign_id}")
    campaign_response = requests.get(
        f"{base_url}/campaigns/{test_campaign_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    print(f"Campaign status: {campaign_response.status_code}")
    if campaign_response.status_code == 200:
        campaign_data = campaign_response.json()
        print(f"Campaign name: {campaign_data.get('name')}")
        print(f"Campaign status: {campaign_data.get('status')}")
        
    print(f"\n📋 STEP 2: Getting ALL leads using correct endpoint")
    
    # Use the CORRECT endpoint: POST /api/v2/leads/list
    leads_request = {
        "limit": 100  # Get up to 100 leads
    }
    
    print(f"Using POST {base_url}/leads/list")
    print(f"Request body: {leads_request}")
    
    leads_response = requests.post(
        f"{base_url}/leads/list",
        headers=headers,
        json=leads_request
    )
    
    print(f"Leads response status: {leads_response.status_code}")
    print(f"Leads response: {leads_response.text}")
    
    if leads_response.status_code == 200:
        leads_data = leads_response.json()
        all_leads = leads_data.get('items', [])
        
        print(f"\n✅ FOUND {len(all_leads)} TOTAL LEADS")
        
        # Filter for our specific campaign
        campaign_leads = [lead for lead in all_leads if lead.get('campaign') == test_campaign_id]
        print(f"✅ LEADS FOR OUR CAMPAIGN: {len(campaign_leads)}")
        
        if campaign_leads:
            print(f"\n🎯 CAMPAIGN LEADS DETAILS:")
            for lead in campaign_leads:
                print(f"  - Email: {lead.get('email')}")
                print(f"  - Lead ID: {lead.get('id')}")
                print(f"  - Name: {lead.get('first_name')} {lead.get('last_name')}")
                print(f"  - Campaign: {lead.get('campaign')}")
                print(f"  - Status: {lead.get('status')}")
                print(f"  - Created: {lead.get('timestamp_created')}")
                print(f"  ---")
        else:
            print(f"\n❌ NO LEADS FOUND FOR CAMPAIGN {test_campaign_id}")
            
            # Check if our test emails exist anywhere
            test_emails = ['test@example.com', 'debug.test@example.com']
            for test_email in test_emails:
                matching_leads = [lead for lead in all_leads if lead.get('email') == test_email]
                if matching_leads:
                    print(f"\n⚠️ {test_email} found in {len(matching_leads)} other locations:")
                    for lead in matching_leads:
                        print(f"  - Campaign: {lead.get('campaign')}")
                        print(f"  - Lead ID: {lead.get('id')}")
                        print(f"  - Status: {lead.get('status')}")
    
    print(f"\n📋 STEP 3: Testing with campaign filter")
    
    # Try filtering specifically by campaign
    campaign_filter_request = {
        "campaign": test_campaign_id,
        "limit": 50
    }
    
    print(f"Filtering by campaign: {campaign_filter_request}")
    
    filtered_response = requests.post(
        f"{base_url}/leads/list",
        headers=headers,
        json=campaign_filter_request
    )
    
    print(f"Filtered response status: {filtered_response.status_code}")
    if filtered_response.status_code == 200:
        filtered_data = filtered_response.json()
        filtered_leads = filtered_data.get('items', [])
        print(f"✅ FILTERED RESULTS: {len(filtered_leads)} leads")
        
        if filtered_leads:
            print(f"🎯 FILTERED LEAD DETAILS:")
            for lead in filtered_leads:
                print(f"  - Email: {lead.get('email')}")
                print(f"  - Lead ID: {lead.get('id')}")
                print(f"  - Campaign: {lead.get('campaign')}")
        else:
            print(f"❌ NO LEADS FOUND WITH CAMPAIGN FILTER")
    else:
        print(f"Filtered response error: {filtered_response.text}")

except Exception as e:
    print(f"Error: {e}")

print(f"\n" + "="*60)
print("🏆 DIAGNOSIS COMPLETE")
print("="*60) 