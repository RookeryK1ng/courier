from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
import openai
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

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "Courier Email API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_configured": bool(openai.api_key)}

@app.post("/generate-emails/")
async def generate_emails(
    file: UploadFile = File(...),
    campaign_content: str = Form(...)
):
    if not openai.api_key:
        return {"error": "OpenAI API key not configured"}
    
    try:
        contents = await file.read()
        contacts = []
        reader = csv.DictReader(io.StringIO(contents.decode()))
        for row in reader:
            contacts.append(row)

        emails = []
        for contact in contacts:
            prompt = (
                f"Write a professional, personalized marketing email to {contact.get('name', 'valued customer')} "
                f"at {contact.get('company', 'their company')}.\n"
                f"Campaign content: {campaign_content}\n"
                f"Recipient email: {contact.get('email', '')}\n"
                f"Make it engaging, professional, and include a clear call-to-action."
            )
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            email_text = response.choices[0].message['content']
            emails.append({
                "to": contact.get('email', ''),
                "name": contact.get('name', ''),
                "company": contact.get('company', ''),
                "subject": f"Exciting Partnership Opportunity - {contact.get('company', 'Your Company')}",
                "body": email_text
            })

        return {"emails": emails, "count": len(emails)}
    
    except Exception as e:
        return {"error": f"Failed to generate emails: {str(e)}"}

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