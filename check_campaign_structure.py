import requests
import json

# Check the exact campaign structure that was created
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
base_url = "https://api.instantly.ai/api/v2"
campaign_id = "78982524-cc8c-4e0e-99ef-7ecf99bbf76e"  # From the recent test

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔍 CHECKING PRODUCTION CAMPAIGN STRUCTURE")
print("="*55)
print(f"Campaign ID: {campaign_id}")

try:
    # Get the campaign details to see what was actually created
    response = requests.get(f"{base_url}/campaigns/{campaign_id}", headers=headers)
    
    if response.status_code == 200:
        campaign_data = response.json()
        print(f"✅ Campaign data retrieved successfully")
        
        # Analyze the campaign structure
        print(f"\n📊 CAMPAIGN ANALYSIS:")
        print(f"   Name: {campaign_data.get('name')}")
        print(f"   Status: {campaign_data.get('status')}")
        print(f"   Email List: {campaign_data.get('email_list', [])}")
        
        # Check if email list contains rob@biscred.ai
        email_list = campaign_data.get('email_list', [])
        if 'rob@biscred.ai' in email_list:
            print(f"   ✅ Using Rob's account: rob@biscred.ai")
        elif 'tim@biscred.com' in email_list:
            print(f"   ❌ Still using old account: tim@biscred.com")
            print(f"   🔧 Environment variable not updated!")
        else:
            print(f"   ⚠️ Unknown email account: {email_list}")
        
        # Check sequence structure
        sequences = campaign_data.get('sequences', [])
        print(f"\n📧 SEQUENCE ANALYSIS:")
        print(f"   Number of sequences: {len(sequences)}")
        
        for i, sequence in enumerate(sequences):
            steps = sequence.get('steps', [])
            print(f"   Sequence {i+1} - Steps: {len(steps)}")
            
            for j, step in enumerate(steps):
                print(f"     Step {j+1}:")
                print(f"       Subject: {step.get('subject', 'MISSING')[:50]}...")
                print(f"       Day: {step.get('day', 'MISSING')}")
                print(f"       Type: {step.get('type', 'MISSING')}")
                print(f"       Delay: {step.get('delay', 'MISSING')}")
                print(f"       Variants: {len(step.get('variants', []))}")
                
                # Check for missing required fields
                required_fields = ['day', 'type', 'delay', 'variants']
                missing_fields = [field for field in required_fields if field not in step]
                if missing_fields:
                    print(f"       ❌ MISSING FIELDS: {missing_fields}")
                else:
                    print(f"       ✅ All required fields present")
        
        # Check schedule
        schedule = campaign_data.get('campaign_schedule', {})
        print(f"\n📅 SCHEDULE ANALYSIS:")
        print(f"   Schedule present: {'✅' if schedule else '❌'}")
        if schedule:
            schedules = schedule.get('schedules', [])
            if schedules:
                first_schedule = schedules[0]
                print(f"   Timezone: {first_schedule.get('timezone', 'MISSING')}")
                print(f"   Days configured: {first_schedule.get('days', 'MISSING')}")
        
        # Now try activation again with better error handling
        print(f"\n🧪 TESTING ACTIVATION AGAIN:")
        activation_response = requests.post(
            f"{base_url}/campaigns/{campaign_id}/activate",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        print(f"   Status: {activation_response.status_code}")
        print(f"   Response: {activation_response.text}")
        
        if activation_response.status_code == 400:
            print(f"\n❌ ACTIVATION FAILS WITH 400 BAD REQUEST")
            print(f"🔧 POSSIBLE ISSUES:")
            print(f"   1. Email account not properly configured in Instantly")
            print(f"   2. Campaign missing required fields")
            print(f"   3. Workspace sending limits not configured")
            print(f"   4. Campaign sequence structure invalid")
            
    else:
        print(f"❌ Failed to get campaign: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error checking campaign: {e}")

print(f"\n" + "="*55)
print(f"🎯 CAMPAIGN STRUCTURE CHECK COMPLETE")
print("="*55) 