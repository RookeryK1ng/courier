import requests
import json
import os
from instantly_client import InstantlyClient

def test_deployment_api():
    """Test the deployed API endpoints"""
    
    print("🔍 TESTING DEPLOYED API")
    print("="*60)
    
    # You'll need to replace this with your actual Vercel URL
    # base_url = "https://your-app-name.vercel.app"  # Replace with your actual URL
    # For now, let's test locally to compare
    base_url = "http://localhost:8000"  # Change this to your Vercel URL
    
    print(f"Testing API at: {base_url}")
    
    # Test 1: Health check
    print("\n📋 TEST 1: Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            print(f"OpenAI configured: {data.get('openai_configured')}")
            print(f"Instantly configured: {data.get('instantly_configured')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Try to send a test email
    print("\n📋 TEST 2: Test Email Sending")
    try:
        test_emails = [
            {
                "to": "deployment.debug@example.com",
                "name": "Deployment Debug",
                "company": "Test Corp",
                "subject": "Deployment Debug Test",
                "body": "This is a test email to debug deployment issues."
            }
        ]
        
        response = requests.post(
            f"{base_url}/send-emails/",
            json={
                "approved_emails": test_emails,
                "campaign_name": "Debug_Deployment_Test",
                "send_mode": "instantly"
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email sending response:")
            print(f"   Mode: {data.get('mode')}")
            print(f"   Total processed: {data.get('total_processed')}")
            print(f"   Successful: {data.get('successful_sends')}")
            print(f"   Failed: {data.get('failed_sends')}")
            
            if data.get('results'):
                for result in data['results']:
                    print(f"   - {result.get('to')}: {result.get('status')} - {result.get('message')}")
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        print(f"     Lead addition - Success: {lead_info.get('successful_leads')}, Failed: {lead_info.get('failed_leads')}")
                        if lead_info.get('failed_details'):
                            for failure in lead_info['failed_details']:
                                print(f"     ❌ Lead failure: {failure.get('email')} - {failure.get('error')}")
        
    except Exception as e:
        print(f"❌ Email sending test failed: {e}")

def test_local_client():
    """Test the local InstantlyClient directly"""
    
    print("\n" + "="*60)
    print("🔍 TESTING LOCAL CLIENT DIRECTLY")
    print("="*60)
    
    client = InstantlyClient()
    
    print(f"API Key (last 10 chars): ...{client.api_key[-10:] if client.api_key else 'None'}")
    print(f"Is configured: {client.is_configured()}")
    
    # Test creating a campaign
    try:
        print("\n📋 Creating test campaign...")
        campaign_id = client.create_campaign(
            "Direct_Client_Test", 
            "Direct Test Subject", 
            "Direct test body"
        )
        print(f"✅ Campaign created: {campaign_id}")
        
        # Test adding a contact
        print("\n📋 Adding test contact...")
        test_contacts = [{
            "to": "direct.client.test@example.com",
            "name": "Direct Client Test",
            "company": "Direct Test Corp"
        }]
        
        result = client.add_leads_to_campaign(campaign_id, test_contacts)
        print(f"✅ Contact addition result:")
        print(f"   Total: {result.get('total_leads')}")
        print(f"   Successful: {result.get('successful_leads')}")
        print(f"   Failed: {result.get('failed_leads')}")
        
        if result.get('failed_details'):
            for failure in result['failed_details']:
                print(f"   ❌ Failure: {failure.get('email')} - {failure.get('error')}")
                
    except Exception as e:
        print(f"❌ Direct client test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_local_client()
    
    print("\n" + "="*60)
    print("📝 NEXT STEPS:")
    print("="*60)
    print("1. Update the base_url in this script to your Vercel deployment URL")
    print("2. Run: python test_deployment_debug.py")
    print("3. Compare local vs deployment results")
    print("4. Check the specific error messages")
    print("\nYour Vercel URL should look like: https://your-app-name.vercel.app") 