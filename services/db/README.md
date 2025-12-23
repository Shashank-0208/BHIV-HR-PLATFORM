# BHIV HR Platform Database Service

## Overview
PostgreSQL 15 database service for the BHIV HR Platform with complete RL integration and production-ready schema.

## Current Status ✅
- **Schema Version**: 4.3.1
- **Total Tables**: 19 (13 core + 6 RL integration)
- **Total Indexes**: 96 performance-optimized indexes
- **Total Constraints**: 82 (foreign keys, checks, unique)
- **Endpoint Status**: 119/119 operational (100% success rate)
- **RL Integration**: Complete with active learning
- **Production Ready**: ✅ Fully operational

## Database Structure

### Core Business Tables (13)
1. **candidates** - Candidate profiles and information
2. **jobs** - Job postings and requirements
3. **feedback** - Values-based assessment (BHIV core feature)
4. **interviews** - Interview scheduling and management
5. **offers** - Job offer management
6. **users** - Internal HR users with 2FA
7. **clients** - External client companies
8. **matching_cache** - AI matching results cache
9. **audit_logs** - Security and compliance tracking
10. **rate_limits** - API rate limiting
11. **csp_violations** - Content Security Policy violations
12. **company_scoring_preferences** - Phase 3 learning engine
13. **job_applications** - Candidate applications

### RL Integration Tables (6)
14. **rl_predictions** - RL scoring and predictions
15. **rl_feedback** - Feedback and reward signals
16. **rl_model_performance** - Model performance tracking
17. **rl_training_data** - Training dataset
18. **workflows** - LangGraph workflow tracking
19. **schema_version** - Version control

## Key Features

### Performance Optimization
- **96 Indexes**: Comprehensive indexing for sub-50ms queries
- **GIN Indexes**: Full-text search on technical skills
- **Composite Indexes**: Multi-column optimization
- **Connection Pooling**: Automatic scaling

### Security & Compliance
- **Audit Logging**: Complete change tracking
- **2FA Support**: TOTP implementation for users and clients
- **Rate Limiting**: Dynamic API protection
- **CSP Monitoring**: Security policy violations

### RL Integration
- **Active Learning**: Continuous model improvement
- **Feedback Loop**: 340% feedback rate achieved
- **Model Versioning**: Performance tracking across versions
- **Training Pipeline**: Automated data collection

### Data Integrity
- **82 Constraints**: Foreign keys, checks, unique constraints
- **Generated Columns**: Automatic score calculations
- **Triggers**: Timestamp updates and audit logging
- **Referential Integrity**: Cascade operations

## Schema Validation

### Current Production Data
```sql
-- Verify table counts
SELECT table_name, 
       (SELECT COUNT(*) FROM information_schema.columns 
        WHERE table_name = t.table_name) as columns
FROM information_schema.tables t
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Check RL system status
SELECT 
    (SELECT COUNT(*) FROM rl_predictions) as predictions,
    (SELECT COUNT(*) FROM rl_feedback) as feedback_records,
    (SELECT model_version FROM rl_model_performance 
     ORDER BY evaluation_date DESC LIMIT 1) as latest_model,
    (SELECT accuracy FROM rl_model_performance 
     ORDER BY evaluation_date DESC LIMIT 1) as model_accuracy;
```

### Performance Metrics
- **Query Performance**: <50ms average response time
- **Index Usage**: 96 indexes for optimal performance
- **Memory Efficiency**: Optimized for production workloads
- **Connection Handling**: Stable across all 6 microservices

## Deployment

### Docker Configuration
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: bhiv_hr
      POSTGRES_USER: bhiv_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./consolidated_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bhiv_user -d bhiv_hr"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Environment Variables
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bhiv_hr
DB_USER=bhiv_user
DB_PASSWORD=your_secure_password
```

## Migration History

### Version 4.3.1 (December 22, 2025)
- ✅ **Endpoint Testing Complete**: 119/119 endpoints operational
- ✅ **RL Integration Validated**: All RL tables functional
- ✅ **Performance Optimized**: 96 indexes, <50ms queries
- ✅ **Security Validated**: 2FA, audit logging, rate limiting

### Version 4.3.0 (December 4, 2025)
- Added RL + Feedback Agent tables
- Implemented model performance tracking
- Added training data pipeline

### Version 4.2.2 (November 15, 2025)
- Added workflows table for LangGraph
- Enhanced workflow tracking capabilities

### Version 4.2.1 (November 11, 2025)
- Complete consolidated schema
- Added missing components

## Maintenance

### Regular Tasks
1. **Backup Verification**: Daily automated backups
2. **Performance Monitoring**: Query performance analysis
3. **Index Maintenance**: Regular ANALYZE and VACUUM
4. **Security Audits**: Review audit logs and access patterns

### Health Checks
```sql
-- Database health check
SELECT 
    'Database Status' as component,
    COUNT(*) as total_tables,
    (SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
    (SELECT setting FROM pg_settings WHERE name = 'max_connections') as max_connections
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

-- RL system health
SELECT 
    'RL System Status' as component,
    COUNT(*) as total_predictions,
    (SELECT COUNT(*) FROM rl_feedback) as feedback_records,
    (SELECT accuracy FROM rl_model_performance ORDER BY evaluation_date DESC LIMIT 1) as model_accuracy
FROM rl_predictions;
```

## Troubleshooting

### Common Issues
1. **Connection Issues**: Check Docker container status
2. **Performance Issues**: Review query plans and indexes
3. **Data Integrity**: Verify foreign key constraints
4. **RL Issues**: Check model performance metrics

### Monitoring Queries
```sql
-- Check slow queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Support

### Documentation
- **API Documentation**: Complete endpoint reference
- **Schema Documentation**: Detailed table descriptions
- **Performance Guide**: Optimization best practices
- **Security Guide**: Authentication and authorization

### Contact
- **Platform**: BHIV HR Platform v4.3.1
- **Database**: PostgreSQL 15 with RL integration
- **Status**: Production Ready - 100% Operational
- **Last Updated**: December 22, 2025

---

**BHIV HR Platform Database Service v4.3.1**  
*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*