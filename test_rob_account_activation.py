import requests
import json

# Test Rob's account for activation
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
base_url = "https://api.instantly.ai/api/v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🧪 TESTING ROB'S ACCOUNT FOR ACTIVATION")
print("="*60)

# Use Rob's email account
rob_email = "rob@biscred.ai"

# Create test campaign with Rob's account
campaign_data = {
    "name": "ROB_ACTIVATION_TEST",
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
                "timezone": "America/Chicago"
            }
        ]
    },
    "email_list": [rob_email],  # Rob's email account
    "sequences": [
        {
            "steps": [
                {
                    "subject": "Partnership Opportunity with {{company_name}}",
                    "body": "Hi {{first_name}}, this is Rob from BiscRed. I wanted to reach out about a potential partnership with {{company_name}}.",
                    "day": 1,
                    "type": "email",
                    "delay": 0,
                    "variants": [
                        {
                            "subject": "Partnership Opportunity with {{company_name}}",
                            "body": "Hi {{first_name}}, this is Rob from BiscRed. I wanted to reach out about a potential partnership with {{company_name}}."
                        }
                    ]
                }
            ]
        }
    ]
}

try:
    print(f"📤 Creating campaign with Rob's account: {rob_email}")
    
    # Create campaign
    response = requests.post(f"{base_url}/campaigns", headers=headers, json=campaign_data)
    
    if response.status_code == 200:
        campaign_data_response = response.json()
        campaign_id = campaign_data_response.get('id')
        print(f"✅ Campaign created successfully: {campaign_id}")
        
        # Add test lead
        print(f"👤 Adding test lead...")
        test_lead = {
            "email": "test@robtest.com",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "campaign": campaign_id
        }
        
        lead_response = requests.post(f"{base_url}/leads", headers=headers, json=test_lead)
        if lead_response.status_code == 200:
            print(f"✅ Test lead added successfully")
            
            # Test activation with Rob's account
            print(f"🚀 Testing activation with Rob's account...")
            activation_response = requests.post(
                f"{base_url}/campaigns/{campaign_id}/activate", 
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            print(f"Activation status: {activation_response.status_code}")
            if activation_response.status_code == 200:
                print(f"🎉 ROB ACCOUNT ACTIVATION SUCCESSFUL!")
                print(f"✅ Campaign {campaign_id} is now ACTIVE with Rob's account")
                
                # Verify campaign status
                status_response = requests.get(f"{base_url}/campaigns/{campaign_id}", headers=headers)
                if status_response.status_code == 200:
                    campaign_status = status_response.json()
                    print(f"📊 Campaign Status: {campaign_status.get('status')}")
                    print(f"📧 Email Account: {campaign_status.get('email_list')}")
                    
            else:
                print(f"❌ Activation failed: {activation_response.status_code}")
                print(f"Response: {activation_response.text}")
                
        else:
            print(f"❌ Failed to add lead: {lead_response.text}")
    else:
        print(f"❌ Campaign creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Test error: {e}")

print(f"\n" + "="*60)
print(f"🎯 ROB ACCOUNT TEST COMPLETE")
print("="*60) 