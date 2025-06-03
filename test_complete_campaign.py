import requests
import json

# Configuration
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🎯 TESTING COMPLETE CAMPAIGN CREATION + ACTIVATION")
print("="*60)

# Test with a business email CSV
csv_content = '''name,email,company
Test Business,test@testcompany.com,Test Company'''

files = {'file': ('test.csv', csv_content, 'text/csv')}
data = {
    'campaign_content': 'Hello! We would like to discuss a potential business partnership with Test Company.',
    'sender_name': 'Business Development',
    'sender_title': 'BD Manager', 
    'sender_company': 'Our Company'
}

print(f"📋 Test Campaign Content:")
print(f"CSV: {csv_content}")
print(f"Campaign Content: {data['campaign_content']}")

try:
    # Step 1: Generate emails
    print(f"\n📧 STEP 1: Generating emails...")
    response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful")
        print(f"Generated emails: {len(email_data.get('emails', []))}")
        
        # Step 2: Send emails (create campaigns + add contacts)
        print(f"\n🚀 STEP 2: Sending emails (creating campaigns)...")
        
        # Prepare the correct payload format for send-emails endpoint
        send_payload = {
            "approved_emails": email_data.get('emails', []),
            "campaign_name": "TEST_COMPLETE_CAMPAIGN",
            "send_mode": "instantly"
        }
        
        print(f"📤 Sending payload:")
        print(f"   approved_emails count: {len(send_payload['approved_emails'])}")
        print(f"   campaign_name: {send_payload['campaign_name']}")
        print(f"   send_mode: {send_payload['send_mode']}")
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_payload, timeout=60)
        
        if send_response.status_code == 200:
            send_result = send_response.json()
            print(f"✅ Campaign creation successful")
            print(f"Mode: {send_result.get('mode')}")
            print(f"Total processed: {send_result.get('total_processed')}")
            print(f"Successful: {send_result.get('successful_sends')}")
            print(f"Failed: {send_result.get('failed_sends')}")
            print(f"Campaigns created: {len(send_result.get('campaigns_created', []))}")
            print(f"Campaigns activated: {send_result.get('campaigns_activated', 0)}")
            
            results = send_result.get('results', [])
            print(f"\n📊 DETAILED RESULTS:")
            
            for i, result in enumerate(results):
                print(f"\nResult {i+1}:")
                print(f"  To: {result.get('to')}")
                print(f"  Status: {result.get('status')}")
                print(f"  Campaign ID: {result.get('campaign_id')}")
                print(f"  Activation Status: {result.get('activation_status', 'N/A')}")
                
                if result.get('lead_addition'):
                    lead_info = result['lead_addition']
                    print(f"  Lead Addition: {lead_info.get('successful_leads', 0)}/{lead_info.get('total_leads', 0)}")
                
                # Test manual activation if auto-activation failed
                campaign_id = result.get('campaign_id')
                if campaign_id and result.get('activation_status') != 'success':
                    print(f"\n🔧 Testing manual activation for campaign {campaign_id}...")
                    try:
                        activation_response = requests.post(
                            f"{VERCEL_URL}/activate-campaign/",
                            json=campaign_id,
                            headers={"Content-Type": "application/json"},
                            timeout=30
                        )
                        
                        print(f"  Manual activation status: {activation_response.status_code}")
                        if activation_response.status_code == 200:
                            print(f"  ✅ Manual activation successful!")
                        else:
                            print(f"  ⚠️ Manual activation failed: {activation_response.text}")
                            
                    except Exception as e:
                        print(f"  ❌ Manual activation error: {e}")
            
        else:
            print(f"❌ Campaign creation failed: {send_response.status_code}")
            print(f"Response: {send_response.text}")
    else:
        print(f"❌ Email generation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Test error: {e}")

print(f"\n" + "="*60)
print(f"🎯 CONCLUSION:")
print(f"This test shows us:")
print(f"1. Whether the complete flow works end-to-end")
print(f"2. If campaigns are created with proper activation fields")
print(f"3. The exact activation error details and resolution")
print("="*60) 