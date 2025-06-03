import requests
import json
import time

VERCEL_URL = "https://sender-sigma.vercel.app"

print("🧪 TESTING DIFFERENT EMAIL TYPES")
print("="*50)

# Test different types of email addresses
test_cases = [
    {
        "name": "Duncan Gmail",
        "csv": "name,email,company\nDuncan Test,duncan.test@gmail.com,TestCorp",
        "description": "Gmail address (like yours)"
    },
    {
        "name": "Duncan Business", 
        "csv": "name,email,company\nDuncan Test,duncan@testcorp.com,TestCorp",
        "description": "Business domain"
    },
    {
        "name": "Duncan Outlook",
        "csv": "name,email,company\nDuncan Test,duncan.test@outlook.com,TestCorp", 
        "description": "Outlook address"
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n🧪 TEST {i}: {test_case['name']}")
    print(f"Description: {test_case['description']}")
    print(f"CSV: {test_case['csv']}")
    
    try:
        # Upload and generate email
        files = {'file': ('test.csv', test_case['csv'], 'text/csv')}
        data = {
            'campaign_content': 'Test partnership opportunity.',
            'sender_name': 'Test Sender',
            'sender_title': 'Tester',
            'sender_company': 'Test Co'
        }
        
        response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            email_data = response.json()
            generated_emails = email_data.get('emails', [])
            
            if generated_emails:
                # Try to send
                send_request = {
                    "approved_emails": generated_emails,
                    "campaign_name": f"EMAIL_TEST_{i}_{int(time.time())}",
                    "send_mode": "instantly"
                }
                
                send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_request, timeout=30)
                
                if send_response.status_code == 200:
                    send_data = send_response.json()
                    result = send_data.get('results', [{}])[0]
                    
                    print(f"✅ Campaign Created: {result.get('campaign_id', 'N/A')}")
                    print(f"📊 Send Status: {send_data.get('successful_sends')}/{send_data.get('total_processed')}")
                    
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        successful = lead_info.get('successful_leads', 0)
                        total = lead_info.get('total_leads', 0)
                        
                        if successful > 0:
                            print(f"✅ LEAD ADDITION: {successful}/{total} SUCCESS")
                        else:
                            print(f"❌ LEAD ADDITION: {successful}/{total} FAILED")
                            
                            failures = lead_info.get('failed_details', [])
                            if failures:
                                for failure in failures:
                                    print(f"   Error: {failure.get('error', 'Unknown')}")
                    else:
                        print(f"❌ No lead addition info")
                else:
                    print(f"❌ Send failed: {send_response.status_code}")
            else:
                print(f"❌ No emails generated")
        else:
            print(f"❌ Upload failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")

print(f"\n" + "="*50)
print(f"🎯 HYPOTHESIS:")
print(f"If Gmail fails but business domains work →")
print(f"   Instantly blocks consumer email addresses")
print(f"If all fail → There's a broader API issue")
print(f"If all work → Your specific email is the problem")
print("="*50) 