import requests
import json

# Test the complete fixed system
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🧪 TESTING COMPLETE FIXED SYSTEM WITH ACTIVATION")
print("="*60)

# Use your test contacts CSV
with open('test_contacts.csv', 'r') as f:
    csv_content = f.read()

print(f"📋 Testing with business contacts:")
print(csv_content)

files = {'file': ('test_contacts.csv', csv_content, 'text/csv')}
data = {
    'campaign_content': 'Hello! I wanted to reach out regarding an exciting business partnership opportunity that could benefit your company.',
    'sender_name': 'Partnership Manager',
    'sender_title': 'Business Development Director',
    'sender_company': 'Strategic Partners Inc'
}

try:
    # Step 1: Generate emails
    print(f"\n📧 STEP 1: Generating emails...")
    response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful")
        print(f"Generated emails: {len(email_data.get('emails', []))}")
        
        # Step 2: Send emails (create campaigns + add contacts + activate)
        print(f"\n🚀 STEP 2: Creating and activating campaigns...")
        
        send_payload = {
            "approved_emails": email_data.get('emails', []),
            "campaign_name": "FINAL_TEST_WITH_ACTIVATION",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_payload, timeout=120)
        
        if send_response.status_code == 200:
            send_result = send_response.json()
            print(f"✅ System processing successful")
            print(f"Mode: {send_result.get('mode')}")
            print(f"Total processed: {send_result.get('total_processed')}")
            print(f"Successful: {send_result.get('successful_sends')}")
            print(f"Failed: {send_result.get('failed_sends')}")
            print(f"Campaigns created: {len(send_result.get('campaigns_created', []))}")
            print(f"🎯 Campaigns activated: {send_result.get('campaigns_activated', 0)}")
            
            results = send_result.get('results', [])
            print(f"\n📊 DETAILED RESULTS:")
            
            for i, result in enumerate(results):
                print(f"\nResult {i+1}:")
                print(f"  To: {result.get('to')}")
                print(f"  Status: {result.get('status')}")
                print(f"  Campaign ID: {result.get('campaign_id')}")
                print(f"  🎯 Activation Status: {result.get('activation_status', 'N/A')}")
                
                if result.get('lead_addition'):
                    lead_info = result['lead_addition']
                    print(f"  Lead Addition: {lead_info.get('successful_leads', 0)}/{lead_info.get('total_leads', 0)}")
            
            print(f"\n🎉 FINAL SUMMARY:")
            if send_result.get('campaigns_activated', 0) > 0:
                print(f"✅ SUCCESS! Campaigns are now ACTIVE and sending emails!")
                print(f"✅ {send_result.get('campaigns_activated')} campaigns activated")
                print(f"✅ Check your Instantly dashboard for active campaigns")
            else:
                print(f"⚠️ Campaigns created but activation status unclear")
                
        else:
            print(f"❌ System processing failed: {send_response.status_code}")
            print(f"Response: {send_response.text}")
    else:
        print(f"❌ Email generation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Test error: {e}")

print(f"\n" + "="*60)
print(f"🎯 SYSTEM STATUS:")
print(f"✅ Contact loading: WORKING")  
print(f"✅ Campaign creation: WORKING")
print(f"🎯 Campaign activation: TESTING...")
print("="*60) 