"""
N8N Notification Routes for BHIV HR Platform
Additional notification endpoints following Comat AI's structure
"""
import httpx
import os
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime, timezone

router = APIRouter()

# N8N Production Webhook URLs
N8N_GMAIL_WEBHOOK = os.getenv("N8N_GMAIL_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/1a108336-bfad-489c-8c38-4f907045a2ed")
N8N_WHATSAPP_WEBHOOK = os.getenv("N8N_WHATSAPP_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/aafbb77b-2dce-41c1-8c34-33fef4cb8ead")
N8N_TELEGRAM_WEBHOOK = os.getenv("N8N_TELEGRAM_WEBHOOK", "https://bhivhrplatform.app.n8n.cloud/webhook/17543422-01c7-4f75-ad76-9504c5fc9499")

@router.post("/notify/email")
async def send_email_notification(payload: dict):
    """
    Send email notification via N8N
    Expected payload: {
        "email": "candidate@example.com",
        "candidateName": "John Doe",
        "status": "Shortlisted",
        "message": "You have been shortlisted for the next round."
    }
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(N8N_GMAIL_WEBHOOK, json=payload)
            return {
                "status": "sent", 
                "service": "email",
                "response_code": response.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email notification failed: {str(e)}")

@router.post("/notify/whatsapp")
async def send_whatsapp_notification(payload: dict):
    """
    Send WhatsApp notification via N8N
    Expected payload: {
        "phone": "+1234567890",  # Format: +[country code][number]
        "candidateName": "John Doe",
        "status": "Interview Scheduled",
        "message": "Your interview is scheduled for tomorrow at 10 AM."
    }
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(N8N_WHATSAPP_WEBHOOK, json=payload)
            return {
                "status": "sent", 
                "service": "whatsapp",
                "response_code": response.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"WhatsApp notification failed: {str(e)}")

@router.post("/notify/telegram")
async def send_telegram_notification(payload: dict):
    """
    Send Telegram notification via N8N
    Expected payload: {
        "chatId": "123456789",  # Telegram chat ID or @username
        "candidateName": "John Doe",
        "status": "Offer Sent",
        "message": "Congratulations! We're pleased to offer you the position."
    }
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(N8N_TELEGRAM_WEBHOOK, json=payload)
            return {
                "status": "sent", 
                "service": "telegram",
                "response_code": response.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Telegram notification failed: {str(e)}")

@router.post("/notify/all")
async def send_all_notifications(payload: dict):
    """
    Send notifications via all channels
    Expected payload: {
        "email": "candidate@example.com",
        "phone": "+1234567890",
        "chatId": "123456789",
        "candidateName": "John Doe",
        "status": "Application Received",
        "message": "Thank you for applying. We'll review your application shortly."
    }
    """
    results = {}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Send email if provided
        if payload.get("email"):
            try:
                response = await client.post(N8N_GMAIL_WEBHOOK, json=payload)
                results["email"] = {"status": "sent", "code": response.status_code}
            except Exception as e:
                results["email"] = {"status": "failed", "error": str(e)}
        
        # Send WhatsApp if provided
        if payload.get("phone"):
            try:
                response = await client.post(N8N_WHATSAPP_WEBHOOK, json=payload)
                results["whatsapp"] = {"status": "sent", "code": response.status_code}
            except Exception as e:
                results["whatsapp"] = {"status": "failed", "error": str(e)}
        
        # Send Telegram if provided
        if payload.get("chatId"):
            try:
                response = await client.post(N8N_TELEGRAM_WEBHOOK, json=payload)
                results["telegram"] = {"status": "sent", "code": response.status_code}
            except Exception as e:
                results["telegram"] = {"status": "failed", "error": str(e)}
    
    return {
        "status": "processed", 
        "services": list(results.keys()),
        "results": results,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/notify/status")
async def get_notification_status():
    """Get N8N notification service status"""
    return {
        "n8n_workspace": "https://bhivhrplatform.app.n8n.cloud",
        "services": {
            "gmail": {"status": "active", "webhook": N8N_GMAIL_WEBHOOK},
            "whatsapp": {"status": "active", "webhook": N8N_WHATSAPP_WEBHOOK},
            "telegram": {"status": "active", "webhook": N8N_TELEGRAM_WEBHOOK}
        },
        "trial_days_left": 14,
        "monthly_executions": "5000 (free tier)",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }