import requests
import json
import os

print("🔍 TESTING CONTACT ADDITION TO CAMPAIGNS (FIXED API KEY)")
print("="*60)

# Use the corrected API key with proper encoding
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
workspace_id = "46dfb1ae-a586-4886-9136-47070c6b1b22"
email_account_id = "1a84157c-ec45-46f2-addf-35688d32d4c6"
base_url = "https://api.instantly.ai/api/v2"

# Test data
test_campaign_id = "1cd17813-4d00-4a1e-809e-5e99f7350ba8"  # Test_Fixed_Campaign_1
test_contacts = [
    {
        "to": "john.doe.fixed@example.com",
        "name": "John Doe Fixed",
        "company": "Test Company Inc",
    },
    {
        "to": "jane.smith.fixed@example.com", 
        "name": "Jane Smith Fixed",
        "company": "Example Corp",
    }
]

try:
    print(f"📋 Testing with campaign: {test_campaign_id}")
    print(f"📋 Adding {len(test_contacts)} test contacts...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    successful_leads = []
    failed_leads = []
    
    for i, contact in enumerate(test_contacts):
        try:
            print(f"\n📋 Processing contact {i+1}/{len(test_contacts)}: {contact['to']}")
            
            # Parse name
            name = contact.get("name", "").strip()
            name_parts = name.split() if name else ["", ""]
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            # Create lead data
            lead_data = {
                "email": contact["to"],
                "first_name": first_name,
                "last_name": last_name,
                "campaign": test_campaign_id,
                "skip_if_in_workspace": True,
                "skip_if_in_campaign": False,
                "skip_if_in_list": False
            }
            
            if contact.get("company"):
                lead_data["company_name"] = contact["company"]
            
            print(f"📤 Sending lead data: {lead_data}")
            
            # Add the lead
            response = requests.post(
                f"{base_url}/leads",
                headers=headers,
                json=lead_data
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Lead added successfully: {result.get('id', 'Unknown ID')}")
                successful_leads.append({
                    "email": contact["to"],
                    "lead_id": result.get("id"),
                    "status": "success"
                })
            else:
                print(f"❌ Failed to add lead: {response.status_code} - {response.text}")
                failed_leads.append({
                    "email": contact["to"],
                    "error": f"{response.status_code}: {response.text}",
                    "status": "failed"
                })
                
        except Exception as e:
            print(f"❌ Exception adding lead: {e}")
            failed_leads.append({
                "email": contact["to"],
                "error": str(e),
                "status": "failed"
            })
    
    print(f"\n✅ RESULTS:")
    print(f"   Total processed: {len(test_contacts)}")
    print(f"   Successful: {len(successful_leads)}")
    print(f"   Failed: {len(failed_leads)}")
    
    if successful_leads:
        print(f"\n🎯 SUCCESSFUL LEADS:")
        for lead in successful_leads:
            print(f"   - {lead['email']}: {lead['status']} (ID: {lead.get('lead_id')})")
    
    if failed_leads:
        print(f"\n❌ FAILED LEADS:")
        for lead in failed_leads:
            print(f"   - {lead['email']}: {lead['error']}")
    
    # Verify leads were added
    print(f"\n📋 VERIFYING LEADS WERE ADDED...")
    
    verification_request = {
        "campaign": test_campaign_id,
        "limit": 10
    }
    
    verification_response = requests.post(
        f"{base_url}/leads/list",
        headers=headers,
        json=verification_request
    )
    
    if verification_response.status_code == 200:
        verification_data = verification_response.json()
        campaign_leads = verification_data.get('items', [])
        
        print(f"✅ VERIFICATION: Found {len(campaign_leads)} leads in campaign")
        
        # Check our new test emails
        test_emails = [contact['to'] for contact in test_contacts]
        found_emails = [lead.get('email') for lead in campaign_leads if lead.get('email') in test_emails]
        
        print(f"🎯 Our test emails found: {found_emails}")
        
        if len(found_emails) == len(successful_leads):
            print("✅ SUCCESS: All successful contacts were verified in campaign!")
        else:
            print("⚠️ PARTIAL: Some contacts may not have been added or are pending")
            
    else:
        print(f"❌ Verification failed: {verification_response.status_code} - {verification_response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*60)
print("🏁 CONTACT ADDITION TEST COMPLETE")
print("="*60) 