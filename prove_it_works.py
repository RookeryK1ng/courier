import requests
import json
import time

# Configuration
VERCEL_URL = "https://sender-sigma.vercel.app"  # Your actual deployment URL
CAMPAIGN_NAME = f"PROOF_TEST_{int(time.time())}"

print("🎯 PROOF TEST: Creating Real Campaign with Real Contacts")
print("="*70)
print(f"Vercel URL: {VERCEL_URL}")
print(f"Campaign Name: {CAMPAIGN_NAME}")

# Create test contacts that will be added to the campaign
test_contacts = [
    {
        "to": "proof.test.1@example.com",
        "name": "Proof Test User 1",
        "company": "Proof Test Corp",
        "subject": "Proof Test Campaign - Contact 1", 
        "body": "This is a proof test email for contact 1. This campaign should appear in your Instantly dashboard."
    },
    {
        "to": "proof.test.2@example.com", 
        "name": "Proof Test User 2",
        "company": "Another Test Corp",
        "subject": "Proof Test Campaign - Contact 2",
        "body": "This is a proof test email for contact 2. This campaign should appear in your Instantly dashboard."
    },
    {
        "to": "proof.test.3@example.com",
        "name": "Proof Test User 3", 
        "company": "Third Test Corp",
        "subject": "Proof Test Campaign - Contact 3",
        "body": "This is a proof test email for contact 3. This campaign should appear in your Instantly dashboard."
    }
]

print(f"📋 Creating campaign with {len(test_contacts)} contacts:")
for i, contact in enumerate(test_contacts, 1):
    print(f"   {i}. {contact['name']} ({contact['to']}) at {contact['company']}")

# Send the request to create campaign and add contacts
request_data = {
    "approved_emails": test_contacts,
    "campaign_name": CAMPAIGN_NAME,
    "send_mode": "instantly"
}

print(f"\n🚀 SENDING REQUEST TO VERCEL...")
print(f"Endpoint: {VERCEL_URL}/send-emails/")
print(f"Request data: {json.dumps(request_data, indent=2)}")

try:
    response = requests.post(
        f"{VERCEL_URL}/send-emails/",
        json=request_data,
        timeout=60  # Give it more time for multiple contacts
    )
    
    print(f"\n📊 RESPONSE:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(f"Mode: {data.get('mode')}")
        print(f"Total Processed: {data.get('total_processed')}")
        print(f"Successful: {data.get('successful_sends')}")
        print(f"Failed: {data.get('failed_sends')}")
        
        if data.get('mode') == 'simulation':
            print(f"\n❌ RUNNING IN SIMULATION MODE!")
            print(f"The integration is not working properly.")
        else:
            print(f"\n🎯 DETAILED RESULTS:")
            
            campaigns_created = data.get('campaigns_created', [])
            print(f"Campaigns Created: {len(campaigns_created)}")
            for campaign_id in campaigns_created:
                print(f"   - Campaign ID: {campaign_id}")
            
            # Check each contact result
            for i, result in enumerate(data.get('results', []), 1):
                print(f"\n📧 Contact {i}: {result.get('to')}")
                print(f"   Status: {result.get('status')}")
                print(f"   Message: {result.get('message')}")
                print(f"   Campaign ID: {result.get('campaign_id')}")
                
                # Check lead addition details
                if 'lead_addition' in result:
                    lead_info = result['lead_addition']
                    print(f"   🎯 Lead Addition:")
                    print(f"      Total: {lead_info.get('total_leads')}")
                    print(f"      Successful: {lead_info.get('successful_leads')}")
                    print(f"      Failed: {lead_info.get('failed_leads')}")
                    
                    if lead_info.get('failed_leads', 0) > 0:
                        print(f"      ❌ Failed Details:")
                        for failure in lead_info.get('failed_details', []):
                            print(f"         - {failure.get('email')}: {failure.get('error')}")
                
                # Check activation status
                if 'activation_status' in result:
                    print(f"   🚀 Activation: {result.get('activation_status')}")
                    print(f"   Message: {result.get('activation_message')}")
        
        print(f"\n" + "="*70)
        print(f"🔍 VERIFICATION STEPS:")
        print(f"1. Go to your Instantly dashboard")
        print(f"2. Look for campaign: '{CAMPAIGN_NAME}'")
        print(f"3. Check if it contains {len(test_contacts)} contacts:")
        for contact in test_contacts:
            print(f"   - {contact['to']}")
        print(f"4. Verify campaign status and settings")
        
        if data.get('successful_sends', 0) == len(test_contacts):
            print(f"\n✅ PROOF: Contact loading is WORKING!")
            print(f"   All {len(test_contacts)} contacts should appear in your dashboard.")
        else:
            print(f"\n❌ PROOF: Contact loading is NOT working properly!")
            print(f"   Only {data.get('successful_sends', 0)}/{len(test_contacts)} contacts were processed successfully.")
        
    else:
        print(f"❌ REQUEST FAILED!")
        print(f"Response: {response.text}")
        
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")

except requests.exceptions.Timeout:
    print(f"❌ REQUEST TIMED OUT!")
    print(f"The request took longer than 60 seconds.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*70)
print(f"🏁 PROOF TEST COMPLETE")
print(f"Campaign Name to Look For: {CAMPAIGN_NAME}")
print("="*70) 