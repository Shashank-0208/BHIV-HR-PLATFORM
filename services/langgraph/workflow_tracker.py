"""
Simple workflow tracker using existing PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class WorkflowTracker:
    def __init__(self):
        self.engine = self._get_db_engine()
        self._ensure_table_exists()
    
    def _get_db_engine(self):
        database_url = os.getenv("DATABASE_URL")
        return create_engine(database_url, pool_pre_ping=True)
    
    def _ensure_table_exists(self):
        """Create workflow_status table if it doesn't exist"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS workflow_status (
                        workflow_id VARCHAR(255) PRIMARY KEY,
                        status VARCHAR(50) NOT NULL,
                        current_stage VARCHAR(100),
                        application_status VARCHAR(50),
                        matching_score FLOAT DEFAULT 0.0,
                        last_action VARCHAR(200),
                        completed BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to create workflow_status table: {e}")
    
    def create_workflow(self, workflow_id: str, initial_status: str = "started"):
        """Record new workflow creation"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO workflow_status 
                    (workflow_id, status, current_stage, application_status, last_action)
                    VALUES (:workflow_id, :status, 'screening', 'pending', 'workflow_created')
                    ON CONFLICT (workflow_id) DO UPDATE SET
                    status = :status, updated_at = CURRENT_TIMESTAMP
                """), {
                    "workflow_id": workflow_id,
                    "status": initial_status
                })
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to create workflow record: {e}")
    
    def update_workflow(self, workflow_id: str, **updates):
        """Update workflow status"""
        try:
            set_clauses = []
            params = {"workflow_id": workflow_id}
            
            for key, value in updates.items():
                if key in ["status", "current_stage", "application_status", "matching_score", "last_action", "completed"]:
                    set_clauses.append(f"{key} = :{key}")
                    params[key] = value
            
            if set_clauses:
                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                query = f"UPDATE workflow_status SET {', '.join(set_clauses)} WHERE workflow_id = :workflow_id"
                
                with self.engine.connect() as conn:
                    conn.execute(text(query), params)
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to update workflow: {e}")
    
    def get_workflow_status(self, workflow_id: str):
        """Get workflow status from database"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT workflow_id, status, current_stage, application_status, 
                           matching_score, last_action, completed, updated_at
                    FROM workflow_status WHERE workflow_id = :workflow_id
                """), {"workflow_id": workflow_id})
                
                row = result.fetchone()
                if row:
                    return {
                        "workflow_id": row[0],
                        "status": row[1],
                        "current_stage": row[2] or "screening",
                        "application_status": row[3] or "pending",
                        "matching_score": float(row[4]) if row[4] else 0.0,
                        "last_action": row[5] or "created",
                        "completed": bool(row[6]),
                        "updated_at": row[7].isoformat() if row[7] else None
                    }
                return None
        except Exception as e:
            logger.error(f"Failed to get workflow status: {e}")
            return None
    
    def list_workflows(self, limit: int = 50):
        """List recent workflows"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT workflow_id, status, current_stage, application_status, created_at
                    FROM workflow_status 
                    ORDER BY created_at DESC 
                    LIMIT :limit
                """), {"limit": limit})
                
                workflows = []
                for row in result:
                    workflows.append({
                        "workflow_id": row[0],
                        "status": row[1],
                        "current_stage": row[2],
                        "application_status": row[3],
                        "created_at": row[4].isoformat() if row[4] else None
                    })
                return workflows
        except Exception as e:
            logger.error(f"Failed to list workflows: {e}")
            return []

# Global tracker instance
tracker = WorkflowTracker()