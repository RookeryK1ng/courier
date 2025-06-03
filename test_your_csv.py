import requests
import json

# Configuration
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🎯 TESTING YOUR EXACT CSV FILE")
print("="*50)

# Your exact CSV content
csv_content = '''name,email,company,position,industry
Duncan Stockdale,duncan.stockdale@gmail.com,BiscRed,CEO,Real Estate Technology'''

print(f"Your CSV content:")
print(csv_content)
print(f"\nColumns: name, email, company, position, industry")
print(f"Extra columns: position, industry")

# Test the upload
files = {
    'file': ('test_contact_duncan.csv', csv_content, 'text/csv')
}

data = {
    'campaign_content': 'Hello! I wanted to reach out regarding a potential partnership opportunity.',
    'sender_name': 'Test Sender',
    'sender_title': 'Business Development',
    'sender_company': 'Test Company'
}

print(f"\n🚀 Testing your CSV upload...")
try:
    response = requests.post(
        f"{VERCEL_URL}/generate-emails/",
        files=files,
        data=data,
        timeout=60
    )
    
    print(f"\n📊 RESPONSE:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful!")
        print(f"Generated emails count: {email_data.get('count')}")
        
        generated_emails = email_data.get('emails', [])
        if generated_emails:
            email = generated_emails[0]
            print(f"\n📧 GENERATED EMAIL:")
            print(f"To: {email.get('to')}")
            print(f"Name: {email.get('name')}")
            print(f"Company: {email.get('company')}")
            print(f"Subject: {email.get('subject')}")
            print(f"Body preview: {email.get('body', '')[:200]}...")
            
            # Check if extra columns are being handled
            print(f"\n🔍 CHECKING EXTRA COLUMNS:")
            if 'position' in email:
                print(f"Position field: {email.get('position')}")
            else:
                print(f"❌ Position field missing (this might be the issue)")
                
            if 'industry' in email:
                print(f"Industry field: {email.get('industry')}")
            else:
                print(f"❌ Industry field missing")
            
            # Now test sending
            print(f"\n🚀 Testing send with your contact...")
            send_request = {
                "approved_emails": generated_emails,
                "campaign_name": f"DUNCAN_TEST_{int(__import__('time').time())}",
                "send_mode": "instantly"
            }
            
            send_response = requests.post(
                f"{VERCEL_URL}/send-emails/",
                json=send_request,
                timeout=60
            )
            
            if send_response.status_code == 200:
                send_data = send_response.json()
                print(f"✅ Send successful!")
                print(f"Mode: {send_data.get('mode')}")
                print(f"Successful: {send_data.get('successful_sends')}")
                print(f"Failed: {send_data.get('failed_sends')}")
                
                if send_data.get('successful_sends') > 0:
                    result = send_data.get('results', [{}])[0]
                    print(f"\n✅ YOUR CONTACT SUCCESSFULLY ADDED!")
                    print(f"Campaign ID: {result.get('campaign_id')}")
                    print(f"Status: {result.get('status')}")
                    
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        print(f"Lead Addition: {lead_info.get('successful_leads')}/{lead_info.get('total_leads')}")
                        
                        if lead_info.get('failed_leads', 0) > 0:
                            print(f"❌ Lead addition failed:")
                            for failure in lead_info.get('failed_details', []):
                                print(f"   {failure.get('email')}: {failure.get('error')}")
                    
                    print(f"\n🎯 Go check your Instantly dashboard for:")
                    print(f"   Campaign: {send_request['campaign_name']}")
                    print(f"   Contact: duncan.stockdale@gmail.com")
                else:
                    print(f"❌ Send failed for your contact!")
                    print(f"Response: {send_data}")
            else:
                print(f"❌ Send request failed: {send_response.status_code}")
                print(f"Response: {send_response.text}")
        else:
            print(f"❌ No emails generated from your CSV!")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Try to parse error details
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            pass

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*50)
print(f"🔍 ANALYSIS:")
print(f"If this works → Your CSV format is fine")
print(f"If this fails → Extra columns are causing issues")
print(f"Check your Instantly dashboard for the campaign!")
print("="*50) 