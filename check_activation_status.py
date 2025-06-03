import requests
import json

# Configuration
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🔍 CHECKING CAMPAIGN ACTIVATION STATUS")
print("="*50)

# Test with a simple contact to see activation in action
csv_content = '''name,email,company
Test User,test@businessdomain.com,Test Corp'''

files = {'file': ('test.csv', csv_content, 'text/csv')}
data = {
    'campaign_content': 'Testing activation functionality.',
    'sender_name': 'Test Sender',
    'sender_title': 'Tester',
    'sender_company': 'Test Co'
}

print(f"🚀 Creating campaign to test activation...")

try:
    # Generate email
    response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        email_data = response.json()
        generated_emails = email_data.get('emails', [])
        
        if generated_emails:
            # Send and check activation
            send_request = {
                "approved_emails": generated_emails,
                "campaign_name": f"ACTIVATION_TEST_{int(__import__('time').time())}",
                "send_mode": "instantly"
            }
            
            print(f"📧 Sending to Instantly...")
            send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_request, timeout=30)
            
            if send_response.status_code == 200:
                result = send_response.json()
                
                print(f"\n📊 SEND RESULTS:")
                print(f"Mode: {result.get('mode')}")
                print(f"Total Processed: {result.get('total_processed')}")
                print(f"Successful: {result.get('successful_sends')}")
                print(f"Failed: {result.get('failed_sends')}")
                
                # Check activation details
                campaigns_activated = result.get('campaigns_activated', 0)
                print(f"\n🚀 ACTIVATION STATUS:")
                print(f"Campaigns Activated: {campaigns_activated}")
                
                if campaigns_activated > 0:
                    print(f"✅ SUCCESS: Campaign was automatically activated!")
                else:
                    print(f"⚠️ WARNING: Campaign was not activated")
                
                # Check individual results
                for i, contact_result in enumerate(result.get('results', []), 1):
                    print(f"\n📧 Contact {i}: {contact_result.get('to')}")
                    print(f"   Campaign ID: {contact_result.get('campaign_id')}")
                    print(f"   Status: {contact_result.get('status')}")
                    
                    activation_status = contact_result.get('activation_status')
                    activation_message = contact_result.get('activation_message')
                    
                    if activation_status:
                        print(f"   🚀 Activation: {activation_status}")
                        print(f"   Message: {activation_message}")
                        
                        if activation_status == 'success':
                            print(f"   ✅ This campaign is ACTIVE and ready to send!")
                        else:
                            print(f"   ❌ Activation failed")
                    else:
                        print(f"   ⚠️ No activation info returned")
                
                print(f"\n🎯 SUMMARY:")
                if campaigns_activated > 0:
                    print(f"✅ Auto-activation is WORKING!")
                    print(f"✅ Your campaigns are ready to send emails")
                    print(f"✅ No manual activation needed")
                else:
                    print(f"❌ Auto-activation failed")
                    print(f"📝 You may need to manually activate in Instantly dashboard")
                    
            else:
                print(f"❌ Send failed: {send_response.status_code}")
                print(f"Response: {send_response.text}")
        else:
            print(f"❌ No emails generated")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")

print(f"\n" + "="*50)
print(f"🎯 ACTIVATION OPTIONS:")
print(f"1. ✅ Automatic (built into system)")
print(f"2. 🔧 Manual via Instantly dashboard")
print(f"3. 🔧 Manual via API endpoint: /activate-campaign/")
print("="*50) 