import requests
import os
import time
from typing import List, Dict, Optional
import uuid

class InstantlyClient:
    """Client for Instantly API v2 integration"""
    
    def __init__(self):
        # Try to get from environment first, then fall back to corrected hardcoded value
        self.api_key = os.getenv("INSTANTLY_API_KEY", "NDZkZmIxYWUtYTU4Ni00ODg2LTkxMzYtNDcwNzBjNmIxYjIyOlRUV0VETWRiRFhIdg==")
        self.workspace_id = os.getenv("INSTANTLY_WORKSPACE_ID", "9a28e3f9-30ce-4c1f-b85a-53e5d893a4a3")
        # Fix: Use Rob's email account from workspace
        self.email_account_id = os.getenv("INSTANTLY_EMAIL_ACCOUNT_ID", "rob@biscred.ai")  # Updated to Rob's account
        self.base_url = "https://api.instantly.ai/api/v2"
        
        print(f"🔑 INSTANTLY CLIENT INITIALIZED:")
        print(f"   API Key: {self.api_key[:20] if self.api_key else 'None'}...")
        print(f"   Workspace ID: {self.workspace_id}")
        print(f"   Email Account: {self.email_account_id}")
        
        if not all([self.api_key, self.workspace_id, self.email_account_id]):
            print("Warning: Instantly API credentials not fully configured")
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make authenticated request to Instantly API"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Enhanced logging
        print(f"🔍 INSTANTLY API REQUEST:")
        print(f"   Method: {method}")
        print(f"   URL: {url}")
        print(f"   Headers: {headers}")
        if data:
            print(f"   Data: {data}")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            
            print(f"✅ INSTANTLY API RESPONSE:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ INSTANTLY API ERROR: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Error Response: {e.response.text}")
            raise Exception(f"Instantly API request failed: {str(e)}")
    
    def create_campaign(self, campaign_name: str, email_subject: str, email_body: str) -> str:
        """Create a new campaign with proper activation-ready structure"""
        print(f"🏗️ CREATING INSTANTLY CAMPAIGN:")
        print(f"   Name: {campaign_name}")
        print(f"   Subject: {email_subject}")
        print(f"   Body: {email_body[:50]}...")
        
        # Create campaign with all required fields for activation
        campaign_data = {
            "name": campaign_name,
            "campaign_schedule": {
                "schedules": [
                    {
                        "name": "Business Hours",
                        "timing": {
                            "from": "09:00",
                            "to": "17:00"
                        },
                        "days": {
                            "0": False,  # Sunday
                            "1": True,   # Monday
                            "2": True,   # Tuesday
                            "3": True,   # Wednesday
                            "4": True,   # Thursday
                            "5": True,   # Friday
                            "6": False   # Saturday
                        },
                        "timezone": "America/Chicago"  # Fixed: Use valid timezone
                    }
                ]
            },
            "email_list": [self.email_account_id],  # Required for activation
            "sequences": [
                {
                    "steps": [
                        {
                            "subject": email_subject,
                            "body": email_body,
                            "day": 1,        # Required: Day number
                            "type": "email", # Required: Step type
                            "delay": 0,      # Required: Delay in days
                            "variants": [    # Required: Email variants
                                {
                                    "subject": email_subject,
                                    "body": email_body
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        try:
            response = self._make_request("POST", "/campaigns", campaign_data)
            campaign_id = response.get("id") or response.get("campaign_id")
            print(f"✅ CAMPAIGN CREATED: {campaign_id}")
            return campaign_id
        except Exception as e:
            print(f"❌ CAMPAIGN CREATION FAILED: {e}")
            raise
    
    def add_leads_to_campaign(self, campaign_id: str, leads: List[Dict]) -> Dict:
        """Add leads to an existing campaign using individual lead creation with duplicate handling"""
        print(f"🎯 ADDING LEADS TO CAMPAIGN:")
        print(f"   Campaign ID: {campaign_id}")
        print(f"   Number of leads: {len(leads)}")
        
        successful_leads = []
        failed_leads = []
        
        for i, lead in enumerate(leads):
            try:
                print(f"   📋 Processing lead {i+1}/{len(leads)}: {lead.get('to') or lead.get('email') or 'Unknown'}")
                
                # Parse name into first/last name
                name = lead.get("name", "").strip()
                name_parts = name.split() if name else ["", ""]
                first_name = name_parts[0] if len(name_parts) > 0 else ""
                last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                
                # Create lead data with duplicate handling flags
                lead_data = {
                    "email": lead.get("to", lead.get("email", "")),
                    "first_name": first_name,
                    "last_name": last_name,
                    "campaign": campaign_id,  # Required field per API docs
                    "skip_if_in_workspace": True,  # Skip if email exists in workspace
                    "skip_if_in_campaign": False,  # Allow moving between campaigns
                    "skip_if_in_list": False  # Allow adding to campaigns even if in lists
                }
                
                # Add optional fields if they exist
                if lead.get("company"):
                    lead_data["company_name"] = lead.get("company")
                if lead.get("phone"):
                    lead_data["phone"] = lead.get("phone")
                if lead.get("website"):
                    lead_data["website"] = lead.get("website")
                
                # Ensure email is not empty
                if not lead_data["email"]:
                    raise ValueError(f"Email is required for lead: {lead}")
                
                print(f"   📤 Sending lead data: {lead_data}")
                
                # Use the correct endpoint for creating leads: POST /api/v2/leads
                response = self._make_request("POST", "/leads", lead_data)
                
                print(f"   ✅ Lead added successfully: {response.get('id', 'Unknown ID')}")
                successful_leads.append({
                    "email": lead_data["email"],
                    "lead_id": response.get("id"),
                    "status": "success",
                    "response": response
                })
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Failed to add lead {lead.get('to', 'Unknown')}: {error_msg}")
                
                # Check if it's a duplicate error - treat as success
                if "duplicate" in error_msg.lower() or "already exists" in error_msg.lower():
                    print(f"   ✅ Lead already exists - treating as success")
                    successful_leads.append({
                        "email": lead.get("to", lead.get("email", "Unknown")),
                        "lead_id": "existing",
                        "status": "success_existing",
                        "note": "Lead already exists in system"
                    })
                else:
                    failed_leads.append({
                        "email": lead.get("to", lead.get("email", "Unknown")),
                        "error": error_msg,
                        "status": "failed",
                        "lead_data": lead_data if 'lead_data' in locals() else lead
                    })
                continue
        
        result = {
            "campaign_id": campaign_id,
            "total_leads": len(leads),
            "successful_leads": len(successful_leads),
            "failed_leads": len(failed_leads),
            "successful_details": successful_leads,
            "failed_details": failed_leads
        }
        
        print(f"   📊 LEAD ADDITION SUMMARY:")
        print(f"   Total leads processed: {len(leads)}")
        print(f"   Successfully added: {len(successful_leads)}")
        print(f"   Failed: {len(failed_leads)}")
        
        if failed_leads:
            print(f"   ⚠️ FAILED LEAD DETAILS:")
            for failed in failed_leads:
                print(f"     - {failed['email']}: {failed['error']}")
        
        return result
    
    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Get campaign status and metrics"""
        try:
            response = self._make_request("GET", f"/campaigns/{campaign_id}")  # Use /campaigns
            return response
        except Exception as e:
            print(f"Failed to get campaign status: {e}")
            raise
    
    def get_lead_emails(self, lead_id: str) -> List[Dict]:
        """Get email history for a specific lead"""
        try:
            response = self._make_request("GET", f"/leads/{lead_id}/emails")
            return response.get("emails", [])
        except Exception as e:
            print(f"Failed to get lead emails: {e}")
            return []
    
    def send_reply(self, lead_id: str, reply_body: str, subject: str = None) -> Dict:
        """Send a reply to a lead"""
        reply_data = {
            "lead_id": lead_id,
            "body": reply_body
        }
        if subject:
            reply_data["subject"] = subject
        
        try:
            response = self._make_request("POST", "/emails/reply", reply_data)
            return response
        except Exception as e:
            print(f"Failed to send reply: {e}")
            raise
    
    def pause_campaign(self, campaign_id: str) -> Dict:
        """Pause a campaign"""
        try:
            response = self._make_request("PUT", f"/campaigns/{campaign_id}/pause")  # Use /campaigns
            return response
        except Exception as e:
            print(f"Failed to pause campaign: {e}")
            raise
    
    def resume_campaign(self, campaign_id: str) -> Dict:
        """Resume a paused campaign"""
        try:
            response = self._make_request("PUT", f"/campaigns/{campaign_id}/resume")  # Use /campaigns
            return response
        except Exception as e:
            print(f"Failed to resume campaign: {e}")
            raise
    
    def activate_campaign(self, campaign_id: str) -> Dict:
        """Activate a draft campaign"""
        try:
            # For activation, we don't need Content-Type: application/json since it expects empty body
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            print(f"🔍 INSTANTLY API REQUEST:")
            print(f"   Method: POST")
            print(f"   URL: {self.base_url}/campaigns/{campaign_id}/activate")
            print(f"   Headers: {headers}")
            print(f"   Data: None (empty body)")
            
            response = requests.post(
                f"{self.base_url}/campaigns/{campaign_id}/activate",
                headers=headers
            )
            
            print(f"✅ INSTANTLY API RESPONSE:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            print(f"✅ Campaign activated: {campaign_id}")
            return result
        except Exception as e:
            print(f"❌ Failed to activate campaign: {e}")
            raise
    
    def is_configured(self) -> bool:
        """Check if Instantly client is properly configured"""
        return all([self.api_key, self.workspace_id, self.email_account_id])
    
    def get_campaign_leads(self, campaign_id: str) -> Dict:
        """Get all leads for a specific campaign"""
        try:
            print(f"🔍 GETTING LEADS FOR CAMPAIGN: {campaign_id}")
            # Try different possible endpoints for getting campaign leads
            response = self._make_request("GET", f"/campaigns/{campaign_id}/leads")
            return response
        except Exception as e:
            print(f"❌ Failed to get campaign leads via /campaigns/{campaign_id}/leads: {e}")
            try:
                # Alternative: Get all leads and filter by campaign
                response = self._make_request("GET", "/leads", {"campaign": campaign_id})
                return response
            except Exception as e2:
                print(f"❌ Failed to get leads via /leads with campaign filter: {e2}")
                raise Exception(f"Could not get leads for campaign: {str(e)}") 