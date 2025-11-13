"""
N8N Notification Service Integration for BHIV HR Platform
Production-ready async notification service using httpx
"""
import httpx
import os
from typing import Dict, Optional
from datetime import datetime, timezone

class NotificationService:
    """N8N Notification Service Integration"""
    
    def __init__(self):
        self.gmail_webhook = os.getenv("N8N_GMAIL_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/1a108336-bfad-489c-8c38-4f907045a2ed")
        self.whatsapp_webhook = os.getenv("N8N_WHATSAPP_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/aafbb77b-2dce-41c1-8c34-33fef4cb8ead")
        self.telegram_webhook = os.getenv("N8N_TELEGRAM_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/17543422-01c7-4f75-ad76-9504c5fc9499")
    
    async def send_email(
        self,
        email: str,
        candidate_name: str,
        status: str,
        message: str
    ) -> Dict:
        """Send email notification via N8N"""
        payload = {
            "email": email,
            "candidateName": candidate_name,
            "status": status,
            "message": message
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.gmail_webhook, json=payload)
                return {
                    "status": "sent", 
                    "service": "email", 
                    "response_code": response.status_code,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            except Exception as e:
                return {
                    "status": "failed", 
                    "service": "email", 
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
    
    async def send_whatsapp(
        self,
        phone: str,
        candidate_name: str,
        status: str,
        message: str
    ) -> Dict:
        """Send WhatsApp notification via N8N"""
        # Phone must be in format: +1234567890
        # User must have joined Twilio sandbox first
        payload = {
            "phone": phone,
            "candidateName": candidate_name,
            "status": status,
            "message": message
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.whatsapp_webhook, json=payload)
                return {
                    "status": "sent", 
                    "service": "whatsapp", 
                    "response_code": response.status_code,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            except Exception as e:
                return {
                    "status": "failed", 
                    "service": "whatsapp", 
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
    
    async def send_telegram(
        self,
        chat_id: str,
        candidate_name: str,
        status: str,
        message: str
    ) -> Dict:
        """Send Telegram notification via N8N"""
        payload = {
            "chatId": chat_id,
            "candidateName": candidate_name,
            "status": status,
            "message": message
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.telegram_webhook, json=payload)
                return {
                    "status": "sent", 
                    "service": "telegram", 
                    "response_code": response.status_code,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            except Exception as e:
                return {
                    "status": "failed", 
                    "service": "telegram", 
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
    
    async def send_all_channels(
        self,
        email: str,
        phone: Optional[str],
        chat_id: Optional[str],
        candidate_name: str,
        status: str,
        message: str
    ) -> Dict:
        """Send notification to all available channels"""
        results = {}
        
        # Always send email
        results["email"] = await self.send_email(email, candidate_name, status, message)
        
        # Send WhatsApp if phone provided
        if phone:
            results["whatsapp"] = await self.send_whatsapp(phone, candidate_name, status, message)
        
        # Send Telegram if chat_id provided
        if chat_id:
            results["telegram"] = await self.send_telegram(chat_id, candidate_name, status, message)
        
        return {
            "status": "processed",
            "channels": list(results.keys()),
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global notification service instance
notification_service = NotificationService()

# Convenience functions for easy import
async def notify_candidate_applied(email: str, name: str, job_title: str, phone: Optional[str] = None):
    """Notify candidate that application was received"""
    return await notification_service.send_all_channels(
        email=email,
        phone=phone,
        chat_id=None,
        candidate_name=name,
        status="Application Received",
        message=f"Thank you for applying for {job_title}. We'll review your application shortly."
    )

async def notify_candidate_shortlisted(email: str, name: str, job_title: str):
    """Notify candidate they were shortlisted"""
    return await notification_service.send_email(
        email=email,
        candidate_name=name,
        status="Shortlisted",
        message=f"Congratulations! You have been shortlisted for {job_title}. We'll contact you soon for the next steps."
    )

async def notify_interview_scheduled(email: str, name: str, job_title: str, date: str, time: str, interviewer: str = "HR Team"):
    """Notify candidate about scheduled interview"""
    return await notification_service.send_email(
        email=email,
        candidate_name=name,
        status="Interview Scheduled",
        message=f"Your interview for {job_title} is scheduled for {date} at {time}. Interviewer: {interviewer}"
    )