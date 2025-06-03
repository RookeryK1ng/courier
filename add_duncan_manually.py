import requests
import json

# Duncan's campaign details
campaign_id = "20bdaa54-d3cb-4966-9aec-80754e66a440"
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg"
base_url = "https://api.instantly.ai/api/v2"

print("🎯 MANUALLY ADDING DUNCAN TO CAMPAIGN AND ACTIVATING")
print("="*60)
print(f"Campaign ID: {campaign_id}")
print(f"Email: duncan.stockdale@gmail.com")

try:
    # Add Duncan as a lead
    print("\n👤 ADDING DUNCAN AS LEAD...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    lead_data = {
        "email": "duncan.stockdale@gmail.com",
        "first_name": "Duncan",
        "last_name": "Stockdale",
        "campaign": campaign_id,
        "company_name": "Stockdale Ventures"
    }
    
    print(f"Lead Data: {lead_data}")
    
    lead_response = requests.post(
        f"{base_url}/leads",
        headers=headers,
        json=lead_data
    )
    
    print(f"Lead Addition Status: {lead_response.status_code}")
    print(f"Lead Response: {lead_response.text}")
    
    if lead_response.status_code == 200:
        lead_result = lead_response.json()
        lead_id = lead_result.get('id')
        print(f"✅ LEAD ADDED SUCCESSFULLY: {lead_id}")
        
        # Now activate the campaign
        print(f"\n🚀 ACTIVATING CAMPAIGN...")
        activation_headers = {
            "Authorization": f"Bearer {api_key}"
            # No Content-Type for activation
        }
        
        activation_response = requests.post(
            f"{base_url}/campaigns/{campaign_id}/activate",
            headers=activation_headers
        )
        
        print(f"Activation Status: {activation_response.status_code}")
        print(f"Activation Response: {activation_response.text}")
        
        if activation_response.status_code == 200:
            activation_result = activation_response.json()
            print(f"\n🎉 CAMPAIGN ACTIVATED SUCCESSFULLY!")
            print(f"Campaign Status: {activation_result.get('status')} (1 = Active)")
            print(f"Campaign Name: {activation_result.get('name')}")
            print(f"Updated: {activation_result.get('timestamp_updated')}")
            
            print(f"\n✅ PROOF OF WORKING SYSTEM:")
            print(f"   📧 Duncan's Email: duncan.stockdale@gmail.com")
            print(f"   🆔 Campaign ID: {campaign_id}")
            print(f"   👤 Lead ID: {lead_id}")
            print(f"   🚀 Status: ACTIVE")
            print(f"   ⏰ Schedule: Weekdays 9AM-5PM Central")
            print(f"   📬 Will send according to Instantly schedule")
            
        else:
            print(f"❌ Activation failed: {activation_response.text}")
            
    else:
        print(f"❌ Lead addition failed: {lead_response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}") 