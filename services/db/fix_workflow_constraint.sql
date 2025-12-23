-- Fix workflows table constraint to include 'completed_with_warnings' status
-- This resolves the constraint violation error in the logs

-- Drop existing constraint
ALTER TABLE workflows DROP CONSTRAINT IF EXISTS workflows_status_check;

-- Add updated constraint with missing status
ALTER TABLE workflows ADD CONSTRAINT workflows_status_check 
CHECK (status IN ('running', 'completed', 'failed', 'cancelled', 'completed_with_warnings'));

-- Verify constraint
SELECT conname, consrc FROM pg_constraint WHERE conname = 'workflows_status_check';