import requests
import json

def debug_vercel_lead_addition():
    """Debug lead addition in Vercel deployment"""
    
    print("🔍 DEBUGGING VERCEL LEAD ADDITION")
    print("="*60)
    
    # Ask for Vercel URL
    vercel_url = input("Enter your Vercel URL (e.g., https://your-app.vercel.app): ").strip()
    
    if not vercel_url.startswith('http'):
        vercel_url = f"https://{vercel_url}"
    
    print(f"Testing: {vercel_url}")
    
    try:
        # Step 1: Check health
        print("\n📋 STEP 1: Health Check")
        health_response = requests.get(f"{vercel_url}/health")
        print(f"Health status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Instantly configured: {health_data.get('instantly_configured')}")
            
            if not health_data.get('instantly_configured'):
                print("❌ FOUND THE ISSUE: Instantly is not configured in deployment!")
                print("Check your environment variables in Vercel dashboard.")
                return
        else:
            print(f"❌ Health check failed: {health_response.text}")
            return
        
        # Step 2: Test with a very simple email
        print("\n📋 STEP 2: Testing Simple Email Sending")
        
        test_email = {
            "to": "vercel.debug.test@example.com",
            "name": "Vercel Debug Test",
            "company": "Debug Corp",
            "subject": "Vercel Lead Addition Debug",
            "body": "This is a test email to debug lead addition in Vercel deployment."
        }
        
        send_request = {
            "approved_emails": [test_email],
            "campaign_name": f"Vercel_Debug_Test_{int(__import__('time').time())}",
            "send_mode": "instantly"
        }
        
        print(f"Sending request: {json.dumps(send_request, indent=2)}")
        
        send_response = requests.post(
            f"{vercel_url}/send-emails/",
            json=send_request,
            headers={"Content-Type": "application/json"},
            timeout=60  # Give it more time
        )
        
        print(f"\nResponse status: {send_response.status_code}")
        print(f"Response headers: {dict(send_response.headers)}")
        
        if send_response.status_code == 200:
            response_data = send_response.json()
            print(f"\n✅ Email sending response:")
            print(f"   Mode: {response_data.get('mode')}")
            print(f"   Total processed: {response_data.get('total_processed')}")
            print(f"   Successful: {response_data.get('successful_sends')}")
            print(f"   Failed: {response_data.get('failed_sends')}")
            
            # Detailed analysis of results
            if response_data.get('results'):
                for result in response_data['results']:
                    print(f"\n📧 Email result for {result.get('to')}:")
                    print(f"   Status: {result.get('status')}")
                    print(f"   Message: {result.get('message')}")
                    print(f"   Campaign ID: {result.get('campaign_id')}")
                    
                    # Check lead addition details
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        print(f"   🎯 LEAD ADDITION DETAILS:")
                        print(f"      Total leads: {lead_info.get('total_leads')}")
                        print(f"      Successful: {lead_info.get('successful_leads')}")
                        print(f"      Failed: {lead_info.get('failed_leads')}")
                        
                        if lead_info.get('successful_details'):
                            print(f"      ✅ Successful leads:")
                            for success in lead_info['successful_details']:
                                print(f"         - {success.get('email')}: {success.get('status')} (ID: {success.get('lead_id')})")
                        
                        if lead_info.get('failed_details'):
                            print(f"      ❌ FAILED LEADS:")
                            for failure in lead_info['failed_details']:
                                print(f"         - {failure.get('email')}: {failure.get('error')}")
                                print(f"         - Response: {failure.get('response', 'No response details')}")
                    else:
                        print(f"   ⚠️ NO LEAD ADDITION INFO IN RESPONSE")
                    
                    # Check activation details
                    if 'activation' in result:
                        activation_info = result['activation']
                        print(f"   🚀 ACTIVATION DETAILS:")
                        print(f"      Status: {result.get('activation_status')}")
                        print(f"      Message: {result.get('activation_message')}")
                        if activation_info.get('error'):
                            print(f"      Error: {activation_info.get('error')}")
            
            # Check if the issue is mode fallback
            if response_data.get('mode') == 'simulation':
                print(f"\n❌ ISSUE FOUND: Running in simulation mode!")
                print(f"   This means Instantly integration failed and fell back to simulation.")
                print(f"   Check the Vercel function logs for the actual error.")
        
        else:
            print(f"❌ Email sending failed with status {send_response.status_code}")
            print(f"Response: {send_response.text}")
            
            # Try to parse error details
            try:
                error_data = send_response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check if Vercel function is taking too long.")
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_vercel_lead_addition() 