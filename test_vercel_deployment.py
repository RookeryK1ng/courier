import requests
import json

def test_vercel_deployment(vercel_url):
    """Test the Vercel deployment"""
    
    print(f"🔍 TESTING VERCEL DEPLOYMENT: {vercel_url}")
    print("="*60)
    
    try:
        # Test 1: Health check
        print("📋 TEST 1: Health Check")
        response = requests.get(f"{vercel_url}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed:")
            print(f"   OpenAI configured: {data.get('openai_configured')}")
            print(f"   Instantly configured: {data.get('instantly_configured')}")
            
            if not data.get('instantly_configured'):
                print("❌ ISSUE FOUND: Instantly is not configured in deployment!")
                return False
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
        
        # Test 2: Simple email sending test
        print("\n📋 TEST 2: Email Sending Test")
        test_emails = [
            {
                "to": "vercel.test@example.com",
                "name": "Vercel Test",
                "company": "Test Corp",
                "subject": "Vercel Deployment Test",
                "body": "Testing the Vercel deployment."
            }
        ]
        
        response = requests.post(
            f"{vercel_url}/send-emails/",
            json={
                "approved_emails": test_emails,
                "campaign_name": "Vercel_Test_Campaign",
                "send_mode": "instantly"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email sending test response:")
            print(f"   Mode: {data.get('mode')}")
            print(f"   Total processed: {data.get('total_processed')}")
            print(f"   Successful: {data.get('successful_sends')}")
            print(f"   Failed: {data.get('failed_sends')}")
            
            # Check for specific failures
            if data.get('results'):
                for result in data['results']:
                    print(f"   - {result.get('to')}: {result.get('status')}")
                    if result.get('status') == 'failed':
                        print(f"     ❌ Error: {result.get('message')}")
                    if 'lead_addition' in result:
                        lead_info = result['lead_addition']
                        if lead_info.get('failed_leads', 0) > 0:
                            print(f"     ❌ Lead addition failed:")
                            for failure in lead_info.get('failed_details', []):
                                print(f"       - {failure.get('email')}: {failure.get('error')}")
                        
        else:
            print(f"❌ Email sending failed: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Vercel Deployment Tester")
    print("="*60)
    print("Please enter your Vercel deployment URL:")
    print("Example: https://your-app-name.vercel.app")
    
    vercel_url = input("Vercel URL: ").strip()
    
    if not vercel_url:
        print("❌ No URL provided. Exiting.")
        exit(1)
    
    if not vercel_url.startswith('http'):
        vercel_url = f"https://{vercel_url}"
    
    success = test_vercel_deployment(vercel_url)
    
    if success:
        print("\n✅ All tests passed! Your deployment should be working.")
    else:
        print("\n❌ Tests failed. Please check the errors above and:")
        print("1. Verify environment variables in Vercel dashboard")
        print("2. Check Vercel function logs")
        print("3. Ensure the deployment completed successfully") 