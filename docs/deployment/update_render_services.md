# Render Services Database Update Guide

## New Database Credentials
- **Internal URL**: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
- **External URL**: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a.oregon-postgres.render.com/bhiv_hr_i7zb`

## Step 1: Deploy Schema to New Database

```bash
# Run this command to deploy schema
PGPASSWORD=JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA psql -h dpg-d4kjncvpm1nc738abapg-a.oregon-postgres.render.com -U bhiv_user -d bhiv_hr_i7zb -f "services/db/consolidated_schema.sql"
```

## Step 2: Update Each Render Service

### Service 1: bhiv-hr-gateway-ltg0
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0ag
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

### Service 2: bhiv-hr-agent-nhgg
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0b0
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

### Service 3: bhiv-hr-langgraph
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0c0
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

### Service 4: bhiv-hr-portal-u670
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0d0
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

### Service 5: bhiv-hr-client-portal-3iod
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0e0
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

### Service 6: bhiv-hr-candidate-portal-abe6
1. Go to: https://dashboard.render.com/web/srv-cqvhqhf5r7bs73abt0f0
2. Click "Environment" tab
3. Update `DATABASE_URL` to: `postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a/bhiv_hr_i7zb`
4. Click "Save Changes" → Service will auto-redeploy

## Step 3: Verify All Services

After all services redeploy (5-10 minutes):

1. **Gateway**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
2. **Agent**: https://bhiv-hr-agent-nhgg.onrender.com/docs
3. **LangGraph**: https://bhiv-hr-langgraph.onrender.com/health
4. **HR Portal**: https://bhiv-hr-portal-u670.onrender.com/
5. **Client Portal**: https://bhiv-hr-client-portal-3iod.onrender.com/
6. **Candidate Portal**: https://bhiv-hr-candidate-portal-abe6.onrender.com/

## Step 4: Test Database Connection

```bash
# Test new database
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://bhiv_user:JwvtCqKDYsVgnTiAEtSNAKaDHkksATRA@dpg-d4kjncvpm1nc738abapg-a.oregon-postgres.render.com/bhiv_hr_i7zb')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM jobs')
print(f'Jobs in database: {cursor.fetchone()[0]}')
conn.close()
"
```

## Expected Results
- All 6 services operational within 10 minutes
- Database contains sample data (5 jobs, 3 clients, 3 users)
- All API endpoints functional
- Platform fully restored