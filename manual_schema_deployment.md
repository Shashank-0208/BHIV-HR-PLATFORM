# Manual Schema Deployment Instructions

## Database Schema Fix (Execute in Render PostgreSQL Console)

1. Go to Render Dashboard → PostgreSQL service → Connect
2. Execute these SQL commands:

```sql
-- Add missing columns to clients table
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;

-- Update existing records
UPDATE clients 
SET failed_login_attempts = 0 
WHERE failed_login_attempts IS NULL;

-- Create job_applications table
CREATE TABLE IF NOT EXISTS job_applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    cover_letter TEXT,
    status VARCHAR(50) DEFAULT 'applied',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(candidate_id, job_id)
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_job_applications_candidate ON job_applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_job ON job_applications(job_id);

-- Update schema version
INSERT INTO schema_version (version, description) VALUES 
('4.2.0', 'Production schema with job_applications table and client auth fixes')
ON CONFLICT (version) DO UPDATE SET applied_at = CURRENT_TIMESTAMP;
```

## Gateway Service Redeploy

1. Go to Render Dashboard → bhiv-hr-gateway service
2. Click "Manual Deploy" → "Deploy latest commit"
3. Wait for deployment to complete

## Verification Commands

After deployment, test these endpoints:

```bash
# Test client login (should work now)
curl -X POST -H "Content-Type: application/json" \
-d '{"client_id":"TECH001","password":"demo123"}' \
https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login

# Test AI matching (should use Phase 3 now)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top
```

Expected results:
- Client login: Should return success with JWT token
- AI matching: Should show "agent_status": "connected" and Phase 3 algorithm