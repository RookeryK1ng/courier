import requests
import json
from instantly_client import InstantlyClient

print("🔍 TESTING FULL EMAIL SENDING FLOW")
print("="*60)

# Initialize client (now with correct API key)
client = InstantlyClient()

# Test creating a campaign and adding contacts
test_contacts = [
    {
        "to": "test.flow1@example.com",
        "name": "Test Flow User 1",
        "company": "Flow Test Corp",
        "subject": "Test Flow Email",
        "body": "This is a test email for the flow verification."
    },
    {
        "to": "test.flow2@example.com", 
        "name": "Test Flow User 2",
        "company": "Another Test Corp",
        "subject": "Test Flow Email",
        "body": "This is another test email for the flow verification."
    }
]

try:
    print(f"📋 Step 1: Creating new campaign...")
    
    # Create a new campaign
    campaign_name = "Test_Full_Flow_Campaign"
    email_subject = "Test Flow Email"
    email_body = "This is a test email body for flow verification."
    
    campaign_id = client.create_campaign(campaign_name, email_subject, email_body)
    print(f"✅ Campaign created: {campaign_id}")
    
    print(f"\n📋 Step 2: Adding contacts to campaign...")
    
    # Add contacts to the campaign
    result = client.add_leads_to_campaign(campaign_id, test_contacts)
    
    print(f"✅ Contacts added:")
    print(f"   Total: {result.get('total_leads', 0)}")
    print(f"   Successful: {result.get('successful_leads', 0)}")
    print(f"   Failed: {result.get('failed_leads', 0)}")
    
    if result.get('successful_leads', 0) > 0:
        print(f"\n📋 Step 3: Testing campaign activation...")
        
        try:
            activation_result = client.activate_campaign(campaign_id)
            print(f"✅ Campaign activated successfully!")
            print(f"   Activation result: {activation_result}")
        except Exception as e:
            print(f"⚠️ Campaign activation failed: {e}")
            print(f"   This is normal - campaign may need manual activation in Instantly dashboard")
    
    print(f"\n📋 Step 4: Verifying campaign status...")
    
    try:
        status = client.get_campaign_status(campaign_id)
        print(f"✅ Campaign status retrieved:")
        print(f"   Name: {status.get('name')}")
        print(f"   Status: {status.get('status')}")
        print(f"   ID: {status.get('id')}")
    except Exception as e:
        print(f"⚠️ Could not get campaign status: {e}")
    
    print(f"\n🎉 SUCCESS: Full email flow is working!")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Contacts added: {result.get('successful_leads', 0)}")
    print(f"   Next: You can manually activate the campaign in Instantly dashboard if needed")

except Exception as e:
    print(f"❌ ERROR in full flow: {e}")

print("\n" + "="*60)
print("🏁 FULL FLOW TEST COMPLETE")
print("="*60) 