import requests
import json

# Test different API endpoints to determine what scopes our API key has
api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
base_url = "https://api.instantly.ai/api/v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🔍 TESTING API KEY SCOPES")
print("="*50)
print(f"API Key: {api_key[:20]}...")

# Test different endpoints to determine scopes
tests = [
    {
        "name": "Campaigns - List",
        "method": "GET",
        "endpoint": "/campaigns",
        "required_scope": "campaigns:read or campaigns:all",
        "description": "List campaigns"
    },
    {
        "name": "Campaigns - Create", 
        "method": "POST",
        "endpoint": "/campaigns",
        "required_scope": "campaigns:create or campaigns:all",
        "description": "Create campaigns",
        "data": {
            "name": "SCOPE_TEST_CAMPAIGN",
            "email_list": [],
            "status": "draft"
        }
    },
    {
        "name": "Leads - List",
        "method": "POST", 
        "endpoint": "/leads/list",
        "required_scope": "leads:read or leads:all",
        "description": "List leads",
        "data": {"limit": 1}
    },
    {
        "name": "Leads - Create",
        "method": "POST",
        "endpoint": "/leads", 
        "required_scope": "leads:create or leads:all",
        "description": "Create leads",
        "data": {
            "email": "scope.test@example.com",
            "first_name": "Scope",
            "last_name": "Test"
        }
    }
]

# Run scope tests
results = []
for test in tests:
    print(f"\n🧪 Testing: {test['name']}")
    print(f"   Endpoint: {test['method']} {test['endpoint']}")
    print(f"   Required Scope: {test['required_scope']}")
    
    try:
        if test['method'] == 'GET':
            response = requests.get(f"{base_url}{test['endpoint']}", headers=headers, timeout=10)
        else:
            data = test.get('data', {})
            response = requests.post(f"{base_url}{test['endpoint']}", headers=headers, json=data, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS - Scope available")
            results.append({"test": test['name'], "scope": test['required_scope'], "status": "✅ Available"})
        elif response.status_code == 401:
            print(f"   ❌ UNAUTHORIZED - API key invalid")
            results.append({"test": test['name'], "scope": test['required_scope'], "status": "❌ Unauthorized"})
        elif response.status_code == 403:
            print(f"   ⛔ FORBIDDEN - Scope missing")
            results.append({"test": test['name'], "scope": test['required_scope'], "status": "⛔ Scope Missing"})
        else:
            print(f"   ⚠️ OTHER ERROR: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            results.append({"test": test['name'], "scope": test['required_scope'], "status": f"⚠️ Error {response.status_code}"})
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        results.append({"test": test['name'], "scope": test['required_scope'], "status": f"❌ Error: {str(e)[:30]}..."})

# Test campaign activation specifically
print(f"\n🎯 TESTING CAMPAIGN ACTIVATION SCOPE")
test_campaign_id = "dd776a0d-b0d9-45a0-8bdc-571ba8cd1301"  # Our test campaign

try:
    # Test activation endpoint access
    response = requests.post(
        f"{base_url}/campaigns/{test_campaign_id}/activate",
        headers=headers,
        timeout=10
    )
    
    print(f"   Activation Endpoint Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ ACTIVATION SCOPE AVAILABLE!")
        results.append({"test": "Campaign Activation", "scope": "campaigns:update or campaigns:all", "status": "✅ Available"})
    elif response.status_code == 403:
        print(f"   ⛔ ACTIVATION SCOPE MISSING!")
        print(f"   This is why activation fails!")
        results.append({"test": "Campaign Activation", "scope": "campaigns:update or campaigns:all", "status": "⛔ MISSING (Root Cause)"})
    elif response.status_code == 400:
        print(f"   ⚠️ BAD REQUEST - Scope available but campaign state issue")
        print(f"   Campaign might need configuration before activation")
        results.append({"test": "Campaign Activation", "scope": "campaigns:update or campaigns:all", "status": "⚠️ Available but campaign state issue"})
    else:
        print(f"   ❌ ERROR: {response.status_code} - {response.text[:100]}")
        results.append({"test": "Campaign Activation", "scope": "campaigns:update or campaigns:all", "status": f"❌ Error {response.status_code}"})

except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Summary
print(f"\n" + "="*50)
print(f"📊 API KEY SCOPE ANALYSIS")
print(f"="*50)

for result in results:
    print(f"{result['status']} {result['test']}")
    print(f"   Required: {result['scope']}")

print(f"\n🎯 RECOMMENDATIONS:")
print(f"1. If activation scope is missing → Update API key permissions")
print(f"2. If activation scope available but 400 error → Configure campaign settings")
print(f"3. Check Instantly dashboard for API key management")
print("="*50)

if __name__ == "__main__":
    test_api_scopes() 