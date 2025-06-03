import requests
import json

# Direct API test: Create and activate campaign
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
base_url = "https://api.instantly.ai/api/v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🚀 DIRECT API TEST: CREATE AND ACTIVATE CAMPAIGN")
print("="*60)

# Step 1: Create campaign with proper structure
print("📋 STEP 1: Creating campaign with complete structure...")

campaign_data = {
    "name": "DIRECT_API_ACTIVATION_TEST",
    "campaign_schedule": {
        "schedules": [
            {
                "name": "Business Hours",
                "timing": {
                    "from": "09:00",
                    "to": "17:00"
                },
                "days": {
                    "0": False,  # Sunday
                    "1": True,   # Monday  
                    "2": True,   # Tuesday
                    "3": True,   # Wednesday
                    "4": True,   # Thursday
                    "5": True,   # Friday
                    "6": False   # Saturday
                },
                "timezone": "America/Chicago"  # Valid timezone
            }
        ]
    },
    "email_list": ["rob@biscred.ai"],  # Rob's verified account
    "sequences": [
        {
            "steps": [
                {
                    "subject": "Direct API Test - Partnership with {{company_name}}",
                    "body": "Hi {{first_name}}, this is Rob from BiscRed. I'm reaching out via direct API to test our campaign activation. Would love to discuss a partnership with {{company_name}}.",
                    "day": 1,        # Required field
                    "type": "email", # Required field  
                    "delay": 0,      # Required field
                    "variants": [    # Required field
                        {
                            "subject": "Direct API Test - Partnership with {{company_name}}",
                            "body": "Hi {{first_name}}, this is Rob from BiscRed. I'm reaching out via direct API to test our campaign activation. Would love to discuss a partnership with {{company_name}}."
                        }
                    ]
                }
            ]
        }
    ]
}

print(f"📤 Campaign structure:")
print(f"   Name: {campaign_data['name']}")
print(f"   Email account: {campaign_data['email_list'][0]}")
print(f"   Timezone: {campaign_data['campaign_schedule']['schedules'][0]['timezone']}")
print(f"   Has all required fields: day, type, delay, variants ✅")

try:
    # Create the campaign
    create_response = requests.post(f"{base_url}/campaigns", headers=headers, json=campaign_data)
    
    if create_response.status_code == 200:
        campaign_result = create_response.json()
        campaign_id = campaign_result.get('id')
        print(f"✅ Campaign created successfully!")
        print(f"   Campaign ID: {campaign_id}")
        print(f"   Status: {campaign_result.get('status')} (0=draft, 1=active)")
        
        # Step 2: Add a test lead
        print(f"\n👤 STEP 2: Adding test lead to campaign...")
        
        test_lead = {
            "email": "test@directapitest.com",
            "first_name": "Direct",
            "last_name": "APITest",
            "company_name": "API Test Company",
            "campaign": campaign_id
        }
        
        lead_response = requests.post(f"{base_url}/leads", headers=headers, json=test_lead)
        
        if lead_response.status_code == 200:
            lead_result = lead_response.json()
            print(f"✅ Test lead added successfully!")
            print(f"   Lead ID: {lead_result.get('id')}")
            
            # Step 3: Attempt activation
            print(f"\n🚀 STEP 3: Attempting campaign activation...")
            
            activation_response = requests.post(
                f"{base_url}/campaigns/{campaign_id}/activate",
                headers={"Authorization": f"Bearer {api_key}"}  # Just auth header for activation
            )
            
            print(f"📊 ACTIVATION RESULTS:")
            print(f"   Status Code: {activation_response.status_code}")
            print(f"   Response: {activation_response.text}")
            
            if activation_response.status_code == 200:
                activation_result = activation_response.json()
                print(f"\n🎉 ACTIVATION SUCCESSFUL!")
                print(f"   Campaign Status: {activation_result.get('status')}")
                print(f"   Campaign ID: {activation_result.get('id')}")
                
                # Verify the campaign is now active
                print(f"\n📋 STEP 4: Verifying campaign status...")
                status_response = requests.get(f"{base_url}/campaigns/{campaign_id}", headers=headers)
                
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    final_status = status_result.get('status')
                    print(f"✅ Campaign verification:")
                    print(f"   Final Status: {final_status} ({'ACTIVE' if final_status == 1 else 'DRAFT'})")
                    print(f"   Email Account: {status_result.get('email_list')}")
                    
                    if final_status == 1:
                        print(f"\n🎉 COMPLETE SUCCESS!")
                        print(f"✅ Campaign created with proper structure")
                        print(f"✅ Lead added successfully") 
                        print(f"✅ Campaign activated via API")
                        print(f"✅ Campaign is now SENDING emails!")
                        print(f"✅ Check Instantly dashboard for active campaign")
                    else:
                        print(f"\n⚠️ Activation response was 200 but status still shows draft")
                        
            else:
                print(f"\n❌ ACTIVATION FAILED")
                print(f"   Error Code: {activation_response.status_code}")
                print(f"   Error Details: {activation_response.text}")
                
                # Analyze the specific error
                if activation_response.status_code == 400:
                    print(f"\n🔍 400 BAD REQUEST ANALYSIS:")
                    error_text = activation_response.text.lower()
                    if "email" in error_text:
                        print(f"   - Issue might be with email account configuration")
                    if "sequence" in error_text:
                        print(f"   - Issue might be with sequence structure")
                    if "schedule" in error_text:
                        print(f"   - Issue might be with campaign schedule")
                        
        else:
            print(f"❌ Failed to add test lead: {lead_response.status_code}")
            print(f"   Response: {lead_response.text}")
            
    else:
        print(f"❌ Campaign creation failed: {create_response.status_code}")
        print(f"   Response: {create_response.text}")
        
except Exception as e:
    print(f"❌ Direct API test error: {e}")

print(f"\n" + "="*60)
print(f"🎯 DIRECT API TEST COMPLETE")
print("="*60) 