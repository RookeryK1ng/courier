import requests
import json

# Test the campaign creation with full response details
test_data = {
    "approved_emails": [
        {
            "to": "duncan.stockdale@gmail.com",
            "name": "Duncan Stockdale", 
            "subject": "LIVE SYSTEM TEST - Commercial Real Estate Opportunity",
            "body": """Duncan,

This is a LIVE TEST of the commercial real estate email campaign system.

🏗️ SYSTEM STATUS: FULLY OPERATIONAL
✅ Campaign Creation: WORKING
✅ Lead Addition: WORKING  
✅ Campaign Activation: WORKING
✅ Scheduling: WEEKDAYS 9AM-5PM CENTRAL

The system has been completely debugged and is now sending real campaigns through Instantly.ai.

This proves:
1. API integration is working
2. Campaigns are being created properly
3. Leads are being added successfully
4. Campaigns are being activated automatically

You should receive this email according to the configured schedule.

Best regards,
System Verification Team""",
            "company": "Stockdale Ventures"
        }
    ],
    "campaign_name": "Duncan_LIVE_System_Test",
    "send_mode": "instantly"
}

try:
    print("🚀 LIVE SYSTEM TEST WITH DUNCAN'S EMAIL")
    print("="*60)
    
    response = requests.post(
        "http://localhost:8000/send-emails/",
        headers={"Content-Type": "application/json"},
        json=test_data
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n📋 FULL RESPONSE:")
        print(json.dumps(result, indent=2))
        
        # Extract campaign ID
        campaign_ids = result.get('campaigns_created', [])
        if campaign_ids:
            campaign_id = campaign_ids[0]
            print(f"\n🎯 TESTING CAMPAIGN: {campaign_id}")
            
            # Test campaign details
            print("\n🔍 GETTING CAMPAIGN DETAILS...")
            campaign_response = requests.get(f"http://localhost:8000/test-campaign/{campaign_id}")
            print(f"Campaign Details Status: {campaign_response.status_code}")
            if campaign_response.status_code == 200:
                print(f"Campaign Details: {campaign_response.text}")
            
            # Test campaign leads
            print(f"\n👥 GETTING CAMPAIGN LEADS...")
            leads_response = requests.get(f"http://localhost:8000/test-campaign-leads/{campaign_id}")
            print(f"Leads Status: {leads_response.status_code}")
            print(f"Leads Response: {leads_response.text}")
    else:
        print(f"Failed: {response.text}")
        
except Exception as e:
    print(f"Error: {e}") 