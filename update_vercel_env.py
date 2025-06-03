import json

print("VERCEL ENVIRONMENT VARIABLE UPDATE INSTRUCTIONS")
print("="*70)

print("PROBLEM: Your Vercel deployment is using the old email account")
print("   Current (invalid): tim@biscred.com")
print("   Required (valid):  alex@biscred.ai")

print("\nSTEP-BY-STEP INSTRUCTIONS:")
print("1. Go to: https://vercel.com/dashboard")
print("2. Find your project: sender-sigma")
print("3. Go to Settings > Environment Variables")
print("4. Update INSTANTLY_EMAIL_ACCOUNT_ID:")
print("   From: tim@biscred.com")
print("   To:   alex@biscred.ai")
print("5. Click 'Save'")
print("6. Redeploy the project")

print("\nCORRECT ENVIRONMENT VARIABLES:")
print("INSTANTLY_EMAIL_ACCOUNT_ID=alex@biscred.ai")

print("\nCRITICAL: The system won't activate campaigns until this is fixed!")

print("\nAFTER UPDATING:")
print("1. Wait for Vercel to redeploy")
print("2. Test with your business email CSV (not Gmail)")
print("3. Campaigns should now activate automatically")

print("\n" + "="*70)
print("Once updated, your system will:")
print("✅ Create campaigns")
print("✅ Add contacts")  
print("✅ ACTIVATE campaigns automatically")
print("="*70) 