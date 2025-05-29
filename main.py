from fastapi import FastAPI, UploadFile, File, Form, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import csv
import io
import requests
import os

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

@app.get("/")
async def root():
    return {"message": "Courier Email API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_configured": bool(openai_api_key)}

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
    campaign_content: str = Form(...)
):
    if not openai_client:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        )
    
    try:
        # Read and parse CSV file
        contents = await file.read()
        contacts = []
        
        try:
            reader = csv.DictReader(io.StringIO(contents.decode()))
            for row in reader:
                if row:  # Skip empty rows
                    contacts.append(row)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse CSV file: {str(e)}. Please ensure your CSV has headers and proper formatting."
            )
        
        if not contacts:
            raise HTTPException(
                status_code=400,
                detail="No valid contacts found in CSV file. Please check your file format."
            )

        print(f"Processing {len(contacts)} contacts...")
        emails = []
        
        for i, contact in enumerate(contacts):
            print(f"Generating email {i+1}/{len(contacts)} for {contact.get('name', 'Unknown')}")
            
            try:
                prompt = (
                    f"Write a professional, personalized marketing email to {contact.get('name', 'valued customer')} "
                    f"at {contact.get('company', 'their company')}.\n"
                    f"Campaign content: {campaign_content}\n"
                    f"Recipient details: {contact.get('position', '')} in {contact.get('industry', '')} industry\n"
                    f"Make it engaging, professional, and include a clear call-to-action. "
                    f"Keep it concise (under 200 words)."
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

        print(f"Successfully generated {len(emails)} emails")
        return {"emails": emails, "count": len(emails)}
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Unexpected error in generate_emails: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/send-emails/")
async def send_emails(approved_emails: list = Body(...)):
    # Placeholder for Instantly API integration
    try:
        results = []
        for email in approved_emails:
            # Here you would call Instantly's API
            # For now, just simulate success
            results.append({
                "to": email.get("to", ""),
                "name": email.get("name", ""),
                "status": "sent (simulated)",
                "message": "Email sent successfully (demo mode)"
            })
        
        return {
            "results": results, 
            "total_sent": len(results),
            "message": "All emails sent successfully (demo mode)"
        }
    
    except Exception as e:
        return {"error": f"Failed to send emails: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 