from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
import logging
from datetime import datetime
import os

router = APIRouter()
logger = logging.getLogger(__name__)

LANGGRAPH_URL = os.getenv("LANGGRAPH_URL", "http://localhost:9001")

class LangGraphApplicationRequest(BaseModel):
    candidate_id: int
    job_id: int
    application_id: int
    candidate_email: str
    candidate_phone: str
    candidate_name: str
    job_title: str
    job_description: str = ""

@router.post("/langgraph/trigger-workflow")
async def trigger_langgraph_workflow(request: LangGraphApplicationRequest):
    """Trigger LangGraph workflow for candidate application processing"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LANGGRAPH_URL}/workflows/application/start",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"LangGraph workflow started: {result.get('workflow_id')}")
            
            return {
                "status": "langgraph_workflow_triggered",
                "workflow_id": result.get("workflow_id"),
                "message": result.get("message"),
                "triggered_at": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"LangGraph workflow trigger failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "triggered_at": datetime.now().isoformat()
        }

@router.get("/langgraph/workflow/{workflow_id}/status")
async def get_langgraph_workflow_status(workflow_id: str):
    """Get LangGraph workflow status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{LANGGRAPH_URL}/workflows/{workflow_id}/status",
                timeout=10.0
            )
            response.raise_for_status()
            
            return response.json()
    except Exception as e:
        logger.error(f"LangGraph status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/langgraph/health")
async def check_langgraph_health():
    """Check LangGraph orchestrator health"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{LANGGRAPH_URL}/health",
                timeout=5.0
            )
            response.raise_for_status()
            
            return {
                "langgraph_status": "healthy",
                "service_response": response.json(),
                "checked_at": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "langgraph_status": "unhealthy",
            "error": str(e),
            "checked_at": datetime.now().isoformat()
        }