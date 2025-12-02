import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from twilio.rest import Client
from telegram import Bot
import sys
import os

# Import config from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import settings
except ImportError:
    # Fallback for Docker environment
    import os
    class Settings:
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "+14155238886")
        gmail_email = os.getenv("GMAIL_EMAIL", "")
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD", "")
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        environment = os.getenv("ENVIRONMENT", "development")
    settings = Settings()

logger = logging.getLogger(__name__)

class CommunicationManager:
    """Unified communication across multiple channels"""
    
    def __init__(self):
        # Always try to initialize real clients if credentials are provided
        logger.info(f"🔧 Initializing communication manager (env: {settings.environment})")
        
        # Check if we have real credentials
        has_twilio = (settings.twilio_account_sid and 
                     settings.twilio_account_sid != "your_twilio_account_sid")
        has_gmail = (settings.gmail_email and 
                    settings.gmail_email != "your_gmail_email")
        has_telegram = (settings.telegram_bot_token and 
                       settings.telegram_bot_token != "your_telegram_bot_token")
        
        if has_twilio or has_gmail or has_telegram:
            logger.info("✅ Real credentials detected - initializing live services")
        else:
            logger.info("🧪 No real credentials - using development mode")
        
        # Initialize services based on available credentials
        if True:  # Always try to initialize
            try:
                # Twilio
                self.twilio_client = Client(
                    settings.twilio_account_sid,
                    settings.twilio_auth_token
                )
                logger.info("✅ Twilio client initialized")
            except Exception as e:
                logger.warning(f"⚠️ Twilio initialization failed: {e}")
                self.twilio_client = None
            
            try:
                # Telegram
                self.telegram_bot = Bot(token=settings.telegram_bot_token)
                logger.info("✅ Telegram bot initialized")
            except Exception as e:
                logger.warning(f"⚠️ Telegram initialization failed: {e}")
                self.telegram_bot = None
            
            # Gmail SMTP
            self.gmail_email = settings.gmail_email
            self.gmail_app_password = settings.gmail_app_password
            logger.info("✅ Gmail SMTP configured")
    
    async def send_whatsapp(self, phone: str, message: str) -> Dict:
        """Send WhatsApp message via Twilio"""
        try:
            # Check if we have real Twilio credentials
            if not self.twilio_client:
                logger.info(f"🧪 MOCK WhatsApp to {phone}: {message[:50]}...")
                return {"status": "mock_sent", "channel": "whatsapp", "message_id": "mock_msg_123", "recipient": phone, "note": "Mock mode - add real Twilio credentials to send actual messages"}
            
            if not phone.startswith('+'):
                phone = f"+{phone}"
            
            msg = self.twilio_client.messages.create(
                from_=f"whatsapp:{settings.twilio_whatsapp_number}",
                to=f"whatsapp:{phone}",
                body=message
            )
            
            logger.info(f"✅ WhatsApp sent to {phone}: {msg.sid}")
            return {"status": "success", "channel": "whatsapp", "message_id": msg.sid, "recipient": phone}
        except Exception as e:
            logger.error(f"❌ WhatsApp error for {phone}: {str(e)}")
            return {"status": "failed", "channel": "whatsapp", "error": str(e), "recipient": phone}
    
    async def send_email(self, recipient_email: str, subject: str, body: str, html_body: str = None) -> Dict:
        """Send email via Gmail SMTP"""
        try:
            # Check if we have real Gmail credentials
            if (not self.gmail_email or 
                not self.gmail_app_password or 
                self.gmail_email == "your_gmail_email"):
                logger.info(f"🧪 MOCK Email to {recipient_email}: {subject}")
                return {"status": "mock_sent", "channel": "email", "recipient": recipient_email, "subject": subject, "note": "Mock mode - add real Gmail credentials to send actual emails"}
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.gmail_email
            msg['To'] = recipient_email
            
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_email, self.gmail_app_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent to {recipient_email}: {subject}")
            return {"status": "success", "channel": "email", "recipient": recipient_email, "subject": subject}
        except Exception as e:
            logger.error(f"❌ Email error for {recipient_email}: {str(e)}")
            return {"status": "failed", "channel": "email", "error": str(e), "recipient": recipient_email}
    
    async def send_telegram(self, chat_id: str, message: str) -> Dict:
        """Send Telegram message"""
        try:
            if not self.telegram_bot:
                logger.info(f"🧪 MOCK Telegram to {chat_id}: {message[:50]}...")
                return {"status": "mock_sent", "channel": "telegram", "message_id": "mock_tg_123", "recipient": chat_id, "note": "Mock mode - add real Telegram bot token to send actual messages"}
            
            msg = await self.telegram_bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"✅ Telegram message sent to {chat_id}: {msg.message_id}")
            return {"status": "success", "channel": "telegram", "message_id": msg.message_id, "recipient": chat_id}
        except Exception as e:
            logger.error(f"❌ Telegram error for {chat_id}: {str(e)}")
            return {"status": "failed", "channel": "telegram", "error": str(e), "recipient": chat_id}
    
    async def send_multi_channel(self, payload: Dict, channels: List[str]) -> List[Dict]:
        """Send notification across multiple channels"""
        results = []
        
        if "email" in channels:
            email_body = f"""Dear {payload['candidate_name']},

We have an update regarding your application for the position of {payload['job_title']} at BHIV.

Application Status: {payload['application_status'].upper()}

{payload['message']}

If you have any questions, please feel free to contact us.

Best regards,
BHIV HR Team"""
            result = await self.send_email(
                payload['candidate_email'],
                f"BHIV HR - {payload['job_title']} - {payload['application_status'].upper()}",
                email_body
            )
            results.append(result)
        
        if "whatsapp" in channels:
            whatsapp_msg = f"""*📢 BHIV HR Update*

*Job:* {payload['job_title']}
*Status:* {payload['application_status'].upper()}

{payload['message']}

_Thank you for your interest!_"""
            result = await self.send_whatsapp(payload['candidate_phone'], whatsapp_msg)
            results.append(result)
        
        if "telegram" in channels:
            # Try to send Telegram if chat_id is available
            chat_id = payload.get('candidate_telegram_id') or payload.get('telegram_chat_id')
            if chat_id:
                telegram_msg = f"""🔔 *BHIV HR Update*

*Job:* {payload['job_title']}
*Status:* {payload['application_status'].upper()}

{payload['message']}

_Thank you for your interest in BHIV!_"""
                result = await self.send_telegram(chat_id, telegram_msg)
                results.append(result)
            else:
                logger.info("ℹ️ Telegram skipped - no chat_id provided")
                results.append({"status": "skipped", "channel": "telegram", "reason": "No chat_id provided"})
        
        return results

# Singleton instance
comm_manager = CommunicationManager()