-- BHIV HR Platform - Production Schema Deployment v4.2.0
-- Fix missing columns and tables for production deployment

-- Add missing columns to clients table
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;

-- Update existing records
UPDATE clients 
SET failed_login_attempts = 0 
WHERE failed_login_attempts IS NULL;

-- Create job_applications table if not exists
CREATE TABLE IF NOT EXISTS job_applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    cover_letter TEXT,
    status VARCHAR(50) DEFAULT 'applied' CHECK (status IN ('applied', 'reviewed', 'shortlisted', 'rejected', 'withdrawn')),
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(candidate_id, job_id)
);

-- Add indexes for job_applications
CREATE INDEX IF NOT EXISTS idx_job_applications_candidate ON job_applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_job ON job_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status);
CREATE INDEX IF NOT EXISTS idx_job_applications_date ON job_applications(applied_date);

-- Add update trigger for job_applications
CREATE TRIGGER update_job_applications_updated_at 
BEFORE UPDATE ON job_applications 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update schema version
INSERT INTO schema_version (version, description) VALUES 
('4.2.0', 'Production schema with job_applications table and client auth fixes')
ON CONFLICT (version) DO UPDATE SET applied_at = CURRENT_TIMESTAMP;

-- Verify deployment
SELECT 'Schema v4.2.0 deployed successfully' as status,
       COUNT(*) as total_tables
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Show critical tables status
SELECT table_name, 
       CASE WHEN table_name IN ('clients', 'job_applications') THEN 'CRITICAL' ELSE 'OK' END as priority
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('clients', 'candidates', 'jobs', 'job_applications', 'feedback')
ORDER BY table_name;