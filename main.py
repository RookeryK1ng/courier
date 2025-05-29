from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
import openai
import csv
import io
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

@app.post("/generate-emails/")
async def generate_emails(
    file: UploadFile = File(...),
    campaign_content: str = Form(...)
):
    contents = await file.read()
    contacts = []
    reader = csv.DictReader(io.StringIO(contents.decode()))
    for row in reader:
        contacts.append(row)

    emails = []
    for contact in contacts:
        prompt = (
            f"Write a professional marketing email to {contact['name']} at {contact['company']}.\n"
            f"Campaign content: {campaign_content}\n"
            f"Recipient email: {contact['email']}\n"
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        email_text = response.choices[0].message['content']
        emails.append({
            "to": contact['email'],
            "subject": "Your Subject Here",
            "body": email_text
        })

    return {"emails": emails}

@app.post("/send-emails/")
async def send_emails(approved_emails: list = Body(...)):
    # Placeholder for Instantly API integration
    results = []
    for email in approved_emails:
        # Here you would call Instantly's API
        # For now, just simulate success
        results.append({
            "to": email["to"],
            "status": "sent (simulated)"
        })
    return {"results": results} 