import requests
import json
from instantly_client import InstantlyClient

print("🔍 TESTING CONTACT ADDITION TO CAMPAIGNS")
print("="*60)

# Initialize client
client = InstantlyClient()

# Test data
test_campaign_id = "1cd17813-4d00-4a1e-809e-5e99f7350ba8"  # Test_Fixed_Campaign_1
test_contacts = [
    {
        "to": "john.doe@example.com",
        "name": "John Doe",
        "company": "Test Company Inc",
        "subject": "Test Email Subject",
        "body": "This is a test email body."
    },
    {
        "to": "jane.smith@example.com", 
        "name": "Jane Smith",
        "company": "Example Corp",
        "subject": "Test Email Subject",
        "body": "This is another test email body."
    }
]

try:
    print(f"📋 Testing with campaign: {test_campaign_id}")
    print(f"📋 Adding {len(test_contacts)} test contacts...")
    
    # Test adding leads to campaign
    result = client.add_leads_to_campaign(test_campaign_id, test_contacts)
    
    print(f"\n✅ RESULT:")
    print(f"   Total leads processed: {result.get('total_leads', 0)}")
    print(f"   Successful: {result.get('successful_leads', 0)}")
    print(f"   Failed: {result.get('failed_leads', 0)}")
    
    if result.get('successful_details'):
        print(f"\n🎯 SUCCESSFUL LEADS:")
        for lead in result['successful_details']:
            print(f"   - {lead.get('email')}: {lead.get('status')} (ID: {lead.get('lead_id')})")
    
    if result.get('failed_details'):
        print(f"\n❌ FAILED LEADS:")
        for lead in result['failed_details']:
            print(f"   - {lead.get('email')}: {lead.get('error')}")
    
    # Now verify the leads were added by checking campaign leads
    print(f"\n📋 VERIFYING LEADS WERE ADDED...")
    
    # Use the correct endpoint to get campaign leads
    headers = {
        "Authorization": f"Bearer {client.api_key}",
        "Content-Type": "application/json"
    }
    
    # Get leads with campaign filter
    leads_request = {
        "campaign": test_campaign_id,
        "limit": 10
    }
    
    verification_response = requests.post(
        f"{client.base_url}/leads/list",
        headers=headers,
        json=leads_request
    )
    
    if verification_response.status_code == 200:
        verification_data = verification_response.json()
        campaign_leads = verification_data.get('items', [])
        
        print(f"✅ VERIFICATION: Found {len(campaign_leads)} leads in campaign")
        
        # Check if our test emails are there
        test_emails = [contact['to'] for contact in test_contacts]
        found_emails = [lead.get('email') for lead in campaign_leads if lead.get('email') in test_emails]
        
        print(f"🎯 Our test emails found: {found_emails}")
        
        if len(found_emails) == len(test_emails):
            print("✅ SUCCESS: All test contacts were added successfully!")
        else:
            print("⚠️ PARTIAL: Some contacts may not have been added or are pending")
            
    else:
        print(f"❌ Verification failed: {verification_response.status_code} - {verification_response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*60)
print("🏁 CONTACT ADDITION TEST COMPLETE")
print("="*60) 