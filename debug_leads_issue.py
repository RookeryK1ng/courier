import requests
import json

# Test the lead addition issue directly
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"
base_url = "https://api.instantly.ai/api/v2"

print("🔍 DEBUGGING WHY LEADS AREN'T SHOWING UP")
print("="*60)

# First, let's check what campaigns exist
try:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("📋 STEP 1: Getting all campaigns...")
    campaigns_response = requests.get(
        f"{base_url}/campaigns",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    print(f"Campaigns response: {campaigns_response.status_code}")
    if campaigns_response.status_code == 200:
        campaigns = campaigns_response.json()
        print(f"Found {len(campaigns.get('items', []))} campaigns")
        
        # Show recent campaigns
        recent_campaigns = campaigns.get('items', [])[:5]
        for campaign in recent_campaigns:
            print(f"  - {campaign.get('name')} (ID: {campaign.get('id')}) - Status: {campaign.get('status')}")
    
    # Use the most recent campaign from our tests
    test_campaign_id = "1cd17813-4d00-4a1e-809e-5e99f7350ba8"
    
    print(f"\n📋 STEP 2: Checking specific campaign: {test_campaign_id}")
    campaign_response = requests.get(
        f"{base_url}/campaigns/{test_campaign_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    print(f"Campaign status: {campaign_response.status_code}")
    if campaign_response.status_code == 200:
        campaign_data = campaign_response.json()
        print(f"Campaign name: {campaign_data.get('name')}")
        print(f"Campaign status: {campaign_data.get('status')}")
        print(f"Email list: {campaign_data.get('email_list')}")
    else:
        print(f"Campaign error: {campaign_response.text}")
    
    print(f"\n📋 STEP 3: Getting leads for campaign {test_campaign_id}")
    
    # Try different ways to get campaign leads
    leads_endpoints = [
        f"/campaigns/{test_campaign_id}/leads",
        f"/leads?campaign={test_campaign_id}",
        f"/leads"
    ]
    
    for endpoint in leads_endpoints:
        print(f"\nTrying endpoint: {endpoint}")
        leads_response = requests.get(
            f"{base_url}{endpoint}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        print(f"Status: {leads_response.status_code}")
        if leads_response.status_code == 200:
            leads_data = leads_response.json()
            
            if endpoint == "/leads":
                # Filter for our campaign
                all_leads = leads_data.get('items', [])
                campaign_leads = [lead for lead in all_leads if lead.get('campaign') == test_campaign_id]
                print(f"Total leads in system: {len(all_leads)}")
                print(f"Leads for our campaign: {len(campaign_leads)}")
                
                if campaign_leads:
                    for lead in campaign_leads:
                        print(f"  - Email: {lead.get('email')}")
                        print(f"  - Lead ID: {lead.get('id')}")
                        print(f"  - Status: {lead.get('status')}")
                        print(f"  - Campaign: {lead.get('campaign')}")
                else:
                    print("  ❌ NO LEADS FOUND FOR THIS CAMPAIGN!")
                    
                    # Check if test@example.com exists anywhere
                    test_leads = [lead for lead in all_leads if lead.get('email') == 'test@example.com']
                    if test_leads:
                        print(f"  ⚠️ test@example.com found in {len(test_leads)} other campaigns:")
                        for lead in test_leads:
                            print(f"    - Campaign: {lead.get('campaign')}")
                            print(f"    - Lead ID: {lead.get('id')}")
                break
            else:
                print(f"Response: {leads_data}")
        else:
            print(f"Error: {leads_response.text}")
    
    print(f"\n📋 STEP 4: Testing lead creation directly")
    
    # Try to add a test lead directly to see what happens
    test_lead = {
        "email": "debug.test@example.com",
        "first_name": "Debug",
        "last_name": "Test",
        "campaign": test_campaign_id,
        "skip_if_in_workspace": True,
        "skip_if_in_campaign": False,
        "skip_if_in_list": False
    }
    
    print(f"Adding test lead: {test_lead}")
    
    add_response = requests.post(
        f"{base_url}/leads",
        headers=headers,
        json=test_lead
    )
    
    print(f"Add lead status: {add_response.status_code}")
    print(f"Add lead response: {add_response.text}")
    
    if add_response.status_code == 200:
        print("✅ Lead addition succeeded")
        
        # Now check if it really shows up
        print("\nVerifying lead was actually added...")
        verify_response = requests.get(
            f"{base_url}/leads",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if verify_response.status_code == 200:
            all_leads = verify_response.json().get('items', [])
            debug_leads = [lead for lead in all_leads if lead.get('email') == 'debug.test@example.com']
            
            if debug_leads:
                print(f"✅ FOUND DEBUG LEAD: {debug_leads[0]}")
            else:
                print("❌ DEBUG LEAD NOT FOUND - LEADS ARE NOT BEING SAVED!")
    
except Exception as e:
    print(f"Error: {e}")

print(f"\n" + "="*60)
print("🏆 DIAGNOSIS COMPLETE")
print("="*60) 