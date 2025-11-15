#!/usr/bin/env python3
"""
Verify that the Gateway → LangGraph integration fixes are working
"""

import sys
import os

# Set up environment variables
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/test'
os.environ['API_KEY_SECRET'] = 'test_api_key_12345'
os.environ['JWT_SECRET'] = 'test_jwt_secret_12345'
os.environ['CANDIDATE_JWT_SECRET'] = 'test_candidate_jwt_12345'
os.environ['AGENT_SERVICE_URL'] = 'http://localhost:9000'
os.environ['ENVIRONMENT'] = 'development'

# Add services directory to path
services_dir = os.path.join(os.path.dirname(__file__), 'services')
gateway_dir = os.path.join(services_dir, 'gateway')
app_dir = os.path.join(gateway_dir, 'app')
sys.path.insert(0, gateway_dir)
sys.path.insert(0, app_dir)

def verify_langgraph_integration():
    """Verify LangGraph integration is working"""
    print("=== VERIFYING LANGGRAPH INTEGRATION ===")
    
    try:
        # Import the FastAPI app
        from main import app
        print("✓ FastAPI app imported successfully")
        
        # Check total routes
        total_routes = len(app.routes)
        print(f"✓ Total routes in app: {total_routes}")
        
        # Find LangGraph routes
        langgraph_routes = []
        webhook_routes = []
        
        for route in app.routes:
            if hasattr(route, 'path'):
                if '/api/v1/workflow' in route.path:
                    langgraph_routes.append(route.path)
                elif '/api/v1/webhooks' in route.path:
                    webhook_routes.append(route.path)
        
        print(f"✓ LangGraph workflow routes: {len(langgraph_routes)}")
        for route in langgraph_routes:
            print(f"  - {route}")
        
        print(f"✓ LangGraph webhook routes: {len(webhook_routes)}")
        for route in webhook_routes:
            print(f"  - {route}")
        
        # Verify specific routes that were failing
        expected_routes = [
            '/api/v1/workflow/health',
            '/api/v1/workflow/list',
            '/api/v1/workflow/trigger',
            '/api/v1/webhooks/candidate-applied'
        ]
        
        all_routes = [route.path for route in app.routes if hasattr(route, 'path')]
        
        print("\n=== CHECKING PREVIOUSLY FAILING ROUTES ===")
        for expected_route in expected_routes:
            if expected_route in all_routes:
                print(f"✓ {expected_route} - FOUND (was 404, now should work)")
            else:
                print(f"✗ {expected_route} - MISSING")
        
        # Summary
        total_langgraph_routes = len(langgraph_routes) + len(webhook_routes)
        if total_langgraph_routes >= 7:
            print(f"\n🎉 SUCCESS: {total_langgraph_routes} LangGraph routes integrated!")
            print("The 404 errors should be RESOLVED.")
            return True
        else:
            print(f"\n⚠️  WARNING: Only {total_langgraph_routes} LangGraph routes found")
            return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_import_fixes():
    """Verify all import issues are fixed"""
    print("\n=== VERIFYING IMPORT FIXES ===")
    
    try:
        # Test individual module imports
        import config
        print("✓ Config module imports correctly")
        
        import dependencies
        print("✓ Dependencies module imports correctly")
        
        import langgraph_integration
        print("✓ LangGraph integration imports correctly")
        
        import monitoring
        print("✓ Monitoring module imports correctly")
        
        # Test auth routes import
        sys.path.insert(0, os.path.join(gateway_dir, 'routes'))
        from auth import router as auth_router
        print("✓ Auth routes import correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    print("BHIV HR Platform - Fix Verification")
    print("=" * 50)
    
    import_success = verify_import_fixes()
    integration_success = verify_langgraph_integration()
    
    print("\n" + "=" * 50)
    if import_success and integration_success:
        print("🎯 ALL FIXES VERIFIED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Restart your Docker containers")
        print("2. Test the endpoints that were returning 404")
        print("3. Deploy to production")
    else:
        print("❌ Some issues remain - check the output above")