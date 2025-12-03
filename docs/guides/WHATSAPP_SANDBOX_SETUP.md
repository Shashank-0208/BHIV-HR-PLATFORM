# WhatsApp Sandbox Setup Guide

## Issue: Used "stop" command - Need to rejoin sandbox

### Quick Solution (Same Number):

**You can restart with the same number (+14155238886):**

1. **Send "START" message:**
   - Send WhatsApp to: +14155238886
   - Message: `START`
   - This reactivates your number

2. **If START doesn't work, rejoin:**
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Get current join code
   - Send: `join <keyword>` to +14155238886

3. **Test immediately:**
   ```bash
   python send_test_messages.py
   ```

### Alternative: Reset Sandbox (if needed):

1. **Twilio Console:**
   - Visit: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Click "Reset Sandbox" (generates new join code)

2. **Join with new code:**
   - Send: `join <new-keyword>` to +14155238886

## Alternative: Use Different Twilio Number

If sandbox reset doesn't work:
1. Create new Twilio account
2. Get new WhatsApp sandbox number
3. Update credentials in .env file

## Current Status:
- ✅ Gmail: Working
- ✅ Twilio API: Working  
- ✅ WhatsApp: Working (+919284967526 verified)
- ❌ Telegram: Need new bot token

## Email Automation Added:
- ✅ Interview scheduling notifications
- ✅ Application received confirmations  
- ✅ Shortlist notifications
- ✅ Assessment completion emails

The HR portal now automatically sends emails when:
1. Interview is scheduled
2. Candidates are uploaded
3. Candidates are shortlisted
4. Assessments are completed