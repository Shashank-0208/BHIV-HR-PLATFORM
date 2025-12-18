# Database Service

**PostgreSQL 17**  
**Schema Version**: v4.3.1  
**Tables**: 19 total (13 core + 6 RL integration)  
**Status**: ✅ Operational with RL Integration  
**Production Data**: 35 candidates, 29 jobs, 5 RL predictions, 17 RL feedback records  

## Overview

PostgreSQL database with comprehensive schema for HR platform operations.

## Schema Structure

### Core Application Tables (13)
- **candidates**: Candidate profiles with authentication (35 production records)
- **jobs**: Job postings from clients and HR (29 production records)
- **feedback**: Values assessment (5-point BHIV values)
- **interviews**: Interview scheduling and management
- **offers**: Job offer management
- **users**: Internal HR users with 2FA support
- **clients**: External client companies with JWT auth
- **job_applications**: Application tracking system
- **audit_logs**: Security and compliance tracking
- **rate_limits**: API rate limiting by IP and endpoint
- **csp_violations**: Content Security Policy monitoring
- **matching_cache**: AI matching results cache
- **company_scoring_preferences**: Phase 3 learning engine

### RL Integration Tables (6)
- **rl_predictions**: ML model predictions (5 production records)
- **rl_feedback**: Learning feedback system (17 production records, 340% feedback rate)
- **rl_model_performance**: Model metrics (v1.0.1 with 80% accuracy)
- **rl_states**: State management for RL system
- **rl_actions**: Action space definitions
- **rl_rewards**: Reward system tracking

### System Tables (Enhanced)
- **schema_version**: Version tracking (v4.3.1 with RL integration)
- **pg_stat_statements**: Performance monitoring
- **pg_stat_statements_info**: Statistics metadata

## Key Features

- **Constraints**: CHECK constraints for data validation
- **Indexes**: 85+ performance indexes including GIN for full-text search and RL optimization
- **Triggers**: Auto-update timestamps and audit logging
- **Functions**: PostgreSQL functions for complex operations
- **Generated Columns**: Automatic average score calculation

## Local Development

```bash
# Using Docker
docker run -d --name bhiv-db \
  -e POSTGRES_DB=bhiv_hr \
  -e POSTGRES_USER=bhiv_user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:17-alpine

# Initialize schema with RL integration
psql postgresql://bhiv_user:password@localhost:5432/bhiv_hr -f consolidated_schema.sql

# Verify RL integration
psql postgresql://bhiv_user:password@localhost:5432/bhiv_hr -c "SELECT COUNT(*) FROM rl_predictions; SELECT COUNT(*) FROM rl_feedback;"
```
