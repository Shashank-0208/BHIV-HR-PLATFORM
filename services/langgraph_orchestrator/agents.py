from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import CandidateApplicationState
from tools import *
from config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize LLM
try:
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0.7,
        api_key=settings.openai_api_key
    )
    logger.info(f"✅ LLM initialized: {settings.openai_model}")
except Exception as e:
    logger.error(f"❌ Failed to initialize LLM: {e}")
    llm = None

async def application_screener_agent(state: CandidateApplicationState) -> dict:
    """Agent that screens candidate applications using AI matching"""
    logger.info(f"🔍 Screening application {state['application_id']}")
    
    try:
        if not llm:
            logger.error("LLM not initialized")
            return {
                "application_status": "pending",
                "next_action": "error",
                "error": "LLM not available"
            }
        
        # Get AI matching score
        matching_result = await get_ai_matching_score.ainvoke({
            "candidate_id": state['candidate_id'],
            "job_id": state['job_id']
        })
        
        score = matching_result.get('score', 0)
        logger.info(f"AI Matching Score: {score}/100")
        
        # Prepare LLM for decision
        system_prompt = f"""You are an AI recruiter screening candidates for BHIV HR Platform.

Candidate: {state['candidate_name']}
Email: {state['candidate_email']}
Job Title: {state['job_title']}
AI Matching Score: {score}/100

Scoring Decision:
- ≥ 75: SHORTLIST (strong fit, recommend interview)
- 50-74: REVIEW (moderate fit, needs HR decision)
- < 50: REJECT (not suitable)

Provide brief reasoning for the decision."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="What is your recommendation?")
        ]
        
        response = await llm.ainvoke(messages)
        recommendation = response.content
        
        # Make decision based on score
        if score >= 75:
            next_action = "notify_shortlist"
            status = "shortlisted"
        elif score >= 50:
            next_action = "manual_review"
            status = "pending"
        else:
            next_action = "notify_reject"
            status = "rejected"
        
        logger.info(f"✅ Decision: {status} (score: {score})")
        
        return {
            "application_status": status,
            "next_action": next_action,
            "matching_score": float(score),
            "ai_recommendation": recommendation,
            "workflow_stage": "notification",
            "messages": state["messages"] + [
                HumanMessage(content="Screen this application"),
                response
            ]
        }
    
    except Exception as e:
        logger.error(f"❌ Screening error: {str(e)}")
        return {
            "next_action": "error",
            "error": str(e),
            "workflow_stage": "screening"
        }

async def notification_agent(state: CandidateApplicationState) -> dict:
    """Agent that sends multi-channel notifications"""
    logger.info(f"📢 Sending notifications for application {state['application_id']}")
    
    try:
        status = state["application_status"]
        
        if status == "shortlisted":
            message = f"""🎉 Congratulations {state['candidate_name']}!

You have been shortlisted for the position of {state['job_title']}!

Our HR team will contact you within 24-48 hours with the next steps.

AI Matching Score: {state.get('matching_score', 0)}/100

Best regards,
BHIV HR Team"""
            
        elif status == "rejected":
            message = f"""Thank you for your interest in {state['job_title']} at BHIV.

After careful review, we've decided to move forward with other candidates at this time.

Don't worry! We'll keep your profile in our system and notify you about future opportunities that match your profile.

Your Matching Score: {state.get('matching_score', 0)}/100

Best regards,
BHIV HR Team"""
        else:
            logger.info(f"⏭️ No notification needed for status: {status}")
            return {"notifications_sent": []}
        
        # Send notifications
        notification_result = await send_multi_channel_notification.ainvoke({
            "candidate_id": state["candidate_id"],
            "candidate_email": state["candidate_email"],
            "candidate_phone": state["candidate_phone"],
            "candidate_name": state["candidate_name"],
            "job_title": state["job_title"],
            "application_status": status,
            "message": message,
            "channels": ["email", "whatsapp"]
        })
        
        success = notification_result.get('success_count', 0)
        failed = notification_result.get('failed_count', 0)
        logger.info(f"✅ Notifications sent: {success} success, {failed} failed")
        
        return {
            "notifications_sent": notification_result.get("notifications", []),
            "workflow_stage": "hr_update",
            "next_action": "update_dashboard"
        }
    
    except Exception as e:
        logger.error(f"❌ Notification error: {str(e)}")
        return {
            "error": str(e),
            "notifications_sent": [],
            "workflow_stage": "notification"
        }

async def hr_update_agent(state: CandidateApplicationState) -> dict:
    """Agent that updates HR portal and database"""
    logger.info(f"📊 Updating HR dashboard for application {state['application_id']}")
    
    try:
        # Update application status in database
        await update_application_status.ainvoke({
            "application_id": state["application_id"],
            "status": state["application_status"],
            "notes": f"AI: {state.get('ai_recommendation', 'N/A')}"
        })
        
        # Update dashboard
        await update_hr_dashboard.ainvoke({
            "application_id": state["application_id"],
            "update_data": {
                "candidate_name": state["candidate_name"],
                "job_title": state["job_title"],
                "status": state["application_status"],
                "matching_score": state.get("matching_score", 0),
                "updated_at": datetime.now().isoformat()
            }
        })
        
        logger.info(f"✅ Dashboard synced for application {state['application_id']}")
        
        return {
            "workflow_stage": "feedback",
            "next_action": "collect_feedback"
        }
    
    except Exception as e:
        logger.error(f"❌ Dashboard update error: {str(e)}")
        return {
            "error": str(e),
            "workflow_stage": "hr_update"
        }

async def feedback_collection_agent(state: CandidateApplicationState) -> dict:
    """Agent that collects feedback for RL optimization"""
    logger.info(f"📝 Collecting feedback for application {state['application_id']}")
    
    try:
        feedback_data = {
            "candidate_id": state["candidate_id"],
            "job_id": state["job_id"],
            "application_id": state["application_id"],
            "candidate_name": state["candidate_name"],
            "ai_matching_score": state.get("matching_score", 0),
            "final_status": state["application_status"],
            "ai_recommendation": state.get("ai_recommendation", ""),
            "notifications_sent": len(state.get("notifications_sent", [])),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log for future learning
        await log_audit_event.ainvoke({
            "event_type": f"application_{state['application_status']}",
            "details": feedback_data
        })
        
        logger.info(f"✅ Feedback collected and logged")
        
        return {
            "workflow_stage": "completed",
            "sentiment": "positive" if state["application_status"] == "shortlisted" else "negative" if state["application_status"] == "rejected" else "neutral"
        }
    
    except Exception as e:
        logger.error(f"❌ Feedback collection error: {str(e)}")
        return {
            "error": str(e),
            "workflow_stage": "feedback"
        }