import requests
import json
import time

VERCEL_URL = "https://sender-sigma.vercel.app"

print("🎯 TESTING DUNCAN'S BISCRED BUSINESS EMAIL")
print("="*55)

# Read the BiscRed CSV file
with open('duncan_biscred.csv', 'r') as f:
    csv_content = f.read()

print(f"CSV Content:")
print(csv_content)
print(f"\n📧 Business Email: duncan@biscred.com")
print(f"🏢 Company: BiscRed")
print(f"👔 Position: CEO")

# Test the upload
files = {
    'file': ('duncan_biscred.csv', csv_content, 'text/csv')
}

data = {
    'campaign_content': 'Hello! I wanted to reach out regarding an exciting partnership opportunity that could benefit BiscRed.',
    'sender_name': 'Partnership Manager',
    'sender_title': 'Business Development',
    'sender_company': 'Strategic Partners'
}

print(f"\n🚀 Testing BiscRed email upload...")

try:
    # Step 1: Generate emails
    response = requests.post(
        f"{VERCEL_URL}/generate-emails/",
        files=files,
        data=data,
        timeout=60
    )
    
    print(f"\n📊 EMAIL GENERATION:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful!")
        print(f"Generated emails: {email_data.get('count')}")
        
        generated_emails = email_data.get('emails', [])
        if generated_emails:
            email = generated_emails[0]
            print(f"\n📧 GENERATED EMAIL:")
            print(f"To: {email.get('to')}")
            print(f"Name: {email.get('name')}")
            print(f"Company: {email.get('company')}")
            print(f"Subject: {email.get('subject')}")
            print(f"Body preview: {email.get('body', '')[:150]}...")
            
            # Step 2: Send to Instantly
            print(f"\n🚀 SENDING TO INSTANTLY...")
            campaign_name = f"BISCRED_DUNCAN_TEST_{int(time.time())}"
            
            send_request = {
                "approved_emails": generated_emails,
                "campaign_name": campaign_name,
                "send_mode": "instantly"
            }
            
            send_response = requests.post(
                f"{VERCEL_URL}/send-emails/",
                json=send_request,
                timeout=60
            )
            
            print(f"📊 SEND RESPONSE:")
            print(f"Status Code: {send_response.status_code}")
            
            if send_response.status_code == 200:
                send_data = send_response.json()
                print(f"✅ Send successful!")
                print(f"Mode: {send_data.get('mode')}")
                print(f"Total Processed: {send_data.get('total_processed')}")
                print(f"Successful: {send_data.get('successful_sends')}")
                print(f"Failed: {send_data.get('failed_sends')}")
                
                if send_data.get('successful_sends') > 0:
                    result = send_data.get('results', [{}])[0]
                    print(f"\n🎯 CONTACT ADDITION RESULT:")
                    print(f"Campaign ID: {result.get('campaign_id')}")
                    print(f"Status: {result.get('status')}")
                    
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        successful = lead_info.get('successful_leads', 0)
                        total = lead_info.get('total_leads', 0)
                        
                        if successful > 0:
                            print(f"✅ LEAD ADDITION SUCCESS: {successful}/{total}")
                            print(f"\n🎉 DUNCAN'S BISCRED EMAIL WORKS!")
                            print(f"📍 Check your Instantly dashboard for:")
                            print(f"   Campaign: {campaign_name}")
                            print(f"   Contact: duncan@biscred.com")
                            print(f"   Campaign ID: {result.get('campaign_id')}")
                        else:
                            print(f"❌ LEAD ADDITION FAILED: {successful}/{total}")
                            failures = lead_info.get('failed_details', [])
                            if failures:
                                for failure in failures:
                                    print(f"   Error: {failure.get('error', 'Unknown')}")
                else:
                    print(f"❌ No contacts processed successfully")
                    print(f"Response: {send_data}")
            else:
                print(f"❌ Send failed: {send_response.status_code}")
                print(f"Response: {send_response.text}")
        else:
            print(f"❌ No emails generated")
    else:
        print(f"❌ Email generation failed: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*55)
print(f"🎯 EXPECTED RESULT:")
print(f"✅ Business email should work (unlike Gmail)")
print(f"✅ Campaign should be created with contact added")
print(f"📧 Email: duncan@biscred.com should appear in Instantly")
print("="*55) 