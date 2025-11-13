"""
LangGraph Integration Routes for BHIV HR Platform
Replaces N8N with Python-based AI workflow orchestration
"""
import httpx
import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from datetime import datetime, timezone

router = APIRouter()

# LangGraph Service Configuration
LANGGRAPH_URL = os.getenv("LANGGRAPH_URL", "http://localhost:9001")
LANGGRAPH_PRODUCTION_URL = os.getenv("LANGGRAPH_PRODUCTION_URL", "https://bhiv-langgraph.onrender.com")

def get_langgraph_url():
    """Get appropriate LangGraph URL based on environment"""
    environment = os.getenv("ENVIRONMENT", "development")
    return LANGGRAPH_PRODUCTION_URL if environment == "production" else LANGGRAPH_URL

@router.post("/workflows/candidate-applied")
async def trigger_candidate_applied_workflow(payload: dict, background_tasks: BackgroundTasks):
    """
    Trigger LangGraph workflow when candidate applies
    Replaces N8N webhook: /webhooks/candidate-applied
    """
    try:
        workflow_payload = {
            "candidate_id": payload.get("candidate_id"),
            "job_id": payload.get("job_id"),
            "application_id": payload.get("application_id"),
            "candidate_email": payload.get("email"),
            "candidate_phone": payload.get("phone"),
            "candidate_name": payload.get("name"),
            "job_title": payload.get("job_title", "Position")
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{get_langgraph_url()}/workflows/application/start",
                json=workflow_payload
            )
            
            if response.status_code == 200:
                workflow_data = response.json()
                return {
                    "status": "langgraph_workflow_triggered",
                    "workflow_id": workflow_data.get("workflow_id"),
                    "message": "AI workflow processing started",
                    "triggered_at": datetime.now(timezone.utc).isoformat()
                }
            else:
                raise HTTPException(status_code=500, detail="LangGraph workflow failed to start")
                
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@router.post("/workflows/candidate-shortlisted")
async def trigger_candidate_shortlisted_workflow(payload: dict):
    """
    Trigger LangGraph workflow when candidate is shortlisted
    Replaces N8N webhook: /webhooks/candidate-shortlisted
    """
    try:
        notification_payload = {
            "candidate_id": payload.get("candidate_id"),
            "candidate_email": payload.get("email"),
            "candidate_phone": payload.get("phone"),
            "candidate_name": payload.get("name"),
            "job_title": payload.get("job_title"),
            "application_status": "shortlisted",
            "message": f"🎉 Congratulations! You've been shortlisted for {payload.get('job_title')}",
            "channels": ["email", "whatsapp"]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{get_langgraph_url()}/tools/send-notification",
                json=notification_payload
            )
            
            return {
                "status": "shortlist_notification_sent",
                "notification_result": response.json() if response.status_code == 200 else None,
                "triggered_at": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@router.post("/workflows/interview-scheduled")
async def trigger_interview_scheduled_workflow(payload: dict):
    """
    Trigger LangGraph workflow when interview is scheduled
    Replaces N8N webhook: /webhooks/interview-scheduled
    """
    try:
        notification_payload = {
            "candidate_id": payload.get("candidate_id"),
            "candidate_email": payload.get("email"),
            "candidate_phone": payload.get("phone"),
            "candidate_name": payload.get("name"),
            "job_title": payload.get("job_title"),
            "application_status": "interview_scheduled",
            "message": f"📅 Interview scheduled for {payload.get('job_title')} on {payload.get('date')} at {payload.get('time')}",
            "channels": ["email", "whatsapp"]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{get_langgraph_url()}/tools/send-notification",
                json=notification_payload
            )
            
            return {
                "status": "interview_notification_sent",
                "notification_result": response.json() if response.status_code == 200 else None,
                "triggered_at": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@router.get("/workflows/status")
async def get_langgraph_status():
    """Get LangGraph service status"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{get_langgraph_url()}/health")
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    "langgraph_service": "active",
                    "url": get_langgraph_url(),
                    "health": health_data,
                    "replacement_for": "N8N automation",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            else:
                return {
                    "langgraph_service": "unhealthy",
                    "url": get_langgraph_url(),
                    "status_code": response.status_code
                }
                
    except Exception as e:
        return {
            "langgraph_service": "unreachable",
            "url": get_langgraph_url(),
            "error": str(e)
        }