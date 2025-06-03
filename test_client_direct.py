#!/usr/bin/env python3
"""
Direct test of the InstantlyClient to verify activation works
"""
from instantly_client import InstantlyClient
import time

def test_client_direct():
    print("🧪 TESTING INSTANTLY CLIENT DIRECTLY")
    print("="*50)
    
    # Initialize client
    client = InstantlyClient()
    
    if not client.is_configured():
        print("❌ Client not configured")
        return
    
    try:
        # Step 1: Create campaign
        print("📋 Step 1: Creating campaign...")
        campaign_name = f"CLIENT_TEST_{int(time.time())}"
        campaign_id = client.create_campaign(
            campaign_name,
            "Direct Client Test Subject",
            "This is a direct test of the client activation functionality."
        )
        print(f"✅ Campaign created: {campaign_id}")
        
        # Step 2: Add a test lead
        print("📋 Step 2: Adding test lead...")
        test_leads = [{
            "to": "direct.test@example.com",
            "name": "Direct Test User",
            "company": "Test Company"
        }]
        
        leads_result = client.add_leads_to_campaign(campaign_id, test_leads)
        print(f"✅ Leads added: {leads_result.get('successful_leads', 0)} successful")
        
        # Step 3: Try activation
        print("🚀 Step 3: Attempting activation...")
        if leads_result.get('successful_leads', 0) > 0:
            activation_result = client.activate_campaign(campaign_id)
            print(f"✅ ACTIVATION SUCCESSFUL!")
            print(f"Result: {activation_result}")
            
            # Step 4: Check final status
            print("🔍 Step 4: Checking final status...")
            status = client.get_campaign_status(campaign_id)
            campaign_status = status.get('status')
            print(f"Final campaign status: {campaign_status}")
            
            if campaign_status == 1:
                print("🎉 SUCCESS: Campaign is ACTIVE and ready to send!")
            else:
                print(f"⚠️ Campaign status: {campaign_status}")
                
        else:
            print("❌ No leads added - cannot activate")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_client_direct() 