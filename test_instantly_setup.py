#!/usr/bin/env python3
"""
Test script to find your Instantly Email Account ID
Run this to discover your connected email account IDs
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_instantly_connection():
    """Test Instantly API connection and list email accounts"""
    
    # Use the actual credentials from env_template
    api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
    workspace_id = "46dfb1ae-a586-4886-9136-47070c6b1b22"
    
    print("🔍 Testing Instantly API connection...")
    print(f"Using Workspace ID: {workspace_id}")
    
    # Try different API endpoints to find email accounts
    endpoints_to_try = [
        "/api/v2/accounts/email",
        "/api/v2/workspace/email-accounts", 
        "/api/v2/email_accounts",
        "/api/v2/accounts",
        "/api/v1/email-accounts",
        "/api/v1/accounts"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for endpoint in endpoints_to_try:
        try:
            url = f"https://api.instantly.ai{endpoint}"
            print(f"\n🔍 Trying endpoint: {endpoint}")
            
            response = requests.get(url, headers=headers)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Success! Found working endpoint")
                
                try:
                    data = response.json()
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    # Look for email accounts in various possible response structures
                    email_accounts = []
                    
                    if isinstance(data, dict):
                        # Try different possible keys
                        for key in ['email_accounts', 'accounts', 'data', 'emails', 'connected_accounts']:
                            if key in data:
                                email_accounts = data[key]
                                break
                    elif isinstance(data, list):
                        email_accounts = data
                    
                    if email_accounts:
                        print(f"\n📧 Found {len(email_accounts)} email account(s):")
                        print("=" * 60)
                        
                        for i, account in enumerate(email_accounts, 1):
                            email = account.get("email", account.get("address", "Unknown"))
                            account_id = account.get("id", account.get("account_id", account.get("uuid", "Unknown")))
                            status = account.get("status", account.get("state", "Unknown"))
                            
                            print(f"{i}. Email: {email}")
                            print(f"   Account ID: {account_id}")
                            print(f"   Status: {status}")
                            print("-" * 40)
                        
                        print("\n🎯 Use one of the Account IDs above for INSTANTLY_EMAIL_ACCOUNT_ID")
                        
                        if len(email_accounts) == 1:
                            suggested_id = email_accounts[0].get("id", email_accounts[0].get("account_id", email_accounts[0].get("uuid")))
                            print(f"\n💡 Suggestion: Update your .env file with:")
                            print(f"INSTANTLY_EMAIL_ACCOUNT_ID={suggested_id}")
                        
                        return  # Success, exit the function
                    else:
                        print("No email accounts found in response")
                        print(f"Full response: {data}")
                        
                except Exception as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Raw response: {response.text}")
                    
            elif response.status_code == 401:
                print("❌ Authentication failed - API key may be invalid")
            elif response.status_code == 403:
                print("❌ Access denied - API key may lack permissions")
            elif response.status_code == 404:
                print("❌ Endpoint not found")
            else:
                print(f"❌ Request failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error with endpoint {endpoint}: {e}")
    
    print("\n⚠️  Could not find email accounts using any known endpoint")
    print("\n🔧 Alternative methods to find your Email Account ID:")
    print("1. Check your Instantly dashboard under 'Email Accounts' or 'Connected Accounts'")
    print("2. Look in the URL when viewing an email account (e.g., /accounts/abc123...)")
    print("3. Contact Instantly support for assistance")
    print("4. Check if you need to connect an email account first")

def test_basic_api_access():
    """Test basic API access"""
    api_key = "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg=="
    
    # Try a simple workspace info endpoint
    url = "https://api.instantly.ai/api/v2/workspace"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\n🏢 Workspace API Test - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Workspace info: {data}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Workspace API error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Instantly API Setup Test")
    print("=" * 60)
    test_instantly_connection()
    test_basic_api_access()
    print("\n" + "=" * 60) 