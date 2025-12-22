@echo off
echo 1. STOP (keeps database)
docker-compose -f docker-compose.production.yml down
echo.
echo 2. CLEANUP (Safe - keeps database)
echo Cleaning Docker build cache...
docker builder prune --all --force
echo.
echo Cleaning unused containers...
docker container prune -f
echo.
echo Cleaning unused images...
docker image prune -a -f
echo.
echo Checking disk usage...
docker system df
echo.
echo 3. Ready for REBUILD & START
echo Run: docker-compose -f docker-compose.production.yml up -d --build
echo.
echo Docker cleanup complete!
pause
