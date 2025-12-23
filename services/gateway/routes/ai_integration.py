from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import httpx
import os
from dependencies import get_api_key

router = APIRouter(prefix="/ai", tags=["AI Integration"])

@router.post("/test-communication")
async def test_communication_system(
    test_data: Dict,
    api_key_secret: str = Depends(get_api_key)
) -> Dict:
    """Test communication system via LangGraph"""
    try:
        langgraph_service_url = os.getenv("LANGGRAPH_SERVICE_URL", "https://bhiv-hr-langgraph.onrender.com")
        
        # Route to appropriate test endpoint
        channel = test_data.get("channel", "email")
        
        async with httpx.AsyncClient() as client:
            if channel == "email":
                email_params = {
                    "recipient_email": test_data.get("recipient_email", test_data.get("email", "test@test.com")),
                    "subject": test_data.get("subject", "Test Email"),
                    "message": test_data.get("message", "Test communication from BHIV HR")
                }
                response = await client.post(f"{langgraph_service_url}/test/send-email",
                                          params=email_params,
                                          headers={"Authorization": f"Bearer {api_key_secret}"},
                                          timeout=10.0)
            elif channel == "whatsapp":
                whatsapp_params = {
                    "phone": test_data.get("phone", test_data.get("recipient_phone", "+1234567890")),
                    "message": test_data.get("message", "Test WhatsApp message from BHIV HR")
                }
                response = await client.post(f"{langgraph_service_url}/test/send-whatsapp", 
                                          params=whatsapp_params,
                                          headers={"Authorization": f"Bearer {api_key_secret}"},
                                          timeout=10.0)
            elif channel == "telegram":
                telegram_params = {
                    "chat_id": test_data.get("chat_id", test_data.get("recipient_id", "123456")),
                    "message": test_data.get("message", "Test Telegram message from BHIV HR")
                }
                response = await client.post(f"{langgraph_service_url}/test/send-telegram",
                                          params=telegram_params, 
                                          headers={"Authorization": f"Bearer {api_key_secret}"},
                                          timeout=10.0)
            else:
                raise HTTPException(status_code=400, detail="Invalid channel")
            
        if response.status_code == 200:
            return {"success": True, "result": response.json()}
        else:
            return {"success": False, "error": f"LangGraph service returned {response.status_code}", "details": response.text[:200]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gemini/analyze")
async def analyze_with_gemini(
    request_data: Dict,
    api_key_secret: str = Depends(get_api_key)
) -> Dict:
    """Analyze text using Gemini AI"""
    try:
        text = request_data.get("text", "")
        analysis_type = request_data.get("analysis_type", "resume")
        
        if not text:
            raise HTTPException(status_code=422, detail="Text field is required")
        
        # Simulate Gemini analysis
        analysis_result = {
            "text_length": len(text),
            "analysis_type": analysis_type,
            "key_skills": ["Python", "Software Engineering", "Experience"] if "python" in text.lower() else ["General Skills"],
            "sentiment": "positive" if "experience" in text.lower() else "neutral",
            "summary": f"Analyzed {len(text)} characters of {analysis_type} content",
            "confidence_score": 0.85
        }
        
        return {"success": True, "analysis": analysis_result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))