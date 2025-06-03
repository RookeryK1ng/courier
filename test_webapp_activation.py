#!/usr/bin/env python3
"""
Test the full webapp flow to verify campaign activation works in production
"""
import requests
import json
import time

VERCEL_URL = "https://sender-sigma.vercel.app"

def test_webapp_activation():
    print("🌐 TESTING WEBAPP CAMPAIGN ACTIVATION")
    print("="*60)
    
    # Create test data
    csv_content = '''name,email,company
WEBAPP Test User,webapp.activation.test@example.com,WebApp Test Corp'''
    
    files = {'file': ('webapp_test.csv', csv_content, 'text/csv')}
    data = {
        'campaign_content': 'Testing webapp automatic campaign activation functionality. This campaign should be automatically activated after contacts are loaded.',
        'sender_name': 'WebApp Tester',
        'sender_title': 'Activation Test Manager', 
        'sender_company': 'WebApp Test Company'
    }
    
    try:
        # Step 1: Generate emails
        print("📧 Step 1: Generating emails via webapp...")
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
        
        # Step 2: Send emails (this should now activate campaigns automatically)
        print("📤 Step 2: Sending emails through webapp...")
        send_request = {
            "approved_emails": generated_emails,
            "campaign_name": f"WEBAPP_ACTIVATION_TEST_{int(time.time())}",
            "send_mode": "instantly"
        }
        
        send_response = requests.post(f"{VERCEL_URL}/send-emails/", json=send_request, timeout=90)
        
        if send_response.status_code != 200:
            print(f"❌ Send failed: {send_response.status_code}")
            print(send_response.text)
            return
            
        result = send_response.json()
        
        # Analyze results
        print(f"\n📊 WEBAPP RESULTS:")
        print(f"   Mode: {result.get('mode')}")
        print(f"   Total Processed: {result.get('total_processed')}")
        print(f"   Successful: {result.get('successful_sends')}")
        print(f"   Failed: {result.get('failed_sends')}")
        print(f"   Campaigns Created: {len(result.get('campaigns_created', []))}")
        print(f"   Campaigns Activated: {result.get('campaigns_activated', 0)}")
        
        # Check individual campaign results
        campaigns_created = result.get('campaigns_created', [])
        results = result.get('results', [])
        
        print(f"\n🎯 ACTIVATION ANALYSIS:")
        campaigns_activated = result.get('campaigns_activated', 0)
        
        if campaigns_activated > 0:
            print(f"   ✅ SUCCESS: {campaigns_activated} campaign(s) were automatically activated!")
            
            # Show campaign details
            for i, contact_result in enumerate(results, 1):
                campaign_id = contact_result.get('campaign_id')
                activation_status = contact_result.get('activation_status')
                activation_message = contact_result.get('activation_message')
                
                print(f"\n   📋 Contact {i}: {contact_result.get('to')}")
                print(f"      Campaign ID: {campaign_id}")
                print(f"      Activation Status: {activation_status}")
                print(f"      Message: {activation_message}")
                
                if activation_status == 'success':
                    print(f"      ✅ This campaign is ACTIVE and ready to send!")
                    
                    # Verify with status check
                    if campaign_id:
                        print(f"   🔍 Verifying campaign status...")
                        try:
                            status_response = requests.post(
                                f"{VERCEL_URL}/campaign-status/",
                                json=campaign_id,
                                timeout=30
                            )
                            
                            if status_response.status_code == 200:
                                status_data = status_response.json()
                                campaign_status = status_data.get('status', {}).get('status')
                                print(f"      Verified Status: {campaign_status} (1=Active)")
                                
                                if campaign_status == 1:
                                    print(f"      🎉 CONFIRMED: Campaign is ACTIVE in Instantly!")
                                else:
                                    print(f"      ⚠️ Unexpected status: {campaign_status}")
                            else:
                                print(f"      ❌ Status check failed: {status_response.status_code}")
                                
                        except Exception as e:
                            print(f"      ❌ Status check error: {e}")
                
        else:
            print(f"   ❌ No campaigns were activated automatically")
            
            # Show details of what went wrong
            for i, contact_result in enumerate(results, 1):
                activation_details = contact_result.get('activation')
                if activation_details and activation_details.get('error'):
                    print(f"   📋 Contact {i} activation error: {activation_details.get('error')}")
                    print(f"      Status: {activation_details.get('status')}")
                    print(f"      Message: {activation_details.get('message')}")
        
        print(f"\n" + "="*60)
        print(f"🎯 WEBAPP ACTIVATION TEST SUMMARY:")
        
        if result.get('campaigns_activated', 0) > 0:
            print(f"✅ SUCCESS: Webapp automatic activation is WORKING!")
            print(f"✅ {result.get('campaigns_activated')} campaign(s) activated automatically")
            print(f"✅ Your webapp now activates campaigns after loading contacts")
            print(f"✅ Users can send emails immediately without manual activation")
        else:
            print(f"❌ Webapp activation needs attention")
            print(f"📝 Check campaign creation and activation logic")
            
        print("="*60)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_webapp_activation() 