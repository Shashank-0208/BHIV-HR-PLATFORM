from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from .graphs import create_application_workflow
from .state import CandidateApplicationState
from .monitoring import monitor
from langchain_core.messages import HumanMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
import uuid
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BHIV LangGraph Orchestrator",
    version="1.0.0",
    description="AI-driven workflow orchestration for BHIV HR Platform"
)

# Initialize workflow
try:
    application_workflow = create_application_workflow()
    logger.info("✅ Application workflow initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize workflow: {str(e)}")
    application_workflow = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        logger.info(f"✅ WebSocket connected: {client_id}")
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            logger.info(f"❌ WebSocket disconnected: {client_id}")
    
    async def broadcast(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"WebSocket broadcast error: {str(e)}")

manager = ConnectionManager()

# Pydantic models
class ApplicationRequest(BaseModel):
    candidate_id: int
    job_id: int
    application_id: int
    candidate_email: str
    candidate_phone: str
    candidate_name: str
    job_title: str
    job_description: Optional[str] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    message: str
    timestamp: str

class WorkflowStatus(BaseModel):
    workflow_id: str
    current_stage: str
    application_status: str
    matching_score: float
    last_action: str
    completed: bool

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_data = monitor.get_health_status()
    health_data.update({
        "service": "langgraph-orchestrator",
        "version": "1.0.0",
        "environment": settings.environment
    })
    return health_data

@app.post("/workflows/application/start", response_model=WorkflowResponse)
async def start_application_workflow(
    request: ApplicationRequest,
    background_tasks: BackgroundTasks
):
    """Start candidate application processing workflow"""
    try:
        if not application_workflow:
            raise HTTPException(status_code=500, detail="Workflow not initialized")
        
        workflow_id = str(uuid.uuid4())
        logger.info(f"🚀 Starting workflow {workflow_id} for application {request.application_id}")
        
        # Initialize state
        initial_state: CandidateApplicationState = {
            "candidate_id": request.candidate_id,
            "job_id": request.job_id,
            "application_id": request.application_id,
            "candidate_email": request.candidate_email,
            "candidate_phone": request.candidate_phone,
            "candidate_name": request.candidate_name,
            "job_title": request.job_title,
            "job_description": request.job_description or "",
            "application_status": "pending",
            "messages": [HumanMessage(content=f"New application from {request.candidate_name} for {request.job_title}")],
            "notifications_sent": [],
            "matching_score": 0.0,
            "ai_recommendation": "",
            "sentiment": "neutral",
            "next_action": "screening",
            "workflow_stage": "screening",
            "error": None,
            "timestamp": datetime.now().isoformat(),
            "voice_input_path": None,
            "voice_response_path": None
        }
        
        # Execute workflow in background
        config = {"configurable": {"thread_id": workflow_id}}
        background_tasks.add_task(
            _execute_workflow,
            workflow_id,
            initial_state,
            config
        )
        
        logger.info(f"✅ Workflow {workflow_id} scheduled for execution")
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="started",
            message=f"Application workflow started for {request.candidate_name}",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"❌ Error starting workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workflows/{workflow_id}/status", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str):
    """Get current status of a workflow"""
    try:
        config = {"configurable": {"thread_id": workflow_id}}
        state = await application_workflow.aget_state(config)
        
        values = state.values
        return WorkflowStatus(
            workflow_id=workflow_id,
            current_stage=values.get("workflow_stage", "unknown"),
            application_status=values.get("application_status", "pending"),
            matching_score=values.get("matching_score", 0.0),
            last_action=values.get("next_action", ""),
            completed=state.next == [] or not state.next
        )
    
    except Exception as e:
        logger.error(f"❌ Error fetching workflow status: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Workflow not found: {str(e)}")

@app.post("/workflows/{workflow_id}/resume")
async def resume_workflow(workflow_id: str):
    """Resume a paused workflow"""
    try:
        config = {"configurable": {"thread_id": workflow_id}}
        result = await application_workflow.ainvoke(None, config)
        
        return {
            "workflow_id": workflow_id,
            "status": "resumed",
            "result": result
        }
    
    except Exception as e:
        logger.error(f"❌ Error resuming workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{workflow_id}")
async def websocket_endpoint(websocket: WebSocket, workflow_id: str):
    """WebSocket endpoint for real-time workflow updates"""
    await manager.connect(websocket, workflow_id)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"WebSocket received: {data}")
            await manager.broadcast(workflow_id, {"type": "update", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, workflow_id)

@app.get("/workflows")
async def list_workflows():
    """List all active workflows"""
    return {
        "note": "Workflow tracking requires persistence layer",
        "status": "workflow_management_available"
    }

# Background task
async def _execute_workflow(workflow_id: str, state: dict, config: dict):
    """Execute workflow in background and broadcast updates"""
    try:
        logger.info(f"⏳ Executing workflow {workflow_id}")
        result = await application_workflow.ainvoke(state, config)
        logger.info(f"✅ Workflow {workflow_id} completed: {result.get('application_status')}")
        
        # Broadcast completion
        await manager.broadcast(workflow_id, {
            "type": "completed",
            "workflow_id": workflow_id,
            "status": result.get("application_status"),
            "matching_score": result.get("matching_score", 0),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ Workflow {workflow_id} failed: {str(e)}")
        await manager.broadcast(workflow_id, {
            "type": "error",
            "workflow_id": workflow_id,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })