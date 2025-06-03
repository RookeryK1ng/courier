import requests
import json
import time

# Test with a completely fresh email to avoid any duplicate issues
timestamp = int(time.time())
test_data = {
    "approved_emails": [
        {
            "to": f"test.lead.{timestamp}@example.com",
            "name": "Test User", 
            "subject": f"Test Campaign - Fresh Email Verification ({timestamp})",
            "body": f"""This is a test email to verify the lead addition system works.

Testing with fresh email: test.lead.{timestamp}@example.com
Timestamp: {timestamp}

If you receive this email, the system is working perfectly!""",
            "company": "Test Company"
        }
    ],
    "campaign_name": f"Fresh_Email_Test_{timestamp}",
    "send_mode": "instantly"
}

try:
    print("🎯 TESTING WITH COMPLETELY FRESH EMAIL")
    print("="*60)
    print(f"Fresh Email: test.lead.{timestamp}@example.com")
    print(f"Campaign: {test_data['campaign_name']}")
    print("="*60)
    
    response = requests.post(
        "http://localhost:8000/send-emails/",
        headers={"Content-Type": "application/json"},
        json=test_data
    )
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n📊 RESULTS:")
        print(f"   Total processed: {result.get('total_processed')}")
        print(f"   Successful: {result.get('successful_sends')}")
        print(f"   Failed: {result.get('failed_sends')}")
        print(f"   Campaigns activated: {result.get('campaigns_activated')}")
        
        # Check lead addition details
        for email_result in result.get('results', []):
            print(f"\n📧 EMAIL RESULTS:")
            print(f"   Status: {email_result['status']}")
            print(f"   Campaign ID: {email_result['campaign_id']}")
            
            if 'lead_addition' in email_result:
                lead_info = email_result['lead_addition']
                print(f"\n   🎯 LEAD ADDITION:")
                print(f"     - Total: {lead_info.get('total_leads')}")
                print(f"     - Successful: {lead_info.get('successful_leads')}")
                print(f"     - Failed: {lead_info.get('failed_leads')}")
                
                if lead_info.get('successful_details'):
                    for success in lead_info['successful_details']:
                        print(f"     - ✅ SUCCESS: {success.get('email')}")
                        print(f"     - ✅ Lead ID: {success.get('lead_id')}")
                
                if lead_info.get('failed_details'):
                    for failure in lead_info['failed_details']:
                        print(f"     - ❌ FAILED: {failure.get('email')}")
                        print(f"     - ❌ Error: {failure.get('error')}")
            
            if 'activation_status' in email_result:
                print(f"\n   🚀 Activation: {email_result['activation_status']}")
        
        # Summary
        campaign_ids = result.get('campaigns_created', [])
        if campaign_ids:
            campaign_id = campaign_ids[0]
            
            # Check if leads were actually added
            total_successful_leads = sum(
                email_result.get('lead_addition', {}).get('successful_leads', 0) 
                for email_result in result.get('results', [])
            )
            
            print(f"\n🎯 FINAL ASSESSMENT:")
            print(f"   ✅ Campaign Created: {campaign_id}")
            print(f"   📊 Leads Successfully Added: {total_successful_leads}")
            
            if total_successful_leads > 0:
                print(f"   🎉 SUCCESS! Leads are properly attached to campaign!")
                print(f"   ✅ System is working - check Instantly dashboard")
            else:
                print(f"   ⚠️ Campaign created but NO leads attached")
                print(f"   ❌ Lead addition still failing")
            
    else:
        print(f"❌ Request failed: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}") 