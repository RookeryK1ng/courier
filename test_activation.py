#!/usr/bin/env python3
"""
Simple test to verify campaign activation functionality
"""
import requests
import json
import time

VERCEL_URL = "https://sender-sigma.vercel.app"

def test_activation():
    print("🚀 TESTING CAMPAIGN ACTIVATION")
    print("="*50)
    
    # Create a simple test campaign
    csv_content = '''name,email,company
Activation Test,activation.test@example.com,Test Corp'''
    
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    data = {
        'campaign_content': 'Testing campaign activation functionality.',
        'sender_name': 'Test Sender', 
        'sender_title': 'Test Manager',
        'sender_company': 'Test Company'
    }
    
    try:
        # Step 1: Generate emails
        print("📧 Step 1: Generating emails...")
        response = requests.post(f"{VERCEL_URL}/generate-emails/", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Email generation failed: {response.status_code}")
            print(response.text)
            return
            
        email_data = response.json()
        generated_emails = email_data.get('emails', [])
        
        if not generated_emails:
            print("❌ No emails generated")
            return
            
        print(f"✅ Generated {len(generated_emails)} emails")
        
        # Step 2: Send emails (creates campaign and should activate)
        print("📤 Step 2: Sending emails and creating campaign...")
        send_request = {
            "approved_emails": generated_emails,
            "campaign_name": f"ACTIVATION_TEST_{int(time.time())}",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_request, timeout=60)
        
        if send_response.status_code != 200:
            print(f"❌ Send failed: {send_response.status_code}")
            print(send_response.text)
            return
            
        result = send_response.json()
        
        # Analyze results
        print(f"\n📊 RESULTS:")
        print(f"   Mode: {result.get('mode')}")
        print(f"   Total Processed: {result.get('total_processed')}")
        print(f"   Successful: {result.get('successful_sends')}")
        print(f"   Failed: {result.get('failed_sends')}")
        print(f"   Campaigns Created: {len(result.get('campaigns_created', []))}")
        print(f"   Campaigns Activated: {result.get('campaigns_activated', 0)}")
        
        # Get campaign ID
        campaign_id = None
        results = result.get('results', [])
        if results:
            campaign_id = results[0].get('campaign_id')
            activation_status = results[0].get('activation_status')
            activation_message = results[0].get('activation_message')
            
            print(f"\n🎯 ACTIVATION DETAILS:")
            print(f"   Campaign ID: {campaign_id}")
            print(f"   Activation Status: {activation_status}")
            print(f"   Message: {activation_message}")
            
            if activation_status == 'success':
                print(f"   ✅ AUTOMATIC ACTIVATION SUCCESSFUL!")
            else:
                print(f"   ❌ Automatic activation failed")
                
                # Step 3: Try manual activation
                if campaign_id:
                    print(f"\n🔧 Step 3: Trying manual activation...")
                    try:
                        activation_response = requests.post(
                            f"{VERCEL_URL}/activate-campaign/",
                            json=campaign_id,
                            timeout=30
                        )
                        
                        if activation_response.status_code == 200:
                            print(f"   ✅ MANUAL ACTIVATION SUCCESSFUL!")
                            activation_result = activation_response.json()
                            print(f"   Result: {json.dumps(activation_result, indent=2)}")
                        else:
                            print(f"   ❌ Manual activation failed: {activation_response.status_code}")
                            print(f"   Response: {activation_response.text}")
                            
                    except Exception as e:
                        print(f"   ❌ Manual activation error: {e}")
        
        # Step 4: Check final campaign status
        if campaign_id:
            print(f"\n🔍 Step 4: Checking final campaign status...")
            try:
                status_response = requests.post(
                    f"{VERCEL_URL}/campaign-status/", 
                    json=campaign_id,
                    timeout=30
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    campaign_status = status_data.get('status', {}).get('status')
                    print(f"   Campaign Status Code: {campaign_status}")
                    
                    # Status codes: 1 = active, 2 = paused, 3 = draft
                    if campaign_status == 1:
                        print(f"   ✅ CAMPAIGN IS ACTIVE AND READY TO SEND!")
                    elif campaign_status == 3:
                        print(f"   ⚠️ Campaign is still in draft mode")
                    elif campaign_status == 2:
                        print(f"   ⏸️ Campaign is paused")
                    else:
                        print(f"   ❓ Unknown status: {campaign_status}")
                        
                else:
                    print(f"   ❌ Status check failed: {status_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Status check error: {e}")
        
        print(f"\n" + "="*50)
        print(f"🎯 ACTIVATION SUMMARY:")
        
        if result.get('campaigns_activated', 0) > 0:
            print(f"✅ AUTOMATIC ACTIVATION IS WORKING!")
            print(f"✅ Your campaigns are being activated automatically")
            print(f"✅ No manual intervention needed")
        else:
            print(f"⚠️ Automatic activation needs attention")
            print(f"🔧 Manual activation endpoint: /activate-campaign/")
            print(f"🔧 Or activate manually in Instantly dashboard")
            
        print("="*50)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_activation() 