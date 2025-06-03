import requests
import json

# Test production deployment with Rob's account
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🚀 TESTING PRODUCTION DEPLOYMENT WITH ROB'S ACCOUNT")
print("="*65)

# Create test CSV with business emails
csv_content = '''name,email,company
Production Test,test@productiontest.com,Production Company'''

files = {'file': ('production_test.csv', csv_content, 'text/csv')}
data = {
    'campaign_content': 'Hello! This is a production test from Rob at BiscRed regarding a partnership opportunity.',
    'sender_name': 'Rob',
    'sender_title': 'Business Development',
    'sender_company': 'BiscRed'
}

print(f"📋 Testing production with:")
print(f"   URL: {VERCEL_URL}")
print(f"   Expected sender: rob@biscred.ai")
print(f"   Test email: test@productiontest.com")

try:
    # Test email generation
    print(f"\n📧 STEP 1: Testing email generation...")
    response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful")
        print(f"Generated emails: {len(email_data.get('emails', []))}")
        
        # Test campaign creation and activation
        print(f"\n🚀 STEP 2: Testing campaign creation and activation...")
        
        send_payload = {
            "approved_emails": email_data.get('emails', []),
            "campaign_name": "PRODUCTION_ROB_TEST",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_payload, timeout=60)
        
        if send_response.status_code == 200:
            send_result = send_response.json()
            print(f"✅ Production system working!")
            print(f"Mode: {send_result.get('mode')}")
            print(f"Total processed: {send_result.get('total_processed')}")
            print(f"Successful: {send_result.get('successful_sends')}")
            print(f"Failed: {send_result.get('failed_sends')}")
            print(f"🎯 Campaigns activated: {send_result.get('campaigns_activated', 0)}")
            
            # Check detailed results
            results = send_result.get('results', [])
            for result in results:
                print(f"\n📊 Campaign Details:")
                print(f"   To: {result.get('to')}")
                print(f"   Campaign ID: {result.get('campaign_id')}")
                print(f"   🎯 Activation Status: {result.get('activation_status', 'N/A')}")
                print(f"   Lead Addition: {result.get('lead_addition', {}).get('successful_leads', 0)}/1")
            
            if send_result.get('campaigns_activated', 0) > 0:
                print(f"\n🎉 SUCCESS! PRODUCTION DEPLOYMENT WORKING!")
                print(f"✅ Rob's account activated campaigns successfully")
                print(f"✅ Campaigns are now live and sending emails")
                print(f"✅ Check Instantly dashboard for active campaigns")
            else:
                print(f"\n⚠️ Campaigns created but activation status unclear")
                print(f"   Check Vercel environment variables")
                
        else:
            print(f"❌ Campaign creation failed: {send_response.status_code}")
            print(f"Response: {send_response.text}")
            if "tim@biscred.com" in send_response.text:
                print(f"🔧 ISSUE: Still using old email account - update environment variable!")
                
    else:
        print(f"❌ Email generation failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Production test error: {e}")

print(f"\n" + "="*65)
print(f"🎯 PRODUCTION DEPLOYMENT STATUS")
print(f"✅ Code: DEPLOYED")
print(f"🔧 Environment: UPDATE INSTANTLY_EMAIL_ACCOUNT_ID to rob@biscred.ai")
print(f"🧪 Test: RUN THIS SCRIPT AFTER ENV UPDATE")
print("="*65) 