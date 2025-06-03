#!/usr/bin/env python3
"""
Test script to verify Vercel deployment status
"""
import requests
import json

VERCEL_URL = "https://sender-sigma.vercel.app"

def test_vercel_deployment():
    print("🚀 TESTING VERCEL DEPLOYMENT STATUS")
    print("="*50)
    
    try:
        # Test 1: Health check to see if app is running
        print("🏥 Step 1: Health check...")
        health_response = requests.get(f"{VERCEL_URL}/health", timeout=10)
        print(f"   Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Instantly Configured: {health_data.get('instantly_configured')}")
            print(f"   OpenAI Configured: {health_data.get('openai_configured')}")
        
        # Test 2: Test a known campaign ID with manual activation
        print("🧪 Step 2: Testing manual activation endpoint...")
        test_campaign_id = "7a72cb5d-cbb3-480e-8ac4-5064b6f0c04e"  # From recent test
        
        activation_response = requests.post(
            f"{VERCEL_URL}/activate-campaign/", 
            json=test_campaign_id, 
            timeout=30
        )
        
        print(f"   Activation Status: {activation_response.status_code}")
        print(f"   Response Preview: {activation_response.text[:200]}...")
        
        if activation_response.status_code == 200:
            print("   ✅ SUCCESS: Activation endpoint is working!")
            activation_data = activation_response.json()
            campaign_status = activation_data.get('result', {}).get('status')
            print(f"   Campaign Status: {campaign_status} (1=Active)")
            
            if campaign_status == 1:
                print("   🎉 CAMPAIGN ACTIVATED: The fixes are deployed!")
                return True
            else:
                print("   ⚠️ Campaign not active, but endpoint is working")
                return False
        else:
            print("   ❌ FAILED: Activation endpoint returning error")
            print(f"   Error: {activation_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def check_git_status():
    print("📋 CHECKING GIT STATUS:")
    import subprocess
    try:
        # Check git status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        if result.stdout.strip():
            print("   ⚠️ Uncommitted changes found:")
            print(f"   {result.stdout}")
        else:
            print("   ✅ Working directory clean")
        
        # Check latest commit
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True, cwd='.')
        print(f"   Latest commit: {result.stdout.strip()}")
        
    except Exception as e:
        print(f"   ❌ Git check failed: {e}")

if __name__ == "__main__":
    check_git_status()
    print()
    success = test_vercel_deployment()
    
    print("\n" + "="*50)
    if success:
        print("🎉 VERCEL DEPLOYMENT: SUCCESS")
        print("✅ Campaign activation is working in production!")
    else:
        print("❌ VERCEL DEPLOYMENT: NEEDS ATTENTION")
        print("📝 Deployment may not be complete or there's a configuration issue")
    print("="*50) 