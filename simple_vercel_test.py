import requests

# Replace this with your actual Vercel URL
VERCEL_URL = input("Enter your Vercel URL: ").strip()

if not VERCEL_URL.startswith('http'):
    VERCEL_URL = f"https://{VERCEL_URL}"

print(f"🔍 TESTING VERCEL DEPLOYMENT: {VERCEL_URL}")
print("="*60)

# Test 1: Health check
print("📋 TEST 1: Health Check")
try:
    response = requests.get(f"{VERCEL_URL}/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health Response: {data}")
        print(f"Instantly configured: {data.get('instantly_configured')}")
        
        if not data.get('instantly_configured'):
            print("❌ FOUND THE ISSUE: Instantly not configured in Vercel!")
            print("Fix: Update environment variables in Vercel dashboard")
            exit()
    else:
        print(f"❌ Health check failed: {response.text}")
        exit()
except Exception as e:
    print(f"❌ Health check error: {e}")
    exit()

# Test 2: Debug endpoint (if deployed)
print("\n📋 TEST 2: Debug Lead Addition Endpoint")
try:
    response = requests.post(f"{VERCEL_URL}/debug-lead-addition/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Debug Response:")
        print(f"   Status: {data.get('status')}")
        print(f"   Message: {data.get('message')}")
        
        if data.get('status') == 'success':
            lead_result = data.get('lead_addition_result', {})
            print(f"   Campaign ID: {data.get('campaign_id')}")
            print(f"   Lead Addition:")
            print(f"     Total: {lead_result.get('total_leads')}")
            print(f"     Successful: {lead_result.get('successful_leads')}")
            print(f"     Failed: {lead_result.get('failed_leads')}")
            
            if lead_result.get('successful_leads', 0) > 0:
                print("✅ LEAD ADDITION WORKS IN VERCEL!")
                print("   The issue might be elsewhere in your flow.")
            else:
                print("❌ LEAD ADDITION FAILING IN VERCEL")
                if lead_result.get('failed_details'):
                    for failure in lead_result['failed_details']:
                        print(f"     Error: {failure}")
        else:
            print(f"❌ Debug test failed: {data.get('message')}")
            print(f"Environment check: {data.get('environment_check')}")
    else:
        print(f"❌ Debug endpoint failed: {response.text}")
        
except Exception as e:
    print(f"❌ Debug test error: {e}")

# Test 3: Simple email sending
print("\n📋 TEST 3: Simple Email Send Test")
try:
    test_request = {
        "approved_emails": [{
            "to": "vercel.simple.test@example.com",
            "name": "Vercel Simple Test",
            "company": "Test Corp",
            "subject": "Vercel Test",
            "body": "Simple test email"
        }],
        "campaign_name": "Vercel_Simple_Test",
        "send_mode": "instantly"
    }
    
    response = requests.post(
        f"{VERCEL_URL}/send-emails/",
        json=test_request,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Email Send Response:")
        print(f"   Mode: {data.get('mode')}")
        print(f"   Successful: {data.get('successful_sends')}")
        print(f"   Failed: {data.get('failed_sends')}")
        
        if data.get('mode') == 'simulation':
            print("❌ RUNNING IN SIMULATION MODE - Instantly integration failed!")
        
        # Check individual results
        for result in data.get('results', []):
            print(f"   Result: {result.get('status')} - {result.get('message')}")
            if 'lead_addition' in result:
                lead_info = result['lead_addition']
                print(f"   Lead Addition: {lead_info.get('successful_leads')}/{lead_info.get('total_leads')} successful")
                
                if lead_info.get('failed_details'):
                    print("   ❌ Lead Addition Failures:")
                    for failure in lead_info['failed_details']:
                        print(f"     - {failure.get('email')}: {failure.get('error')}")
    else:
        print(f"❌ Email send failed: {response.text}")
        
except Exception as e:
    print(f"❌ Email send error: {e}")

print("\n" + "="*60)
print("🎯 NEXT STEPS:")
print("If you see 'simulation mode' or 'Instantly not configured':")
print("1. Check Vercel environment variables")
print("2. Ensure the API key includes the == at the end")
print("3. Redeploy after updating variables")
print("="*60) 