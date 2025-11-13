#!/usr/bin/env python3
"""
Comprehensive Integration Test for BHIV LangGraph Service
Tests all endpoints, configuration, and integration with Gateway
"""
import asyncio
import httpx
import json
from datetime import datetime

LANGGRAPH_URL = "http://localhost:9001"
GATEWAY_URL = "http://localhost:8000"

async def test_service_health():
    """Test both services are healthy"""
    print("🔍 Testing Service Health...")
    
    try:
        async with httpx.AsyncClient() as client:
            # Test LangGraph health
            lg_response = await client.get(f"{LANGGRAPH_URL}/health")
            lg_healthy = lg_response.status_code == 200
            
            # Test Gateway health
            gw_response = await client.get(f"{GATEWAY_URL}/health")
            gw_healthy = gw_response.status_code == 200
            
            print(f"  ✅ LangGraph Service: {'Healthy' if lg_healthy else 'Unhealthy'}")
            print(f"  ✅ Gateway Service: {'Healthy' if gw_healthy else 'Unhealthy'}")
            
            if lg_healthy and gw_healthy:
                lg_data = lg_response.json()
                gw_data = gw_response.json()
                print(f"  📊 LangGraph uptime: {lg_data.get('uptime_seconds', 0)}s")
                print(f"  📊 Gateway version: {gw_data.get('version', 'unknown')}")
                return True
            return False
            
    except Exception as e:
        print(f"  ❌ Health check failed: {e}")
        return False

async def test_workflow_creation():
    """Test workflow creation endpoint"""
    print("\n🚀 Testing Workflow Creation...")
    
    payload = {
        "candidate_id": 1,
        "job_id": 1,
        "application_id": 123,
        "candidate_email": "john.doe@example.com",
        "candidate_phone": "+1234567890",
        "candidate_name": "John Doe",
        "job_title": "Senior Python Developer",
        "job_description": "Develop scalable backend systems using Python and FastAPI"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LANGGRAPH_URL}/workflows/application/start",
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                workflow_id = data.get('workflow_id')
                print(f"  ✅ Workflow created: {workflow_id}")
                print(f"  📝 Status: {data.get('status')}")
                print(f"  💬 Message: {data.get('message')}")
                return workflow_id
            else:
                print(f"  ❌ Workflow creation failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return None
                
    except Exception as e:
        print(f"  ❌ Workflow creation error: {e}")
        return None

async def test_workflow_status(workflow_id: str):
    """Test workflow status endpoint"""
    print(f"\n📊 Testing Workflow Status for {workflow_id}...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LANGGRAPH_URL}/workflows/{workflow_id}/status")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Status retrieved successfully")
                print(f"  🎯 Current stage: {data.get('current_stage')}")
                print(f"  📋 Application status: {data.get('application_status')}")
                print(f"  🎯 Matching score: {data.get('matching_score')}")
                print(f"  ⚡ Last action: {data.get('last_action')}")
                print(f"  ✅ Completed: {data.get('completed')}")
                return True
            else:
                print(f"  ⚠️ Status check returned: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"  ❌ Status check error: {e}")
        return False

async def test_api_documentation():
    """Test API documentation endpoint"""
    print("\n📚 Testing API Documentation...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LANGGRAPH_URL}/docs")
            
            if response.status_code == 200:
                print(f"  ✅ API docs available at: {LANGGRAPH_URL}/docs")
                return True
            else:
                print(f"  ❌ API docs failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"  ❌ API docs error: {e}")
        return False

async def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        # Import and test config
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config import settings
        
        print(f"  ✅ Config loaded successfully")
        print(f"  🌐 Gateway URL: {settings.gateway_url}")
        print(f"  🔧 Environment: {settings.environment}")
        print(f"  📊 Log level: {settings.log_level}")
        print(f"  🤖 OpenAI model: {settings.openai_model}")
        print(f"  🔑 API key configured: {'Yes' if settings.api_key_secret != 'your-api-key' else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

async def test_mock_communication():
    """Test mock communication in development mode"""
    print("\n📞 Testing Mock Communication...")
    
    try:
        # Import communication manager
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))
        from app.communication import comm_manager
        
        # Test mock email
        email_result = await comm_manager.send_email(
            "test@example.com",
            "Test Subject",
            "Test body content"
        )
        
        # Test mock WhatsApp
        whatsapp_result = await comm_manager.send_whatsapp(
            "+1234567890",
            "Test WhatsApp message"
        )
        
        print(f"  ✅ Mock email: {email_result.get('status')}")
        print(f"  ✅ Mock WhatsApp: {whatsapp_result.get('status')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Communication test error: {e}")
        return False

async def main():
    """Run comprehensive integration tests"""
    print("🧪 BHIV LangGraph Service - Comprehensive Integration Test")
    print("=" * 60)
    
    results = []
    
    # Test 1: Service Health
    health_ok = await test_service_health()
    results.append(("Service Health", health_ok))
    
    if not health_ok:
        print("\n❌ Services not healthy. Please ensure both services are running:")
        print(f"  - LangGraph: {LANGGRAPH_URL}")
        print(f"  - Gateway: {GATEWAY_URL}")
        return
    
    # Test 2: Configuration
    config_ok = await test_configuration()
    results.append(("Configuration", config_ok))
    
    # Test 3: Mock Communication
    comm_ok = await test_mock_communication()
    results.append(("Mock Communication", comm_ok))
    
    # Test 4: API Documentation
    docs_ok = await test_api_documentation()
    results.append(("API Documentation", docs_ok))
    
    # Test 5: Workflow Creation
    workflow_id = await test_workflow_creation()
    workflow_ok = workflow_id is not None
    results.append(("Workflow Creation", workflow_ok))
    
    if workflow_id:
        # Wait for workflow to process
        print("\n⏳ Waiting 5 seconds for workflow to process...")
        await asyncio.sleep(5)
        
        # Test 6: Workflow Status
        status_ok = await test_workflow_status(workflow_id)
        results.append(("Workflow Status", status_ok))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! LangGraph service is fully operational.")
        print(f"\n🚀 Service URLs:")
        print(f"  - LangGraph API: {LANGGRAPH_URL}")
        print(f"  - API Documentation: {LANGGRAPH_URL}/docs")
        print(f"  - Health Check: {LANGGRAPH_URL}/health")
    else:
        print("⚠️ Some tests failed. Please check the logs above.")

if __name__ == "__main__":
    asyncio.run(main())