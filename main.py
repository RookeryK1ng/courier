from fastapi import FastAPI, UploadFile, File, Form, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import csv
import io
import requests
import os
import pandas as pd
import uuid
from datetime import datetime
from dotenv import load_dotenv
from instantly_client import InstantlyClient

# Load environment variables
load_dotenv()

app = FastAPI(title="Courier Email API", version="1.0.0")

# CORS middleware - restrict to your frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://biscred-courier.vercel.app",
        "http://localhost:3000",  # for development
        "https://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Initialize Instantly client
instantly_client = InstantlyClient()

def normalize_contact_data(df):
    """
    Normalize contact data to handle different column naming conventions.
    Maps various possible column names to standard field names.
    """
    # Create a copy to avoid modifying the original dataframe
    df_normalized = df.copy()
    
    # Column mappings: {standard_name: [possible_variations]}
    column_mappings = {
        'name': ['name', 'full_name', 'full name', 'contact_name', 'contact name'],
        'first_name': ['first_name', 'first name', 'firstname', 'fname'],
        'last_name': ['last_name', 'last name', 'lastname', 'lname', 'surname'],
        'email': ['email', 'email_address', 'email address', 'e-mail', 'e_mail'],
        'company': ['company', 'company_name', 'company name', 'organization', 'org'],
        'position': ['position', 'title', 'job_title', 'job title', 'role', 'job_role', 'job role'],
        'industry': ['industry', 'company_industries', 'company industries', 'industries', 'sector'],
        'location': ['location', 'city', 'address', 'region'],
        'phone': ['phone', 'phone_number', 'phone number', 'telephone', 'tel'],
        'linkedin': ['linkedin', 'linkedin_url', 'linkedin url', 'linkedin_profile', 'linkedin profile']
    }
    
    # Apply mappings
    for standard_name, variations in column_mappings.items():
        for variation in variations:
            if variation.title() in df_normalized.columns or variation.lower() in df_normalized.columns or variation.upper() in df_normalized.columns:
                # Find the actual column name (case-insensitive)
                actual_col = None
                for col in df_normalized.columns:
                    if col.lower() == variation.lower():
                        actual_col = col
                        break
                
                if actual_col and standard_name not in [c.lower() for c in df_normalized.columns]:
                    df_normalized = df_normalized.rename(columns={actual_col: standard_name})
                    break
    
    # If we have separate first_name and last_name but no name, combine them
    if 'first_name' in df_normalized.columns and 'last_name' in df_normalized.columns and 'name' not in df_normalized.columns:
        df_normalized['name'] = df_normalized['first_name'].astype(str) + ' ' + df_normalized['last_name'].astype(str)
        df_normalized['name'] = df_normalized['name'].str.strip()
    
    return df_normalized

@app.get("/")
async def root():
    return {"message": "Courier Email API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "openai_configured": bool(openai_api_key),
        "instantly_configured": instantly_client.is_configured()
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working!",
        "openai_configured": bool(openai_api_key),
        "openai_key_preview": f"{openai_api_key[:10]}..." if openai_api_key else "NOT SET"
    }

@app.post("/generate-emails/")
async def generate_emails(
    file: UploadFile = File(...),
    campaign_content: str = Form(...),
    sender_name: str = Form(...),
    sender_title: str = Form(""),
    sender_company: str = Form("")
):
    try:
        # Read file contents
        contents = await file.read()
        contacts = []
        
        try:
            # Determine file type and process accordingly
            file_extension = file.filename.lower().split('.')[-1] if file.filename else ''
            
            if file_extension == 'csv':
                # Process CSV file
                df = pd.read_csv(io.StringIO(contents.decode()))
            elif file_extension in ['xlsx', 'xls']:
                # Process Excel file
                df = pd.read_excel(io.BytesIO(contents))
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format: {file_extension}. Please upload a CSV or Excel file."
                )
            
            # Normalize contact data
            df = normalize_contact_data(df)
            
            # Convert DataFrame to list of dictionaries
            # Handle NaN values by replacing them with empty strings
            df = df.fillna('')
            contacts = df.to_dict('records')
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse {file_extension.upper()} file: {str(e)}. Please ensure your file has headers and proper formatting."
            )
        
        if not contacts:
            raise HTTPException(
                status_code=400,
                detail="No valid contacts found in file. Please check your file format and ensure it contains contact data."
            )

        print(f"Processing {len(contacts)} contacts...")
        print(f"Available columns: {list(df.columns)}")
        emails = []
        
        # Create custom signature
        signature_lines = []
        signature_lines.append(sender_name)
        if sender_title:
            signature_lines.append(sender_title)
        if sender_company:
            signature_lines.append(sender_company)
        
        custom_signature = "\n".join(signature_lines)
        
        # Check if OpenAI is available
        if not openai_client:
            print("OpenAI not configured, using dummy mode...")
            # Generate dummy emails for testing
            for i, contact in enumerate(contacts):
                dummy_email = f"""Hi {contact.get('name', 'there')},

I hope this email finds you well! I'm reaching out from our team regarding an exciting opportunity.

{campaign_content}

Given your role as {contact.get('position', 'a professional')} at {contact.get('company', 'your company')}, I thought this might be of interest to you.

Would you be available for a quick 15-minute call to discuss further?

{custom_signature}

P.S. This is a demo email generated without OpenAI integration."""
                
                emails.append({
                    "to": contact.get('email', ''),
                    "name": contact.get('name', ''),
                    "company": contact.get('company', ''),
                    "subject": f"Partnership Opportunity - {contact.get('company', 'Your Company')}",
                    "body": dummy_email
                })
        else:
            # Use OpenAI for real personalized emails
            for i, contact in enumerate(contacts):
                print(f"Generating email {i+1}/{len(contacts)} for {contact.get('name', 'Unknown')}")
                
                try:
                    prompt = (
                        f"Write a professional, personalized marketing email to {contact.get('name', 'valued customer')} "
                        f"at {contact.get('company', 'their company')}.\n"
                        f"Campaign content: {campaign_content}\n"
                        f"Recipient details: {contact.get('position', '')} in {contact.get('industry', '')} industry\n"
                        f"Sender: {sender_name}" + (f", {sender_title}" if sender_title else "") + (f" at {sender_company}" if sender_company else "") + "\n"
                        f"Make it engaging, professional, and include a clear call-to-action. "
                        f"Keep it concise (under 200 words). "
                        f"End the email with just the sender's name and details on separate lines, no 'Best regards' needed."
                    )
                    
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=300,
                        temperature=0.7
                    )
                    
                    email_text = response.choices[0].message.content
                    
                    emails.append({
                        "to": contact.get('email', ''),
                        "name": contact.get('name', ''),
                        "company": contact.get('company', ''),
                        "subject": f"Partnership Opportunity with {contact.get('company', 'Your Company')}",
                        "body": email_text
                    })
                    
                except Exception as e:
                    print(f"Error generating email for {contact.get('name', 'contact')}: {str(e)}")
                    # Continue with other contacts, but log the error
                    emails.append({
                        "to": contact.get('email', ''),
                        "name": contact.get('name', ''),
                        "company": contact.get('company', ''),
                        "subject": f"Partnership Opportunity with {contact.get('company', 'Your Company')}",
                        "body": f"Error generating personalized content for {contact.get('name', 'this contact')}. Please contact support."
                    })

        print(f"Successfully generated {len(emails)} emails (OpenAI: {'enabled' if openai_client else 'disabled - using dummy mode'})")
        return {"emails": emails, "count": len(emails), "mode": "openai" if openai_client else "dummy"}
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Unexpected error in generate_emails: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/send-emails/")
async def send_emails(
    approved_emails: list = Body(...),
    campaign_name: str = Body(None),
    send_mode: str = Body("instantly")  # "instantly" or "fallback"
):
    """
    Send emails via Instantly API or fallback to simulation mode
    """
    try:
        print(f"📧 SEND EMAILS REQUEST:")
        print(f"   Email count: {len(approved_emails)}")
        print(f"   Campaign name: {campaign_name}")
        print(f"   Send mode: {send_mode}")
        print(f"   Instantly configured: {instantly_client.is_configured()}")
        
        # Validate input
        if not approved_emails:
            raise HTTPException(status_code=400, detail="No emails provided")
        
        # Check if Instantly is configured
        if send_mode == "instantly" and not instantly_client.is_configured():
            print("⚠️ Instantly not configured, falling back to simulation mode")
            send_mode = "fallback"
        
        if send_mode == "instantly":
            print("🚀 Using Instantly API mode")
            return await _send_emails_via_instantly(approved_emails, campaign_name)
        else:
            print("🎭 Using simulation mode")
            return await _send_emails_simulation(approved_emails)
            
    except Exception as e:
        print(f"❌ ERROR in send_emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send emails: {str(e)}")

async def _send_emails_via_instantly(approved_emails: list, campaign_name: str = None) -> dict:
    """Send emails using Instantly API via campaigns"""
    try:
        print(f"🎯 STARTING INSTANTLY EMAIL PROCESS:")
        
        # Generate campaign name if not provided
        if not campaign_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            campaign_name = f"Courier_Campaign_{timestamp}"
        
        print(f"   Campaign base name: {campaign_name}")
        
        # Group emails by subject/content for campaign creation
        # For simplicity, we'll create one campaign per unique subject
        campaigns_created = {}
        results = []
        
        # Group emails by subject
        email_groups = {}
        for email in approved_emails:
            subject = email.get("subject", "No Subject")
            if subject not in email_groups:
                email_groups[subject] = []
            email_groups[subject].append(email)
        
        print(f"📊 EMAIL GROUPING:")
        print(f"   Creating {len(email_groups)} campaign(s) for {len(approved_emails)} emails")
        for subject, emails in email_groups.items():
            print(f"   Group '{subject}': {len(emails)} emails")
        
        # Process each group
        for i, (subject, email_group) in enumerate(email_groups.items(), 1):
            print(f"\n🏗️ PROCESSING GROUP {i}/{len(email_groups)}:")
            print(f"   Subject: {subject}")
            print(f"   Emails in group: {len(email_group)}")
            
            try:
                # Create campaign with unique name for this group
                group_campaign_name = f"{campaign_name}_{len(campaigns_created) + 1}"
                print(f"   Creating campaign: {group_campaign_name}")
                
                campaign_id = instantly_client.create_campaign(
                    group_campaign_name, 
                    subject, 
                    email_group[0]['body']  # Use first email's body as template
                )
                campaigns_created[subject] = campaign_id
                print(f"   ✅ Campaign created with ID: {campaign_id}")
                
                # Add leads to the campaign
                print(f"   📋 Adding {len(email_group)} leads to campaign...")
                lead_addition_result = None
                try:
                    leads_response = instantly_client.add_leads_to_campaign(campaign_id, email_group)
                    print(f"   ✅ Leads added successfully: {leads_response}")
                    lead_addition_result = leads_response
                except Exception as lead_error:
                    print(f"   ⚠️ Warning: Failed to add leads to campaign: {lead_error}")
                    lead_addition_result = {
                        "error": str(lead_error),
                        "total_leads": len(email_group),
                        "successful_leads": 0,
                        "failed_leads": len(email_group)
                    }
                
                # Activate the campaign if leads were added successfully
                activation_result = None
                if lead_addition_result and lead_addition_result.get("successful_leads", 0) > 0:
                    try:
                        print(f"   🚀 Activating campaign...")
                        activation_result = instantly_client.activate_campaign(campaign_id)
                        print(f"   ✅ Campaign activated successfully!")
                    except Exception as activation_error:
                        print(f"   ⚠️ Warning: Failed to activate campaign: {activation_error}")
                        print(f"   📝 Campaign created but needs manual activation in Instantly dashboard")
                        activation_result = {
                            "error": str(activation_error),
                            "status": "needs_manual_activation",
                            "message": "Campaign created successfully but needs manual activation in Instantly dashboard"
                        }
                
                # Mark all emails in this group as successfully processed
                for email_data in email_group:
                    result_item = {
                        "to": email_data["to"],
                        "name": email_data["name"], 
                        "subject": subject,
                        "status": "success",
                        "message": f"Campaign '{group_campaign_name}' created successfully",
                        "campaign_id": campaign_id
                    }
                    
                    # Add lead addition details to the result
                    if lead_addition_result:
                        result_item["lead_addition"] = lead_addition_result
                    
                    # Add activation details to the result
                    if activation_result:
                        result_item["activation"] = activation_result
                        if activation_result.get("error"):
                            result_item["activation_status"] = "failed"
                            result_item["activation_message"] = "Campaign created but needs manual activation in dashboard"
                        else:
                            result_item["activation_status"] = "success"
                            result_item["activation_message"] = "Campaign activated and ready to send"
                    
                    results.append(result_item)
                
                print(f"   ✅ Group completed: {len(email_group)} emails added to campaign")
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Error creating campaign for subject '{subject}': {error_msg}")
                
                # Mark all emails in this group as failed
                for email_data in email_group:
                    results.append({
                        "to": email_data["to"],
                        "name": email_data["name"],
                        "subject": subject,
                        "status": "failed", 
                        "message": f"Campaign creation failed: {error_msg}"
                    })
        
        successful_sends = len([r for r in results if r["status"] == "success"])
        failed_sends = len([r for r in results if r["status"] == "failed"])
        activated_campaigns = len([r for r in results if r.get("activation_status") == "success"])
        
        print(f"\n📈 FINAL RESULTS:")
        print(f"   Total processed: {len(approved_emails)}")
        print(f"   Successful: {successful_sends}")
        print(f"   Failed: {failed_sends}")
        print(f"   Campaigns created: {len(campaigns_created)}")
        print(f"   Campaigns activated: {activated_campaigns}")
        
        return {
            "results": results,
            "total_processed": len(approved_emails),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "campaigns_created": list(campaigns_created.values()),
            "campaigns_activated": activated_campaigns,
            "message": f"Processed {len(approved_emails)} emails via Instantly API with automatic activation",
            "mode": "instantly"
        }
        
    except Exception as e:
        print(f"❌ ERROR in Instantly email sending: {e}")
        raise Exception(f"Instantly integration failed: {str(e)}")

async def _send_emails_simulation(approved_emails: list) -> dict:
    """Fallback simulation mode for when Instantly is not available"""
    results = []
    for email in approved_emails:
        results.append({
            "to": email.get("to", ""),
            "name": email.get("name", ""),
            "subject": email.get("subject", ""),
            "status": "sent (simulated)",
            "message": "Email sent successfully (demo mode - Instantly not configured)"
        })
    
    return {
        "results": results, 
        "total_processed": len(results),
        "successful_sends": len(results),
        "failed_sends": 0,
        "message": "All emails processed in simulation mode",
        "mode": "simulation"
    }

@app.post("/campaign-status/")
async def get_campaign_status(campaign_id: str = Body(...)):
    """Get status of a specific campaign"""
    try:
        if not instantly_client.is_configured():
            raise HTTPException(status_code=400, detail="Instantly API not configured")
        
        status = instantly_client.get_campaign_status(campaign_id)
        return {"campaign_id": campaign_id, "status": status}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get campaign status: {str(e)}")

@app.post("/pause-campaign/")
async def pause_campaign(campaign_id: str = Body(...)):
    """Pause a running campaign"""
    try:
        if not instantly_client.is_configured():
            raise HTTPException(status_code=400, detail="Instantly API not configured")
        
        result = instantly_client.pause_campaign(campaign_id)
        return {"campaign_id": campaign_id, "action": "paused", "result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause campaign: {str(e)}")

@app.post("/resume-campaign/")
async def resume_campaign(campaign_id: str = Body(...)):
    """Resume a paused campaign"""
    try:
        if not instantly_client.is_configured():
            raise HTTPException(status_code=400, detail="Instantly API not configured")
        
        result = instantly_client.resume_campaign(campaign_id)
        return {"campaign_id": campaign_id, "action": "resumed", "result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume campaign: {str(e)}")

@app.post("/activate-campaign/")
async def activate_campaign(campaign_id: str = Body(...)):
    """Activate a draft campaign"""
    try:
        if not instantly_client.is_configured():
            raise HTTPException(status_code=400, detail="Instantly API not configured")
        
        result = instantly_client.activate_campaign(campaign_id)
        return {"campaign_id": campaign_id, "action": "activated", "result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate campaign: {str(e)}")

@app.get("/test-campaign/{campaign_id}")
async def test_campaign_status(campaign_id: str):
    """Test endpoint to check campaign status and leads"""
    if not instantly_client.is_configured():
        return {"error": "Instantly API not configured", "mode": "simulation"}
    
    try:
        print(f"🔍 CHECKING CAMPAIGN STATUS: {campaign_id}")
        
        # Get campaign details
        campaign_status = instantly_client.get_campaign_status(campaign_id)
        print(f"📊 Campaign Status: {campaign_status}")
        
        return {
            "campaign_id": campaign_id,
            "status": "success",
            "campaign_details": campaign_status,
            "mode": "instantly"
        }
        
    except Exception as e:
        print(f"❌ Error checking campaign: {e}")
        return {
            "campaign_id": campaign_id,
            "error": str(e),
            "status": "failed"
        }

@app.get("/test-campaign-leads/{campaign_id}")
async def test_campaign_leads(campaign_id: str):
    """Test endpoint to check campaign leads"""
    if not instantly_client.is_configured():
        return {"error": "Instantly API not configured", "mode": "simulation"}
    
    try:
        print(f"🔍 CHECKING CAMPAIGN LEADS: {campaign_id}")
        
        # Get campaign leads
        campaign_leads = instantly_client.get_campaign_leads(campaign_id)
        print(f"📋 Campaign Leads: {campaign_leads}")
        
        return {
            "campaign_id": campaign_id,
            "status": "success",
            "leads": campaign_leads,
            "mode": "instantly"
        }
        
    except Exception as e:
        print(f"❌ Error checking campaign leads: {e}")
        return {
            "campaign_id": campaign_id,
            "error": str(e),
            "status": "failed"
        }

@app.post("/debug-lead-addition/")
async def debug_lead_addition():
    """Debug endpoint to test lead addition in deployment"""
    try:
        print("🔍 DEBUG: Testing lead addition in deployment environment")
        
        # Check client configuration
        client_info = {
            "is_configured": instantly_client.is_configured(),
            "api_key_last_10": instantly_client.api_key[-10:] if instantly_client.api_key else "None",
            "workspace_id": instantly_client.workspace_id,
            "email_account_id": instantly_client.email_account_id
        }
        
        print(f"📋 Client info: {client_info}")
        
        if not instantly_client.is_configured():
            return {
                "status": "error",
                "message": "Instantly client not configured",
                "client_info": client_info,
                "environment_check": {
                    "INSTANTLY_API_KEY": "SET" if os.getenv("INSTANTLY_API_KEY") else "NOT SET",
                    "INSTANTLY_WORKSPACE_ID": "SET" if os.getenv("INSTANTLY_WORKSPACE_ID") else "NOT SET", 
                    "INSTANTLY_EMAIL_ACCOUNT_ID": "SET" if os.getenv("INSTANTLY_EMAIL_ACCOUNT_ID") else "NOT SET"
                }
            }
        
        # Test creating a campaign
        print("📋 Testing campaign creation...")
        test_campaign_name = f"Debug_Test_{int(__import__('time').time())}"
        campaign_id = instantly_client.create_campaign(
            test_campaign_name,
            "Debug Test Subject",
            "Debug test body for deployment testing"
        )
        
        print(f"✅ Campaign created: {campaign_id}")
        
        # Test adding a lead
        print("📋 Testing lead addition...")
        test_contacts = [{
            "to": "deployment.debug@example.com",
            "name": "Deployment Debug",
            "company": "Debug Corp"
        }]
        
        lead_result = instantly_client.add_leads_to_campaign(campaign_id, test_contacts)
        
        print(f"✅ Lead addition result: {lead_result}")
        
        return {
            "status": "success",
            "message": "Debug test completed successfully",
            "client_info": client_info,
            "campaign_id": campaign_id,
            "campaign_name": test_campaign_name,
            "lead_addition_result": lead_result,
            "environment_check": {
                "INSTANTLY_API_KEY": "SET" if os.getenv("INSTANTLY_API_KEY") else "NOT SET",
                "INSTANTLY_WORKSPACE_ID": "SET" if os.getenv("INSTANTLY_WORKSPACE_ID") else "NOT SET",
                "INSTANTLY_EMAIL_ACCOUNT_ID": "SET" if os.getenv("INSTANTLY_EMAIL_ACCOUNT_ID") else "NOT SET"
            }
        }
        
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "status": "error",
            "message": f"Debug test failed: {str(e)}",
            "error_details": traceback.format_exc(),
            "client_info": {
                "is_configured": instantly_client.is_configured() if 'instantly_client' in locals() else False,
                "api_key_last_10": instantly_client.api_key[-10:] if 'instantly_client' in locals() and instantly_client.api_key else "None"
            }
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 