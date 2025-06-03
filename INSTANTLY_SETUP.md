# 📧 Instantly API Integration Setup

## Overview
Your email sending workflow now supports **real email delivery** via Instantly API! This replaces the previous simulation mode with actual campaign-based email sending.

## 🔧 Setup Steps

### 1. Get Instantly API Credentials
1. Sign up/login at [instantly.ai](https://instantly.ai)
2. Connect your email account(s) to Instantly
3. Go to **Workspace Settings** > **API Keys**
4. Create a new API key with these scopes:
   - `campaigns:read`
   - `campaigns:create`
   - `emails:create`
   - `leads:create`

### 2. Configure Environment Variables
1. Copy `env_template.txt` to `.env`
2. Add your credentials:
```bash
OPENAI_API_KEY=your_openai_key
INSTANTLY_API_KEY=your_instantly_api_key
INSTANTLY_WORKSPACE_ID=your_workspace_id
INSTANTLY_EMAIL_ACCOUNT_ID=your_connected_email_id
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test the Integration
```bash
python main.py
```

Visit `http://localhost:8000/health` to verify all services are configured.

## 🎯 How It Works Now

### Email Sending Process:
1. **Generate Emails**: Upload contacts → AI generates personalized emails
2. **Review & Approve**: Review generated emails in frontend
3. **Send via Instantly**: Creates campaigns → Adds leads → Sends emails

### Campaign Creation:
- Groups emails by subject line
- Creates separate campaigns for different subjects
- Adds all recipients as leads to appropriate campaigns
- Tracks campaign IDs for monitoring

### Fallback Mode:
- If Instantly API is not configured, falls back to simulation mode
- No emails sent, but workflow continues normally
- Perfect for testing and development

## 📊 New API Endpoints

### Enhanced Send Emails
```http
POST /send-emails/
{
  "approved_emails": [...],
  "campaign_name": "My Campaign",
  "send_mode": "instantly"  // or "fallback"
}
```

### Campaign Management
```http
POST /campaign-status/
{"campaign_id": "campaign_uuid"}

POST /pause-campaign/
{"campaign_id": "campaign_uuid"}

POST /resume-campaign/
{"campaign_id": "campaign_uuid"}
```

## ✅ Features Added

- ✅ **Real email sending** via Instantly campaigns
- ✅ **Campaign grouping** by subject/content
- ✅ **Lead management** and tracking
- ✅ **Campaign pause/resume** controls
- ✅ **Status monitoring** and analytics
- ✅ **Graceful fallback** when Instantly unavailable
- ✅ **Error handling** and retry logic

## 🔍 Testing

1. **Health Check**: `GET /health` - Shows Instantly configuration status
2. **Test Mode**: Set `send_mode: "fallback"` for simulation
3. **Live Mode**: Set `send_mode: "instantly"` for real sending

## 🚨 Important Notes

- **Instantly Limitation**: Cannot send one-off emails - everything must be campaign-based
- **Campaign Strategy**: System auto-groups emails by subject to create campaigns
- **Rate Limiting**: Instantly API has rate limits - system handles this automatically
- **Cost**: Instantly charges per email sent - monitor usage

## 🎯 Next Steps

Your email workflow now supports:
1. **Immediate Use**: Configure credentials and start sending real emails
2. **Campaign Analytics**: Monitor open rates, clicks, replies
3. **Follow-up Sequences**: Extend campaigns with multiple email steps
4. **Reply Management**: Handle responses automatically

## 📞 Support

If you encounter issues:
1. Check `/health` endpoint for configuration status
2. Review server logs for Instantly API errors
3. Verify your Instantly account has connected email accounts
4. Ensure API key has proper scopes

---
**Status**: ✅ Integration Complete - Ready for Production Use! 