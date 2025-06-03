#!/usr/bin/env python3
"""
Diagnostic script to examine campaign structure and activation requirements
"""
import requests
import json
import os

# Configuration
BASE_URL = "https://api.instantly.ai/api/v2"
API_KEY = os.getenv("INSTANTLY_API_KEY", "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg==")

def diagnose_campaign():
    print("🔍 DIAGNOSING CAMPAIGN ACTIVATION ISSUE")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # First, let's create a minimal campaign
    print("📋 Step 1: Creating test campaign with minimal structure...")
    
    minimal_campaign = {
        "name": f"DIAGNOSTIC_TEST_{int(__import__('time').time())}",
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Business Hours",
                    "timing": {
                        "from": "09:00",
                        "to": "17:00"
                    },
                    "days": {
                        "0": False,  # Sunday
                        "1": True,   # Monday  
                        "2": True,   # Tuesday
                        "3": True,   # Wednesday
                        "4": True,   # Thursday
                        "5": True,   # Friday
                        "6": False   # Saturday
                    },
                    "timezone": "America/Chicago"
                }
            ]
        },
        "email_list": ["rob@biscred.ai"],  # Using the known working email
        "sequences": [
            {
                "steps": [
                    {
                        "day": 1,
                        "type": "email",
                        "delay": 0,
                        "variants": [
                            {
                                "subject": "Test Subject",
                                "body": "Test body content"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    try:
        # Create the campaign
        create_response = requests.post(
            f"{BASE_URL}/campaigns",
            headers=headers,
            json=minimal_campaign,
            timeout=30
        )
        
        print(f"   Campaign creation status: {create_response.status_code}")
        
        if create_response.status_code == 200:
            campaign_data = create_response.json()
            campaign_id = campaign_data.get("id")
            
            print(f"   ✅ Campaign created: {campaign_id}")
            print(f"   Initial status: {campaign_data.get('status')}")
            
            # Now examine the campaign structure
            print(f"\n📊 Step 2: Examining campaign structure...")
            get_response = requests.get(
                f"{BASE_URL}/campaigns/{campaign_id}",
                headers=headers,
                timeout=30
            )
            
            if get_response.status_code == 200:
                full_campaign = get_response.json()
                
                print(f"   📝 FULL CAMPAIGN STRUCTURE:")
                print(f"   Name: {full_campaign.get('name')}")
                print(f"   Status: {full_campaign.get('status')} (0=Draft, 1=Active, 2=Paused, 3=Completed)")
                print(f"   Email List: {full_campaign.get('email_list')}")
                
                # Check sequences
                sequences = full_campaign.get('sequences', [])
                print(f"   Sequences: {len(sequences)}")
                
                if sequences:
                    sequence = sequences[0]
                    steps = sequence.get('steps', [])
                    print(f"   Steps in sequence: {len(steps)}")
                    
                    if steps:
                        step = steps[0]
                        print(f"   Step details:")
                        print(f"     Day: {step.get('day')}")
                        print(f"     Type: {step.get('type')}")
                        print(f"     Delay: {step.get('delay')}")
                        print(f"     Variants: {len(step.get('variants', []))}")
                        
                        variants = step.get('variants', [])
                        if variants:
                            variant = variants[0]
                            print(f"     Variant subject: {variant.get('subject')}")
                            print(f"     Variant body length: {len(variant.get('body', ''))}")
                
                # Check schedule
                schedule = full_campaign.get('campaign_schedule', {})
                schedules = schedule.get('schedules', [])
                print(f"   Schedule configured: {len(schedules) > 0}")
                
                if schedules:
                    sched = schedules[0]
                    print(f"     Schedule name: {sched.get('name')}")
                    print(f"     Timezone: {sched.get('timezone')}")
                    print(f"     Days enabled: {sched.get('days')}")
                
                # Additional fields
                print(f"   Additional fields:")
                print(f"     stop_on_reply: {full_campaign.get('stop_on_reply')}")
                print(f"     text_only: {full_campaign.get('text_only')}")
                print(f"     link_tracking: {full_campaign.get('link_tracking')}")
                print(f"     open_tracking: {full_campaign.get('open_tracking')}")
                
                # Now try to activate
                print(f"\n🚀 Step 3: Attempting activation...")
                
                # Try activation with empty body (no Content-Type)
                activate_headers = {
                    "Authorization": f"Bearer {API_KEY}"
                    # No Content-Type header
                }
                
                activate_response = requests.post(
                    f"{BASE_URL}/campaigns/{campaign_id}/activate",
                    headers=activate_headers
                    # No body/json parameter
                )
                
                print(f"   Activation status: {activate_response.status_code}")
                print(f"   Activation response: {activate_response.text}")
                
                if activate_response.status_code == 200:
                    print(f"   ✅ ACTIVATION SUCCESSFUL!")
                    activation_result = activate_response.json()
                    new_status = activation_result.get('status')
                    print(f"   New campaign status: {new_status}")
                else:
                    print(f"   ❌ Activation failed")
                    if activate_response.status_code == 400:
                        print(f"   This suggests missing required fields or invalid campaign structure")
                        
                        # Let's try to identify what's missing
                        print(f"\n🔧 Step 4: Analyzing potential issues...")
                        
                        # Check if campaign has leads
                        print("   Checking if campaign needs leads first...")
                        try:
                            leads_response = requests.get(
                                f"{BASE_URL}/leads",
                                headers=headers,
                                params={"campaign": campaign_id},
                                timeout=30
                            )
                            
                            if leads_response.status_code == 200:
                                leads_data = leads_response.json()
                                leads_count = len(leads_data.get('items', []))
                                print(f"     Campaign has {leads_count} leads")
                                
                                if leads_count == 0:
                                    print(f"   ⚠️ POTENTIAL ISSUE: Campaign has no leads!")
                                    print(f"   📝 Solution: Add leads before activation")
                                    
                        except Exception as e:
                            print(f"     Error checking leads: {e}")
                            
                        # Check email account status
                        print("   Checking email account status...")
                        try:
                            account_response = requests.get(
                                f"{BASE_URL}/accounts/rob@biscred.ai",
                                headers=headers,
                                timeout=30
                            )
                            
                            if account_response.status_code == 200:
                                account_data = account_response.json()
                                account_status = account_data.get('status')
                                print(f"     Email account status: {account_status}")
                                
                                if account_status != 1:  # 1 = active
                                    print(f"   ⚠️ POTENTIAL ISSUE: Email account not active!")
                                    print(f"   📝 Solution: Activate email account first")
                                    
                        except Exception as e:
                            print(f"     Error checking account: {e}")
                
            else:
                print(f"   ❌ Failed to get campaign details: {get_response.status_code}")
                
        else:
            print(f"   ❌ Campaign creation failed: {create_response.status_code}")
            print(f"   Response: {create_response.text}")
            
    except Exception as e:
        print(f"❌ Error in diagnosis: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n" + "="*60)
    print(f"🎯 DIAGNOSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    diagnose_campaign() 