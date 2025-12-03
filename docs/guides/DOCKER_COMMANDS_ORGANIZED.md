# ========================================
# BHIV HR PLATFORM - DOCKER COMMANDS
# ========================================

# 1. CLEANUP (Safe - keeps database)
docker builder prune --all --force          # Remove build cache
docker container prune -f                   # Remove stopped containers
docker image prune -a -f                    # Remove unused images
docker system df                            # Check disk usage

# 2. BUILD
docker-compose -f docker-compose.production.yml build

# 3. RUN
docker-compose -f docker-compose.production.yml up -d

# 4. STOP (keeps database)
docker-compose -f docker-compose.production.yml down

# ========================================
# ADVANCED COMMANDS
# ========================================

# REBUILD & START
docker-compose -f docker-compose.production.yml up -d --build

# FRESH BUILD (no cache)
docker-compose -f docker-compose.production.yml build --no-cache

# WITH EXPLICIT ENV FILE
docker-compose -f docker-compose.production.yml --env-file .env up -d

# ========================================
# MONITORING
# ========================================

# CHECK STATUS
docker ps

# VIEW LOGS
docker-compose -f docker-compose.production.yml logs

# FOLLOW LOGS
docker-compose -f docker-compose.production.yml logs -f

# SERVICE-SPECIFIC LOGS
docker-compose -f docker-compose.production.yml logs gateway
docker-compose -f docker-compose.production.yml logs portal

# ========================================
# DATABASE MANAGEMENT
# ========================================

# RESET DATABASE (removes all data)
docker volume rm bhiv-hr-platform_postgres_data

# BACKUP DATABASE
docker exec bhiv-hr-platform-db-1 pg_dump -U bhiv_user bhiv_hr > backup.sql

# ========================================
# TROUBLESHOOTING
# ========================================

# FULL CLEANUP (removes everything)
docker-compose -f docker-compose.production.yml down -v
docker system prune -a -f --volumes

# RESTART SINGLE SERVICE
docker-compose -f docker-compose.production.yml restart gateway

# EXEC INTO CONTAINER
docker exec -it bhiv-hr-platform-gateway-1 bash

# ========================================
# TESTING & VALIDATION
# ========================================

# TEST API ENDPOINTS
curl http://localhost:8000/health
curl http://localhost:8000/docs

# TEST PORTALS
curl http://localhost:8501/_stcore/health
curl http://localhost:8502/_stcore/health
curl http://localhost:8503/_stcore/health

# RUN PYTHON TESTS
python tests/run_all_tests.py
python validation/final_verification.py

# ========================================
# DEVELOPMENT WORKFLOW
# ========================================

# QUICK START (Fresh)
docker-compose -f docker-compose.production.yml down -v
docker builder prune -f
docker-compose -f docker-compose.production.yml up -d --build

# DAILY DEVELOPMENT
docker-compose -f docker-compose.production.yml restart
docker-compose -f docker-compose.production.yml logs -f

# UPDATE SINGLE SERVICE
docker-compose -f docker-compose.production.yml build gateway
docker-compose -f docker-compose.production.yml up -d gateway

# ========================================
# ENVIRONMENT MANAGEMENT
# ========================================

# CHECK ENV VARIABLES
docker-compose -f docker-compose.production.yml config

# VALIDATE ENV FILE
cat .env | grep -v "^#" | grep -v "^$"

# ========================================
# PERFORMANCE & RESOURCES
# ========================================

# MONITOR RESOURCES
docker stats

# CHECK DISK USAGE
docker system df -v

# MEMORY USAGE BY SERVICE
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# ========================================
# NETWORK & CONNECTIVITY
# ========================================

# LIST NETWORKS
docker network ls

# INSPECT NETWORK
docker network inspect bhiv-hr-platform_default

# TEST INTERNAL CONNECTIVITY
docker exec bhiv-hr-platform-gateway-1 curl http://db:5432
docker exec bhiv-hr-platform-portal-1 curl http://gateway:8000/health