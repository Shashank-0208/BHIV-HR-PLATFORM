# 📧 Communication Setup Guide

## 🚀 Quick Setup for Real Notifications

### 1. 📧 Gmail Email Setup
1. Go to your Gmail account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Google Account → Security → App passwords
   - Generate password for "Mail"
4. Add to your `.env` file:
```bash
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

### 2. 📱 WhatsApp Setup (Twilio)
1. Sign up at [Twilio](https://www.twilio.com)
2. Get your Account SID and Auth Token
3. Set up WhatsApp Sandbox or get approved number
4. Add to your `.env` file:
```bash
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### 3. 🤖 Telegram Bot Setup
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the bot token
5. Add to your `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
TELEGRAM_BOT_USERNAME=your-bot-username
```

### 4. 🧠 Gemini AI Setup
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Create API key
3. Add to your `.env` file:
```bash
GEMINI_API_KEY=AIzaSyC8vbbDqAgcFIHw6fAT4Ta6Nr7zsG5ELIs
```

## 🧪 Testing Steps

### Step 1: Access HR Portal
1. Go to [HR Portal](https://bhiv-hr-portal-u670.onrender.com/)
2. Navigate to "Communication Testing" in sidebar

### Step 2: Test Each Channel
1. **Email Test**: Enter your email and send test
2. **WhatsApp Test**: Enter phone number (+1234567890 format)
3. **Telegram Test**: Get your chat ID by messaging your bot
4. **Multi-Channel**: Test all channels together

### Step 3: Verify Results
- Check email inbox
- Check WhatsApp messages
- Check Telegram messages
- Review response status in portal

## 🔧 Getting Chat ID for Telegram

### Method 1: Direct Message
1. Start your bot by sending `/start`
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for "chat":{"id": YOUR_CHAT_ID}

### Method 2: Use @userinfobot
1. Message @userinfobot on Telegram
2. It will show your chat ID

## 📊 Current Status

Your system is configured for:
- ✅ **Mock Mode**: Shows test messages in logs
- 🔄 **Real Mode**: Activates when credentials are added

## 🚨 Troubleshooting

### Email Not Working
- Check Gmail app password (not regular password)
- Ensure 2FA is enabled
- Verify email format

### WhatsApp Not Working
- Check Twilio account balance
- Verify phone number format (+country code)
- Ensure WhatsApp sandbox is active

### Telegram Not Working
- Verify bot token format
- Check if bot is active
- Ensure chat ID is correct

## 📱 Manual Testing URLs

### Test Endpoints (with API key):
```bash
# Email Test
POST https://bhiv-hr-langgraph.onrender.com/test/send-email
Headers: Authorization: Bearer <YOUR_API_KEY>
Params: recipient_email, subject, message

# WhatsApp Test  
POST https://bhiv-hr-langgraph.onrender.com/test/send-whatsapp
Headers: Authorization: Bearer <YOUR_API_KEY>
Params: phone, message

# Telegram Test
POST https://bhiv-hr-langgraph.onrender.com/test/send-telegram  
Headers: Authorization: Bearer <YOUR_API_KEY>
Params: chat_id, message
```

## 🎯 Next Steps

1. **Add Real Credentials**: Update `.env` with actual values
2. **Test in Portal**: Use "Communication Testing" section
3. **Verify Delivery**: Check all channels receive messages
4. **Production Use**: Notifications will work in workflows

---

**Note**: Without real credentials, system runs in mock mode showing test responses.