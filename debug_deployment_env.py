import os
from instantly_client import InstantlyClient
import requests

print("🔍 DEBUGGING DEPLOYMENT ENVIRONMENT")
print("="*60)

# Test environment variables
print("📋 ENVIRONMENT VARIABLES:")
print(f"   INSTANTLY_API_KEY: {os.getenv('INSTANTLY_API_KEY', 'NOT SET')}")
print(f"   INSTANTLY_WORKSPACE_ID: {os.getenv('INSTANTLY_WORKSPACE_ID', 'NOT SET')}")
print(f"   INSTANTLY_EMAIL_ACCOUNT_ID: {os.getenv('INSTANTLY_EMAIL_ACCOUNT_ID', 'NOT SET')}")

# Initialize client as it would be in deployment
client = InstantlyClient()
print(f"\n📋 CLIENT CONFIGURATION:")
print(f"   API Key: {client.api_key[:20]}...{client.api_key[-10:] if client.api_key else 'None'}")
print(f"   Workspace ID: {client.workspace_id}")
print(f"   Email Account ID: {client.email_account_id}")
print(f"   Is Configured: {client.is_configured()}")

# Test simple API call first
print(f"\n📋 TESTING BASIC API ACCESS:")
try:
    headers = {
        "Authorization": f"Bearer {client.api_key}",
        "Content-Type": "application/json"
    }
    
    # Test a simple GET request first
    print("Testing GET request (reading campaigns)...")
    response = requests.get(
        f"{client.base_url}/campaigns",
        headers={"Authorization": f"Bearer {client.api_key}"},
        params={"limit": 1}
    )
    
    print(f"GET response status: {response.status_code}")
    if response.status_code == 200:
        print("✅ GET requests working (can read data)")
    else:
        print(f"❌ GET failed: {response.text}")
    
    # Test a simple POST request 
    print("\nTesting POST request (adding a single lead)...")
    test_lead_data = {
        "email": "deployment.test@example.com",
        "first_name": "Deploy",
        "last_name": "Test",
        "campaign": "1cd17813-4d00-4a1e-809e-5e99f7350ba8",  # Use existing campaign
        "skip_if_in_workspace": True,
        "skip_if_in_campaign": False,
        "skip_if_in_list": False
    }
    
    post_response = requests.post(
        f"{client.base_url}/leads",
        headers=headers,
        json=test_lead_data
    )
    
    print(f"POST response status: {post_response.status_code}")
    print(f"POST response: {post_response.text}")
    
    if post_response.status_code == 200:
        print("✅ POST requests working (can add leads)")
    elif post_response.status_code == 401:
        print("❌ AUTHENTICATION FAILED - API key is invalid or missing ==")
    else:
        print(f"❌ POST failed with status {post_response.status_code}")

except Exception as e:
    print(f"❌ ERROR during API testing: {e}")

# Test the full client method
print(f"\n📋 TESTING CLIENT METHOD:")
try:
    test_contacts = [{
        "to": "client.method.test@example.com",
        "name": "Client Method Test",
        "company": "Test Corp"
    }]
    
    result = client.add_leads_to_campaign("1cd17813-4d00-4a1e-809e-5e99f7350ba8", test_contacts)
    
    print(f"✅ Client method result:")
    print(f"   Total: {result.get('total_leads', 0)}")
    print(f"   Successful: {result.get('successful_leads', 0)}")
    print(f"   Failed: {result.get('failed_leads', 0)}")
    
    if result.get('failed_details'):
        print(f"❌ Failures:")
        for failure in result['failed_details']:
            print(f"   - {failure.get('email')}: {failure.get('error')}")

except Exception as e:
    print(f"❌ Client method failed: {e}")

print("\n" + "="*60)
print("🏁 DEPLOYMENT ENVIRONMENT DEBUG COMPLETE")
print("="*60) 