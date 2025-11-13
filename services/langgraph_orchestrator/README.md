# BHIV LangGraph Orchestrator

AI-driven workflow orchestration service for the BHIV HR Platform using LangGraph.

## Features

- **Multi-Agent Workflow**: 4 specialized agents for candidate application processing
- **Multi-Channel Notifications**: Email, WhatsApp, Telegram integration
- **AI-Powered Screening**: OpenAI GPT-4 for intelligent candidate evaluation
- **Real-time Updates**: WebSocket support for live workflow status
- **State Persistence**: PostgreSQL checkpointing for workflow state

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start service
uvicorn app:app --port 9001

# Test health endpoint
curl http://localhost:9001/health
```

## API Endpoints

- `GET /health` - Health check
- `POST /workflows/application/start` - Start workflow
- `GET /workflows/{id}/status` - Get workflow status
- `WebSocket /ws/{id}` - Real-time updates

## Integration

This service integrates with the BHIV HR Platform Gateway to provide automated candidate application processing with AI-driven decision making and multi-channel notifications.