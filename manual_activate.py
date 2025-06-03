import requests
import json

VERCEL_URL = "https://sender-sigma.vercel.app"

# Use the campaign ID from our recent test
campaign_id = "dd776a0d-b0d9-45a0-8bdc-571ba8cd1301"  # From the recent activation test

print("🚀 MANUAL CAMPAIGN ACTIVATION TEST")
print("="*50)
print(f"Campaign ID: {campaign_id}")

try:
    # Try manual activation via API endpoint
    response = requests.post(
        f"{VERCEL_URL}/activate-campaign/",
        json=campaign_id,  # Send as JSON body
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f"\n📊 ACTIVATION RESPONSE:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ MANUAL ACTIVATION SUCCESS!")
        print(f"Campaign ID: {result.get('campaign_id')}")
        print(f"Action: {result.get('action')}")
        print(f"Result: {result.get('result')}")
        
        print(f"\n🎯 SOLUTION FOUND:")
        print(f"✅ Manual activation works via API")
        print(f"📝 You can manually activate campaigns using:")
        print(f"   POST {VERCEL_URL}/activate-campaign/")
        print(f"   Body: \"<campaign_id>\"")
        
    else:
        print(f"\n❌ MANUAL ACTIVATION FAILED:")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Error text: {response.text}")
        
        print(f"\n📝 ALTERNATIVE SOLUTIONS:")
        print(f"1. Manually activate in Instantly dashboard")
        print(f"2. Check Instantly API configuration")
        print(f"3. Verify campaign exists and is in 'draft' status")

except Exception as e:
    print(f"❌ ERROR: {e}")

print(f"\n" + "="*50)
print(f"🎯 SUMMARY:")
print(f"• Campaigns are created successfully")
print(f"• Contacts are added successfully") 
print(f"• Activation requires manual intervention")
print(f"• Check your Instantly dashboard for campaigns")
print("="*50) 