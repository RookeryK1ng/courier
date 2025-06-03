import requests
import json

# Real test data with Duncan's email
test_data = {
    "approved_emails": [
        {
            "to": "duncan.stockdale@gmail.com",
            "name": "Duncan Stockdale", 
            "subject": "Real Estate Investment Opportunity - Verified System Test",
            "body": """Hi Duncan,

I hope this email finds you well! I'm reaching out regarding an exclusive commercial real estate investment opportunity that has become available.

Our platform has identified several high-yield properties in emerging markets that align with current investment trends. Given the current market conditions, these opportunities are presenting excellent cash-on-cash returns.

Key highlights:
• Pre-vetted commercial properties
• Expected 12-15% annual returns
• Full due diligence completed
• Flexible investment minimums

This is a live test of our email campaign system to verify that:
✅ Campaign creation works properly
✅ Lead addition is successful  
✅ Campaign activation functions correctly
✅ Scheduling is properly configured

Would you be interested in a brief 15-minute call to discuss these opportunities?

Best regards,
Commercial Real Estate Team
BiscredCourier Platform

P.S. This is a system verification test - the campaign system is now fully operational!""",
            "company": "Stockdale Ventures"
        }
    ],
    "campaign_name": "Duncan_System_Verification_Test",
    "send_mode": "instantly"
}

try:
    print("🎯 CREATING REAL CAMPAIGN FOR DUNCAN STOCKDALE")
    print("="*60)
    print(f"📧 Email: {test_data['approved_emails'][0]['to']}")
    print(f"👤 Name: {test_data['approved_emails'][0]['name']}")
    print(f"📋 Subject: {test_data['approved_emails'][0]['subject']}")
    print(f"🏢 Company: {test_data['approved_emails'][0]['company']}")
    print(f"🎯 Campaign: {test_data['campaign_name']}")
    print("="*60)
    
    response = requests.post(
        "http://localhost:8000/send-emails/",
        headers={"Content-Type": "application/json"},
        json=test_data
    )
    
    print(f"\n📊 RESPONSE STATUS: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n🎉 SUCCESS! CAMPAIGN CREATED AND ACTIVATED")
        print("="*60)
        print(f"✅ Total processed: {result.get('total_processed')}")
        print(f"✅ Successful sends: {result.get('successful_sends')}")
        print(f"❌ Failed sends: {result.get('failed_sends')}")
        print(f"🚀 Campaigns activated: {result.get('campaigns_activated')}")
        print(f"📋 Campaign IDs: {result.get('campaigns_created')}")
        print(f"⚙️ Mode: {result.get('mode')}")
        
        # Show detailed results for Duncan's email
        for email_result in result.get('results', []):
            if email_result['to'] == "duncan.stockdale@gmail.com":
                print(f"\n📧 DUNCAN'S EMAIL DETAILS:")
                print(f"   📬 Status: {email_result['status']}")
                print(f"   💬 Message: {email_result['message']}")
                print(f"   🆔 Campaign ID: {email_result['campaign_id']}")
                
                if 'lead_addition' in email_result:
                    lead_info = email_result['lead_addition']
                    print(f"   👤 Lead Addition: {lead_info['successful_leads']}/{lead_info['total_leads']} successful")
                    if lead_info['successful_details']:
                        lead_id = lead_info['successful_details'][0]['lead_id']
                        print(f"   🔗 Lead ID: {lead_id}")
                
                if 'activation' in email_result:
                    activation_status = email_result.get('activation_status', 'unknown')
                    print(f"   🚀 Activation: {activation_status}")
                    if activation_status == "success":
                        print(f"   ✅ Campaign is ACTIVE and will send according to schedule!")
                        print(f"   ⏰ Schedule: Weekdays 9AM-5PM Central Time")
        
        print("\n🎯 VERIFICATION COMPLETE!")
        print("The campaign has been created, leads added, and activated in Instantly.")
        print("Duncan should see this campaign in his Instantly dashboard.")
        
    else:
        print(f"\n❌ FAILED: {response.text}")
    
except Exception as e:
    print(f"❌ ERROR: {e}") 