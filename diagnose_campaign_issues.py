import requests
import json

# Test campaign structure and email account validation
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
workspace_id = "9a28e3f9-30ce-4c1f-b85a-53e5d893a4a3"
email_account_id = "tim@biscred.com"
base_url = "https://api.instantly.ai/api/v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔍 DIAGNOSING CAMPAIGN ACTIVATION ISSUES")
print("="*60)

# Step 1: Validate email account
print("📧 STEP 1: Validating Email Account")
try:
    response = requests.get(f"{base_url}/accounts", headers=headers)
    if response.status_code == 200:
        accounts = response.json()
        print(f"✅ Found {len(accounts.get('items', []))} email accounts")
        
        valid_emails = []
        for account in accounts.get('items', []):
            email = account.get('email')
            status = account.get('status')
            setup_pending = account.get('setup_pending')
            print(f"   Email: {email}")
            print(f"   Status: {status}")
            print(f"   Setup Pending: {setup_pending}")
            
            if not setup_pending and status == 1:  # Active status
                valid_emails.append(email)
                
        print(f"✅ Valid email accounts: {valid_emails}")
        
        if email_account_id in valid_emails:
            print(f"✅ Our email account '{email_account_id}' is valid!")
        else:
            print(f"❌ Our email account '{email_account_id}' is NOT in valid list!")
            print(f"🔧 Should use one of: {valid_emails}")
            
    else:
        print(f"❌ Failed to get accounts: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Error checking accounts: {e}")

# Step 2: Test simplified campaign creation with correct format
print(f"\n🏗️ STEP 2: Testing Corrected Campaign Structure")

# Use the first valid email if our current one doesn't work
correct_email = valid_emails[0] if valid_emails else email_account_id

correct_campaign_data = {
    "name": "DIAGNOSIS_TEST_CAMPAIGN",
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
                "timezone": "America/New_York"
            }
        ]
    },
    "email_list": [correct_email],  # Use validated email
    "sequences": [
        {
            "steps": [
                {
                    "subject": "Business Partnership Opportunity",
                    "body": "Hi {{first_name}}, I wanted to reach out about a potential partnership.",
                    "day": 1  # THIS IS THE KEY MISSING FIELD!
                }
            ]
        }
    ]
}

print(f"📤 Testing campaign with corrected structure:")
print(f"   Email account: {correct_email}")
print(f"   Sequence includes 'day' field: {correct_campaign_data['sequences'][0]['steps'][0].get('day')}")

try:
    response = requests.post(f"{base_url}/campaigns", headers=headers, json=correct_campaign_data)
    
    if response.status_code == 200:
        campaign_data = response.json()
        campaign_id = campaign_data.get('id')
        print(f"✅ Campaign created successfully: {campaign_id}")
        
        # Step 3: Add a test lead
        print(f"\n👤 STEP 3: Adding test lead to campaign")
        test_lead = {
            "email": "test@businessdomain.com",
            "first_name": "Test",
            "last_name": "User",
            "campaign": campaign_id
        }
        
        lead_response = requests.post(f"{base_url}/leads", headers=headers, json=test_lead)
        if lead_response.status_code == 200:
            print(f"✅ Test lead added successfully")
            
            # Step 4: Try activation
            print(f"\n🚀 STEP 4: Testing campaign activation")
            activation_response = requests.post(f"{base_url}/campaigns/{campaign_id}/activate", headers={"Authorization": f"Bearer {api_key}"})
            
            print(f"Activation status: {activation_response.status_code}")
            if activation_response.status_code == 200:
                print(f"✅ ACTIVATION SUCCESSFUL!")
                print(f"Response: {activation_response.json()}")
            else:
                print(f"❌ Activation failed: {activation_response.text}")
                
        else:
            print(f"❌ Failed to add test lead: {lead_response.text}")
    else:
        print(f"❌ Campaign creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error in diagnosis: {e}")

print(f"\n" + "="*60)
print(f"🎯 DIAGNOSIS COMPLETE")
print("="*60) 