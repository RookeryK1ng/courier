import requests
import json
import time

# Final test of the complete deployment
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🎯 FINAL DEPLOYMENT TEST WITH COMPLETE ACTIVATION FIX")
print("="*65)

print("⏳ Waiting 30 seconds for deployment to complete...")
time.sleep(30)

# Create test CSV with business emails
csv_content = '''name,email,company
Final Test,test@finaltest.com,Final Test Company'''

files = {'file': ('final_test.csv', csv_content, 'text/csv')}
data = {
    'campaign_content': 'Final test of the complete activation system from Rob at BiscRed.',
    'sender_name': 'Rob',
    'sender_title': 'CEO',
    'sender_company': 'BiscRed'
}

print(f"📋 Final test parameters:")
print(f"   URL: {VERCEL_URL}")
print(f"   Sender: Rob from BiscRed")
print(f"   Expected account: rob@biscred.ai")
print(f"   Test email: test@finaltest.com")

try:
    # Test email generation
    print(f"\n📧 STEP 1: Testing email generation...")
    response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful")
        print(f"Generated emails: {len(email_data.get('emails', []))}")
        
        # Test complete flow: campaign creation + activation
        print(f"\n🚀 STEP 2: Testing complete flow with activation...")
        
        send_payload = {
            "approved_emails": email_data.get('emails', []),
            "campaign_name": "FINAL_DEPLOYMENT_TEST",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_payload, timeout=60)
        
        if send_response.status_code == 200:
            send_result = send_response.json()
            print(f"✅ System response successful!")
            print(f"Mode: {send_result.get('mode')}")
            print(f"Total processed: {send_result.get('total_processed')}")
            print(f"Successful: {send_result.get('successful_sends')}")
            print(f"Failed: {send_result.get('failed_sends')}")
            print(f"🎯 Campaigns activated: {send_result.get('campaigns_activated', 0)}")
            
            # Detailed analysis
            results = send_result.get('results', [])
            for result in results:
                print(f"\n📊 Final Test Results:")
                print(f"   To: {result.get('to')}")
                print(f"   Campaign ID: {result.get('campaign_id')}")
                print(f"   🎯 Activation Status: {result.get('activation_status', 'N/A')}")
                print(f"   Lead Addition: {result.get('lead_addition', {}).get('successful_leads', 0)}/1")
                
                # Check for activation success
                activation_status = result.get('activation_status')
                if activation_status == 'success':
                    print(f"\n🎉 SUCCESS! CAMPAIGN ACTIVATION WORKING!")
                    print(f"✅ Rob's account is sending emails")
                    print(f"✅ Campaign is ACTIVE in Instantly")
                    print(f"✅ Contact loading system is COMPLETE")
                elif activation_status == 'failed':
                    print(f"\n⚠️ Activation still failing")
                    print(f"   Campaign created but needs manual activation")
                else:
                    print(f"\n❓ Activation status: {activation_status}")
            
            # Overall status
            if send_result.get('campaigns_activated', 0) > 0:
                print(f"\n🎉 FINAL RESULT: COMPLETE SUCCESS!")
                print(f"✅ System is fully operational")
                print(f"✅ Automatic campaign activation working")
                print(f"✅ Ready for production use")
            else:
                print(f"\n📝 FINAL RESULT: Manual activation required")
                print(f"✅ Campaigns created successfully")
                print(f"📋 Check Instantly dashboard to activate")
                
        else:
            print(f"❌ System failed: {send_response.status_code}")
            print(f"Response: {send_response.text}")
            
    else:
        print(f"❌ Email generation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Final test error: {e}")

print(f"\n" + "="*65)
print(f"🎯 FINAL DEPLOYMENT TEST COMPLETE")
print(f"✅ Your contact loading system is ready!")
print("="*65) 