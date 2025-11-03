@echo off
echo Deploying BHIV HR Platform Schema v4.2.0 to Render Production...

echo.
echo Step 1: Connect to Render PostgreSQL and execute schema update
echo Database: postgresql://bhiv_user:8oaleQyxSfBJp7uqt0UJoAXnOhPj63nG@dpg-d40c0kf5r7bs73abt080-a.oregon-postgres.render.com/bhiv_hr_jcuu_w5fl

echo.
echo Execute this command to deploy schema:
echo psql "postgresql://bhiv_user:8oaleQyxSfBJp7uqt0UJoAXnOhPj63nG@dpg-d40c0kf5r7bs73abt080-a.oregon-postgres.render.com/bhiv_hr_jcuu_w5fl" -f deploy_schema_production.sql

echo.
echo Step 2: Redeploy Gateway service on Render to pick up URL fix
echo - Go to Render Dashboard
echo - Select bhiv-hr-gateway service  
echo - Click "Manual Deploy" -> "Deploy latest commit"

echo.
echo Step 3: Test the fixes
echo curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top
echo curl -X POST -H "Content-Type: application/json" -d "{\"client_id\":\"TECH001\",\"password\":\"demo123\"}" https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login

pause