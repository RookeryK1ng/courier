import requests

campaign_id = "b437adf6-d495-480b-a96a-47e4ffdae324"

try:
    # Test campaign leads
    response = requests.get(f"http://localhost:8000/test-campaign-leads/{campaign_id}")
    print(f"Lead Test Status: {response.status_code}")
    print(f"Lead Test Response: {response.text}")
    
    # Test campaign status
    response2 = requests.get(f"http://localhost:8000/test-campaign/{campaign_id}")
    print(f"\nCampaign Status: {response2.status_code}")
    print(f"Campaign Response: {response2.text}")
    
except Exception as e:
    print(f"Error: {e}") 