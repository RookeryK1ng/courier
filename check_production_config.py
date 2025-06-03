import requests
import json

# Check what configuration the production deployment is using
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🔍 CHECKING PRODUCTION CONFIGURATION")
print("="*50)

try:
    # Test a simple request to see what configuration is being used
    response = requests.get(f"{VERCEL_URL}/", timeout=10)
    print(f"✅ Production site accessible: {response.status_code}")
    
    # Check if we can get any configuration info
    print(f"\n🔧 Testing configuration endpoint...")
    
    # Create a minimal test to see the actual email account being used
    csv_content = "name,email,company\nConfig Test,test@configtest.com,Config Company"
    files = {'file': ('config_test.csv', csv_content, 'text/csv')}
    data = {
        'campaign_content': 'Configuration test',
        'sender_name': 'Test',
        'sender_title': 'Test',
        'sender_company': 'Test'
    }
    
    # Generate emails to see what account is configured
    gen_response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
    
    if gen_response.status_code == 200:
        email_data = gen_response.json()
        print(f"✅ Email generation working")
        
        # Try to send and capture the detailed error to see actual config
        send_payload = {
            "approved_emails": email_data.get('emails', []),
            "campaign_name": "CONFIG_CHECK_TEST",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_payload, timeout=60)
        
        print(f"\n📊 DETAILED RESPONSE ANALYSIS:")
        print(f"Status Code: {send_response.status_code}")
        print(f"Response Text: {send_response.text}")
        
        if send_response.status_code == 200:
            result = send_response.json()
            print(f"\n🔍 CHECKING FOR EMAIL ACCOUNT CLUES:")
            
            # Look for any mentions of email accounts in the response
            response_str = str(result)
            if "tim@biscred.com" in response_str:
                print(f"❌ FOUND: Still using tim@biscred.com (OLD ACCOUNT)")
                print(f"🔧 SOLUTION: Environment variable not updated in Vercel!")
            elif "rob@biscred.ai" in response_str:
                print(f"✅ FOUND: Using rob@biscred.ai (CORRECT ACCOUNT)")
                print(f"🔧 ISSUE: Activation failing for different reason")
            else:
                print(f"⚠️ Email account not visible in response")
                
            # Check activation status details
            results = result.get('results', [])
            for r in results:
                campaign_id = r.get('campaign_id')
                activation_status = r.get('activation_status')
                print(f"\n📋 Campaign: {campaign_id}")
                print(f"   Activation Status: {activation_status}")
                
                # If we have a campaign ID, let's test activation directly
                if campaign_id:
                    print(f"🧪 Testing direct activation...")
                    activation_test = requests.post(
                        f"{VERCEL_URL}/activate-campaign/",
                        json=campaign_id,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    print(f"   Direct activation: {activation_test.status_code}")
                    if activation_test.status_code != 200:
                        print(f"   Error: {activation_test.text}")
        else:
            print(f"❌ Send failed: {send_response.text}")
            
            # Check if error mentions specific email account
            if "tim@biscred.com" in send_response.text:
                print(f"🚨 CONFIRMED: Production still using tim@biscred.com")
                print(f"🔧 ACTION REQUIRED: Update Vercel environment variable!")
                
    else:
        print(f"❌ Email generation failed: {gen_response.status_code}")
        print(f"Response: {gen_response.text}")
        
except Exception as e:
    print(f"❌ Configuration check error: {e}")

print(f"\n" + "="*50)
print(f"🎯 DIAGNOSIS COMPLETE")
print("="*50) 