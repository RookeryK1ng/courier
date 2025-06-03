import requests
import json

# Test with correct email account and timezone
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
base_url = "https://api.instantly.ai/api/v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔧 TESTING CORRECTED CAMPAIGN ACTIVATION")
print("="*60)

# Use a valid email account from our workspace
valid_email = "alex@biscred.ai"  # First valid email from diagnosis

# Create campaign with corrected structure
corrected_campaign_data = {
    "name": "CORRECTED_ACTIVATION_TEST",
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
                "timezone": "America/Chicago"  # Use valid timezone
            }
        ]
    },
    "email_list": [valid_email],  # Use validated email
    "sequences": [
        {
            "steps": [
                {
                    "subject": "Partnership Opportunity with {{company_name}}",
                    "body": "Hi {{first_name}}, I hope this message finds you well. I wanted to reach out regarding a potential business partnership opportunity with {{company_name}}.",
                    "day": 1,  # Required field for activation!
                    "type": "email",  # Required field - was missing!
                    "delay": 0,  # Required field - delay in days
                    "variants": [  # Required field - email variants
                        {
                            "subject": "Partnership Opportunity with {{company_name}}",
                            "body": "Hi {{first_name}}, I hope this message finds you well. I wanted to reach out regarding a potential business partnership opportunity with {{company_name}}."
                        }
                    ]
                }
            ]
        }
    ]
}

print(f"📤 Creating campaign with corrected parameters:")
print(f"   Email account: {valid_email}")
print(f"   Timezone: America/Chicago")
print(f"   Sequence has 'day' field: ✅")

try:
    # Step 1: Create campaign
    response = requests.post(f"{base_url}/campaigns", headers=headers, json=corrected_campaign_data)
    
    if response.status_code == 200:
        campaign_data = response.json()
        campaign_id = campaign_data.get('id')
        print(f"✅ Campaign created successfully: {campaign_id}")
        
        # Step 2: Add a test lead
        print(f"\n👤 Adding test lead to campaign...")
        test_lead = {
            "email": "test@correctedtest.com",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "campaign": campaign_id
        }
        
        lead_response = requests.post(f"{base_url}/leads", headers=headers, json=test_lead)
        if lead_response.status_code == 200:
            print(f"✅ Test lead added successfully")
            
            # Step 3: Try activation - THIS SHOULD WORK NOW!
            print(f"\n🚀 Attempting campaign activation...")
            activation_response = requests.post(
                f"{base_url}/campaigns/{campaign_id}/activate", 
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            print(f"Activation status: {activation_response.status_code}")
            if activation_response.status_code == 200:
                print(f"🎉 ACTIVATION SUCCESSFUL!")
                activation_data = activation_response.json()
                print(f"Response: {activation_data}")
                
                # Verify campaign is active
                status_response = requests.get(f"{base_url}/campaigns/{campaign_id}", headers=headers)
                if status_response.status_code == 200:
                    campaign_status = status_response.json()
                    print(f"\n📊 Campaign Status After Activation:")
                    print(f"   Status: {campaign_status.get('status', 'Unknown')}")
                    print(f"   Active: {campaign_status.get('is_active', 'Unknown')}")
                    
            else:
                print(f"❌ Activation still failed: {activation_response.status_code}")
                print(f"Response: {activation_response.text}")
                
                # Additional debugging - check what fields might still be missing
                print(f"\n🔍 Campaign details for debugging:")
                debug_response = requests.get(f"{base_url}/campaigns/{campaign_id}", headers=headers)
                if debug_response.status_code == 200:
                    debug_data = debug_response.json()
                    print(f"Campaign data: {json.dumps(debug_data, indent=2)}")
                
        else:
            print(f"❌ Failed to add test lead: {lead_response.status_code}")
            print(f"Response: {lead_response.text}")
    else:
        print(f"❌ Campaign creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n" + "="*60)
print(f"🎯 If activation succeeds, we can update the main system!")
print("="*60) 