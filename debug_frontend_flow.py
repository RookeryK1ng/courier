import requests
import json
import io

# Configuration
VERCEL_URL = "https://sender-sigma.vercel.app"

print("🔍 DEBUGGING FRONTEND UPLOAD FLOW")
print("="*60)

# Step 1: Test the /generate-emails/ endpoint (what frontend calls first)
print("📋 STEP 1: Testing File Upload & Email Generation")

# Create a test CSV content (simulating what user would upload)
csv_content = '''name,email,company
Test User 1,test.user.1@example.com,Test Company 1
Test User 2,test.user.2@example.com,Test Company 2
Test User 3,test.user.3@example.com,Test Company 3'''

print(f"Test CSV content:")
print(csv_content)

# Prepare the request (simulate frontend file upload)
files = {
    'file': ('test_contacts.csv', csv_content, 'text/csv')
}

data = {
    'campaign_content': 'We are reaching out regarding an exciting partnership opportunity that could benefit your business.',
    'sender_name': 'Debug Test Sender',
    'sender_title': 'Partnership Manager',
    'sender_company': 'Debug Test Company'
}

print(f"\n🚀 Sending file upload request...")
print(f"Endpoint: {VERCEL_URL}/generate-emails/")
print(f"Form data: {data}")

try:
    # Step 1: Upload file and generate emails (what frontend does first)
    response = requests.post(
        f"{VERCEL_URL}/generate-emails/",
        files=files,
        data=data,
        timeout=60
    )
    
    print(f"\n📊 GENERATE EMAILS RESPONSE:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        email_data = response.json()
        print(f"✅ Email generation successful!")
        print(f"Generated emails count: {email_data.get('count')}")
        print(f"Mode: {email_data.get('mode')}")
        
        generated_emails = email_data.get('emails', [])
        
        if generated_emails:
            print(f"\n📧 GENERATED EMAILS:")
            for i, email in enumerate(generated_emails[:2], 1):  # Show first 2
                print(f"   {i}. To: {email.get('to')}")
                print(f"      Name: {email.get('name')}")
                print(f"      Company: {email.get('company')}")
                print(f"      Subject: {email.get('subject')}")
                print(f"      Body preview: {email.get('body', '')[:100]}...")
            
            # Step 2: Now test sending these generated emails (what frontend does next)
            print(f"\n📋 STEP 2: Testing Send Generated Emails")
            
            send_request = {
                "approved_emails": generated_emails,
                "campaign_name": "DEBUG_FRONTEND_FLOW",
                "send_mode": "instantly"
            }
            
            print(f"🚀 Sending generated emails...")
            send_response = requests.post(
                f"{VERCEL_URL}/send-emails/",
                json=send_request,
                timeout=60
            )
            
            print(f"\n📊 SEND EMAILS RESPONSE:")
            print(f"Status Code: {send_response.status_code}")
            
            if send_response.status_code == 200:
                send_data = send_response.json()
                print(f"✅ Send emails successful!")
                print(f"Mode: {send_data.get('mode')}")
                print(f"Total Processed: {send_data.get('total_processed')}")
                print(f"Successful: {send_data.get('successful_sends')}")
                print(f"Failed: {send_data.get('failed_sends')}")
                
                if send_data.get('mode') == 'simulation':
                    print(f"\n❌ ISSUE FOUND: Running in simulation mode!")
                    print(f"Something is wrong with the Instantly integration in this flow.")
                else:
                    print(f"\n✅ SUCCESS: Full frontend flow working!")
                    
                    # Show detailed results
                    campaigns_created = send_data.get('campaigns_created', [])
                    print(f"Campaigns Created: {len(campaigns_created)}")
                    
                    for i, result in enumerate(send_data.get('results', [])[:2], 1):
                        print(f"\n📧 Contact {i}: {result.get('to')}")
                        print(f"   Status: {result.get('status')}")
                        print(f"   Campaign ID: {result.get('campaign_id')}")
                        
                        if 'lead_addition' in result:
                            lead_info = result['lead_addition']
                            print(f"   Lead Addition: {lead_info.get('successful_leads')}/{lead_info.get('total_leads')} successful")
                            
                            if lead_info.get('failed_leads', 0) > 0:
                                print(f"   ❌ Lead failures:")
                                for failure in lead_info.get('failed_details', []):
                                    print(f"      - {failure.get('email')}: {failure.get('error')}")
                
                print(f"\n🎯 COMPARISON:")
                print(f"Direct test (worked): 3/3 contacts successful")
                print(f"Frontend flow: {send_data.get('successful_sends')}/{send_data.get('total_processed')} contacts successful")
                
                if send_data.get('successful_sends') == send_data.get('total_processed'):
                    print(f"✅ CONCLUSION: Frontend upload flow is WORKING!")
                    print(f"The issue might be in your specific CSV file or frontend interface.")
                else:
                    print(f"❌ CONCLUSION: Issue found in frontend upload flow!")
                
            else:
                print(f"❌ Send emails failed!")
                print(f"Response: {send_response.text}")
        else:
            print(f"❌ No emails generated!")
            
    else:
        print(f"❌ Email generation failed!")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*60)
print(f"🔍 DIAGNOSIS:")
print(f"1. If email generation fails → Issue with file processing")
print(f"2. If emails generate but sending fails → Issue with data format")
print(f"3. If both work → Issue might be with your specific CSV file")
print(f"4. Check what data your frontend is actually sending")
print("="*60) 