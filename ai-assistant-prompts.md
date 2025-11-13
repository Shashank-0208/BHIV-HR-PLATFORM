# VS Code AI Assistant Prompts - Complete Implementation Guide

## CRITICAL PROMPT TEMPLATE FOR YOUR AI ASSISTANT

Use these prompts **sequentially** in your VS Code AI Assistant (GitHub Copilot or similar). Each prompt represents one complete implementation task.

---

## Prompt 1: Project Structure & Setup
```
Create a new microservice directory structure for BHIV HR Platform:

Create: services/langgraph_orchestrator/
With subdirectories: tests/

Create these files in the service root:
- __init__.py
- app.py (FastAPI application)
- state.py (Pydantic state schemas)
- agents.py (LangChain agents)
- graphs.py (LangGraph workflow)
- tools.py (Tool definitions)
- communication.py (Multi-channel notifications)
- config.py (Settings/config management)
- requirements.txt (Python dependencies)
- Dockerfile (Container configuration)
- README.md
- .env.example (Environment template)

And in tests/:
- __init__.py
- test_workflows.py
- test_agents.py
- test_integration.py

Output the complete directory tree.
```

---

## Prompt 2: Install Core Dependencies
```
Create requirements.txt for BHIV HR LangGraph service with:

Core packages:
- langgraph (>=0.1.2)
- langchain, langchain-openai, langchain-core
- fastapi, uvicorn

API clients:
- httpx (async HTTP)
- twilio (WhatsApp)
- python-telegram-bot
- email/smtp for Gmail

AI/ML:
- openai
- transformers
- torch

Database:
- psycopg2-binary (PostgreSQL)
- sqlalchemy

Testing:
- pytest, pytest-asyncio, pytest-cov

Utilities:
- pydantic, pydantic-settings
- python-dotenv

List all packages with exact versions for Python 3.12.7
```

---

## Prompt 3: Create Configuration Module
```
Create config.py that:

1. Uses pydantic BaseSettings to load from .env
2. Defines these configuration sections:

API Configuration:
- gateway_url: str
- api_key: str
- langgraph_port: int

Database:
- database_url: str (PostgreSQL connection string)

OpenAI:
- openai_api_key: str
- openai_model: str

Communication channels:
- twilio_account_sid, twilio_auth_token, twilio_whatsapp_number
- gmail_email, gmail_app_password
- telegram_bot_token, telegram_bot_username

Environment:
- environment: str (development/production)
- log_level: str

3. Include @lru_cache get_settings() function
4. Add credential validation for production environment
5. Initialize logging at module level

Make all settings configurable via environment variables with proper defaults.
```

---

## Prompt 4: Create State Schemas
```
Create state.py with Pydantic TypedDict schemas:

1. CandidateApplicationState with fields:
   - Identifiers: candidate_id, job_id, application_id
   - Candidate data: email, phone, name
   - Job data: title, description
   - Status: application_status (Literal with: pending, shortlisted, rejected, interview_scheduled, offered, onboarded)
   - Messages: Annotated[Sequence[BaseMessage], operator.add] for LLM conversation history
   - Tracking: notifications_sent (list), matching_score, ai_recommendation
   - Sentiment: positive/neutral/negative
   - Workflow: next_action, workflow_stage (screening/notification/hr_update/feedback/completed)
   - Error handling: error message field
   - Timestamps and optional voice paths

2. NotificationPayload TypedDict for notification data structure

Use proper type hints. Import from langchain_core.messages and typing module.
```

---

## Prompt 5: Create Communication Manager
```
Create communication.py with CommunicationManager class that:

1. Initializes THREE communication channels:
   - Twilio client for WhatsApp
   - Telegram bot using python-telegram-bot
   - Gmail SMTP for email

2. Implements async methods:
   - send_whatsapp(phone, message): Send via Twilio WhatsApp sandbox
   - send_email(email, subject, body, html_body): Send via Gmail SMTP SSL
   - send_telegram(chat_id, message): Send via Telegram bot
   - send_multi_channel(payload, channels): Send across multiple channels

3. Each method:
   - Should handle errors gracefully
   - Return status dict with success/failure info
   - Log using Python logging

4. Create singleton instance: comm_manager = CommunicationManager()

5. Format messages properly:
   - WhatsApp: Shorter, formatted for mobile
   - Email: Structured with subject and body
   - Telegram: Markdown formatted

Include proper credential handling from config.
```

---

## Prompt 6: Create LangGraph Tools
```
Create tools.py with @tool decorated async functions:

Required tools:

1. get_candidate_profile(candidate_id: int) -> dict
   - GET to gateway_url/v1/candidates/{id}
   - Include Bearer token auth

2. get_job_details(job_id: int) -> dict
   - GET to gateway_url/v1/jobs/{id}

3. update_application_status(application_id, status, notes) -> dict
   - PUT to gateway_url/v1/applications/{id}

4. get_ai_matching_score(candidate_id, job_id) -> dict
   - POST to gateway_url/v1/match with JSON body

5. send_multi_channel_notification(...) -> dict
   - Call communication manager's send_multi_channel
   - Return notification results

6. log_audit_event(event_type, details) -> dict
   - POST to gateway_url/v1/audit-logs

7. update_hr_dashboard(application_id, update_data) -> dict
   - POST to gateway_url/v1/dashboard/refresh

All tools:
- Use httpx AsyncClient for async HTTP
- Include proper error handling and logging
- Set HTTPX_TIMEOUT = 30.0 for API calls
- Return dict with status and data

Docstrings should be clear about function purpose.
```

---

## Prompt 7: Create Agent Nodes
```
Create agents.py with 4 async agent functions:

1. application_screener_agent(state) -> dict:
   - Call get_ai_matching_score tool
   - Use ChatOpenAI LLM with system prompt for decision making
   - Decision logic: score >= 75 -> shortlist, 50-74 -> review, < 50 -> reject
   - Return updated state with status and recommendation

2. notification_agent(state) -> dict:
   - Check application_status
   - Prepare messages for shortlisted/rejected status
   - Call send_multi_channel_notification with email + whatsapp
   - Return state with notification records

3. hr_update_agent(state) -> dict:
   - Update application status in database
   - Update HR dashboard via update_hr_dashboard tool
   - Return state with workflow progress

4. feedback_collection_agent(state) -> dict:
   - Collect feedback data from state
   - Log audit event with final outcome
   - Return state with completion status

All agents:
- Accept CandidateApplicationState parameter
- Return dict with state updates
- Include comprehensive logging with emojis
- Have proper error handling with try/except

Initialize ChatOpenAI LLM at module level with settings.
```

---

## Prompt 8: Create LangGraph Workflow
```
Create graphs.py with workflow creation:

1. Define should_send_notification(state) conditional edge function:
   - Returns "notify" if status in [shortlisted, rejected]
   - Returns "skip_notify" otherwise

2. Create create_application_workflow() function that:
   - Initializes StateGraph with CandidateApplicationState
   - Adds nodes: screen_application, send_notifications, update_hr_dashboard, collect_feedback
   - Sets entry point: screen_application
   - Adds conditional edges from screen_application using should_send_notification
   - Routes to send_notifications if notify, else to update_hr_dashboard
   - Adds edges: send_notifications -> update_hr_dashboard -> collect_feedback -> END
   - Setup PostgreSQL checkpointer from database_url
   - Compile graph with checkpointer
   - Return compiled graph

Include proper logging at each step.
Import all agents and StateGraph from langgraph.
```

---

## Prompt 9: Create FastAPI Service
```
Create app.py with FastAPI service:

1. Initialize FastAPI app with title, version, description
2. Load workflow from graphs.py
3. Create ConnectionManager class for WebSocket management
4. Create Pydantic models:
   - ApplicationRequest (with candidate_id, job_id, etc.)
   - WorkflowResponse (workflow_id, status, message, timestamp)
   - WorkflowStatus (detailed status info)

5. Implement endpoints:
   - GET /health -> health check
   - POST /workflows/application/start -> start workflow in background
   - GET /workflows/{workflow_id}/status -> get workflow status
   - POST /workflows/{workflow_id}/resume -> resume paused workflow
   - WebSocket /ws/{workflow_id} -> real-time updates
   - GET /workflows -> list workflows

6. Background task _execute_workflow:
   - Invoke workflow asynchronously
   - Broadcast completion via WebSocket
   - Handle errors and broadcast error messages

All endpoints should:
- Include proper error handling with HTTPException
- Have comprehensive logging
- Return appropriate status codes and messages
- Support async operations
```

---

## Prompt 10: Create Dockerfile & Docker Compose
```
Create Dockerfile for langgraph service:

1. Base image: python:3.12.7-slim
2. Working directory: /app
3. Install system deps: gcc, postgresql-client
4. Copy and install requirements.txt
5. Copy entire application
6. Expose port 9001
7. Add health check using curl to /health endpoint
8. CMD: uvicorn app:app --host 0.0.0.0 --port 9001

Then update deployment/docker/docker-compose.production.yml:
- Add langgraph-orchestrator service
- Build context: services/langgraph_orchestrator
- Port mapping: 9001:9001
- Environment: GATEWAY_URL, API_KEY, DATABASE_URL, OPENAI_API_KEY, TWILIO credentials, GMAIL, TELEGRAM
- Depends on: db, gateway
- Network: bhiv-network
- Health check enabled
- Restart policy: unless-stopped
```

---

## Prompt 11: Create Test Files
```
Create tests/test_workflows.py:

1. Import fixtures for workflow and sample_state
2. Create sample_state fixture returning valid CandidateApplicationState dict
3. Create workflow fixture returning create_application_workflow() output

4. Test functions (mark with @pytest.mark.asyncio):
   - test_workflow_initialization: Check workflow is not None and has ainvoke
   - test_workflow_state_structure: Verify state has required fields
   - test_state_transitions: Test conditional edge logic
   - test_notification_routing: Test should_send_notification

Include proper logging and assertions.
Use pytest for testing framework.
```

---

## Prompt 12: Create Environment Template
```
Create .env.example with all required environment variables:

[API Configuration]
GATEWAY_URL=
API_KEY=
LANGGRAPH_PORT=9001

[Database]
DATABASE_URL=

[OpenAI]
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4-turbo-preview

[Twilio]
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=

[Gmail]
GMAIL_EMAIL=
GMAIL_APP_PASSWORD=

[Telegram]
TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_USERNAME=

[Environment]
ENVIRONMENT=development
LOG_LEVEL=INFO

With comments explaining each variable and what it's used for.
```

---

## Sequential Execution Order

1. **Prompt 1**: Create directory structure
2. **Prompt 2**: Create requirements.txt
3. **Prompt 3**: Create config.py
4. **Prompt 4**: Create state.py
5. **Prompt 5**: Create communication.py
6. **Prompt 6**: Create tools.py
7. **Prompt 7**: Create agents.py
8. **Prompt 8**: Create graphs.py
9. **Prompt 9**: Create app.py
10. **Prompt 10**: Create Dockerfile & update docker-compose.yml
11. **Prompt 11**: Create test files
12. **Prompt 12**: Create .env.example

---

## After Implementation: Local Testing

```bash
# Terminal Commands (not AI prompts)

# 1. Navigate to service
cd services/langgraph_orchestrator

# 2. Create .env and configure
cp .env.example .env
# Edit .env with your credentials

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test imports
python -c "from app import app; print('✅ App loads successfully')"

# 5. Start service
uvicorn app:app --reload --port 9001

# 6. In another terminal, test health endpoint
curl http://localhost:9001/health

# 7. Test workflow start
curl -X POST http://localhost:9001/workflows/application/start \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 1, "job_id": 1, "application_id": 1, "candidate_email": "test@test.com", "candidate_phone": "+919876543210", "candidate_name": "Test User", "job_title": "Engineer"}'
```

---

## Final Deployment

```bash
# Docker Compose (from project root)
docker-compose -f deployment/docker/docker-compose.production.yml up -d langgraph-orchestrator

# Verify
docker-compose -f deployment/docker/docker-compose.production.yml logs langgraph-orchestrator
```

---

## Important Notes

1. **Your Credentials**: Are securely referenced from environment variables, NEVER hardcoded
2. **Error Handling**: All functions include try/except and proper logging
3. **Async/Await**: All I/O operations are properly async
4. **State Management**: LangGraph handles state persistence with PostgreSQL checkpointer
5. **Multi-Channel**: Notifications can fail on one channel and succeed on others - this is handled
6. **Production Ready**: Includes health checks, error handling, logging, and WebSocket support

---

## Implementation Timeline

- **Days 1-2**: Prompts 1-5 (Setup, Config, Communication)
- **Days 2-3**: Prompts 6-8 (Tools, Agents, Workflow)
- **Day 4**: Prompts 9-10 (FastAPI, Docker)
- **Day 5**: Prompt 11-12 (Testing, Environment)
- **Days 6-7**: Local testing, debugging, deployment to Render

**Total: 7 days, ready for production**
