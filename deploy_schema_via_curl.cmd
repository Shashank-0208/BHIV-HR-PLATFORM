@echo off
echo Deploying schema via SQL commands through curl...

echo Adding missing columns to clients table...
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/execute" ^
-H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" ^
-H "Content-Type: application/json" ^
-d "{\"sql\": \"ALTER TABLE clients ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0, ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;\"}"

echo.
echo Creating job_applications table...
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/execute" ^
-H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" ^
-H "Content-Type: application/json" ^
-d "{\"sql\": \"CREATE TABLE IF NOT EXISTS job_applications (id SERIAL PRIMARY KEY, candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE, job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE, cover_letter TEXT, status VARCHAR(50) DEFAULT 'applied', applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(candidate_id, job_id));\"}"

echo.
echo Schema deployment complete. Gateway service will auto-redeploy with URL fix.
pause