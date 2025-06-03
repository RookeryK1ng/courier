import requests
import json
from instantly_client import InstantlyClient

print("🔍 TESTING NEW CAMPAIGN + CONTACT ADDITION")
print("="*60)

# Initialize client
client = InstantlyClient()

# Test data for a fresh campaign
test_contacts = [
    {
        "to": "fresh.test1@example.com",
        "name": "Fresh Test User 1",
        "company": "New Campaign Corp",
        "subject": "New Campaign Test",
        "body": "This is a test for a fresh campaign."
    },
    {
        "to": "fresh.test2@example.com", 
        "name": "Fresh Test User 2",
        "company": "Another New Corp",
        "subject": "New Campaign Test",
        "body": "This is another test for a fresh campaign."
    }
]

try:
    print(f"📋 STEP 1: Creating a brand new campaign...")
    
    # Create a completely new campaign
    campaign_name = f"Fresh_Test_Campaign_{int(__import__('time').time())}"
    email_subject = "Fresh Campaign Test Email"
    email_body = "This is a test email body for a fresh campaign."
    
    campaign_id = client.create_campaign(campaign_name, email_subject, email_body)
    print(f"✅ New campaign created: {campaign_id}")
    
    print(f"\n📋 STEP 2: Immediately adding contacts to the new campaign...")
    
    # Try adding contacts immediately after campaign creation
    result = client.add_leads_to_campaign(campaign_id, test_contacts)
    
    print(f"\n✅ CONTACT ADDITION RESULTS:")
    print(f"   Total: {result.get('total_leads', 0)}")
    print(f"   Successful: {result.get('successful_leads', 0)}")
    print(f"   Failed: {result.get('failed_leads', 0)}")
    
    if result.get('successful_details'):
        print(f"\n🎯 SUCCESSFUL CONTACTS:")
        for lead in result['successful_details']:
            print(f"   - {lead.get('email')}: {lead.get('status')} (ID: {lead.get('lead_id')})")
    
    if result.get('failed_details'):
        print(f"\n❌ FAILED CONTACTS:")
        for lead in result['failed_details']:
            print(f"   - {lead.get('email')}: {lead.get('error')}")
    
    print(f"\n📋 STEP 3: Verifying contacts were added...")
    
    # Verify the contacts were added
    headers = {
        "Authorization": f"Bearer {client.api_key}",
        "Content-Type": "application/json"
    }
    
    verification_request = {
        "campaign": campaign_id,
        "limit": 10
    }
    
    verification_response = requests.post(
        f"{client.base_url}/leads/list",
        headers=headers,
        json=verification_request
    )
    
    if verification_response.status_code == 200:
        verification_data = verification_response.json()
        campaign_leads = verification_data.get('items', [])
        
        print(f"✅ VERIFICATION: Found {len(campaign_leads)} leads in new campaign")
        
        # Check our test emails
        test_emails = [contact['to'] for contact in test_contacts]
        found_emails = [lead.get('email') for lead in campaign_leads if lead.get('email') in test_emails]
        
        print(f"🎯 Our test emails found: {found_emails}")
        
        if len(found_emails) == len(test_emails):
            print("✅ SUCCESS: All contacts were added to the new campaign!")
        else:
            print("⚠️ ISSUE: Some contacts may not have been added")
            
        # Show all leads in the campaign for debugging
        print(f"\n📋 ALL LEADS IN NEW CAMPAIGN:")
        for lead in campaign_leads:
            print(f"   - {lead.get('email')} (ID: {lead.get('id')})")
            
    else:
        print(f"❌ Verification failed: {verification_response.status_code} - {verification_response.text}")
    
    print(f"\n📋 CAMPAIGN INFO:")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Campaign Name: {campaign_name}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🏁 NEW CAMPAIGN + CONTACT TEST COMPLETE")
print("="*60) 