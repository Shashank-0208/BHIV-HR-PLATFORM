# 🗄️ BHIV HR Platform - Database Documentation

**PostgreSQL 17 Database Schema v4.2.0**  
**Updated**: November 15, 2025  
**Status**: ✅ Production Ready  
**Tables**: 13 core tables (8 application + 5 security/performance)

---

## 📊 Database Overview

### **Database Architecture**
- **Engine**: PostgreSQL 17
- **Schema Version**: v4.2.0
- **Total Tables**: 13 core tables + system tables
- **Indexes**: 75+ performance indexes
- **Triggers**: 15+ automated triggers
- **Functions**: 2 PostgreSQL functions

### **Production Statistics**
- **Real Data**: 10+ candidates, 6+ jobs, 3+ clients
- **Performance**: <50ms query response time
- **Uptime**: 99.9% availability
- **Backup**: Automated daily backups
- **Security**: Encrypted connections, audit logging

---

## 🏗️ Core Tables Structure

### **1. Application Tables (8 Tables)**

#### **candidates** - Candidate Profiles
```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    location VARCHAR(255),
    experience_years INTEGER DEFAULT 0,
    technical_skills TEXT,
    seniority_level VARCHAR(100),
    education_level VARCHAR(100),
    resume_path VARCHAR(500),
    password_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'applied',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **Unique Constraints**: Email uniqueness
- **Indexes**: GIN index on technical_skills for full-text search
- **Security**: bcrypt password hashing
- **Validation**: CHECK constraints on experience_years >= 0

#### **jobs** - Job Postings
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    location VARCHAR(255),
    experience_level VARCHAR(100),
    requirements TEXT,
    description TEXT,
    client_id INTEGER REFERENCES clients(client_id),
    employment_type VARCHAR(50) DEFAULT 'Full-time',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **Foreign Keys**: References clients table
- **Indexes**: Composite indexes on status, department, location
- **Validation**: Status enum constraints

#### **feedback** - Values Assessment
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
    average_score DECIMAL(3,2) GENERATED ALWAYS AS 
        ((integrity + honesty + discipline + hard_work + gratitude) / 5.0) STORED,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **Generated Columns**: Automatic average score calculation
- **CHECK Constraints**: 1-5 scale validation for all values
- **Foreign Keys**: References candidates and jobs
- **BHIV Values**: Integrity, Honesty, Discipline, Hard Work, Gratitude

#### **interviews** - Interview Management
```sql
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    interview_date TIMESTAMP,
    interviewer VARCHAR(255),
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **offers** - Job Offers
```sql
CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    salary DECIMAL(12,2),
    start_date DATE,
    terms TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **users** - HR Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'hr_user',
    totp_secret VARCHAR(32),
    is_2fa_enabled BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **2FA Support**: TOTP secret storage
- **Security**: Account locking after failed attempts
- **Role Management**: HR user roles

#### **clients** - Client Companies
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **Unique Constraints**: client_id and email uniqueness
- **Security**: Account locking mechanism
- **JWT Integration**: For client portal authentication

#### **job_applications** - Application Tracking
```sql
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    cover_letter TEXT,
    status VARCHAR(50) DEFAULT 'applied',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(candidate_id, job_id)
);
```

**Features**:
- **Unique Constraints**: Prevent duplicate applications
- **Status Tracking**: Application status management

### **2. Security & Performance Tables (5 Tables)**

#### **audit_logs** - Security Tracking
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- **JSONB Storage**: Flexible audit data storage
- **IP Tracking**: Security monitoring
- **Automated Triggers**: Automatic audit logging

#### **rate_limits** - API Rate Limiting
```sql
CREATE TABLE rate_limits (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ip_address, endpoint)
);
```

**Features**:
- **Dynamic Limiting**: CPU-based rate adjustment
- **Endpoint Specific**: Granular rate limiting
- **IP Tracking**: Per-IP rate limiting

#### **csp_violations** - Security Policy Monitoring
```sql
CREATE TABLE csp_violations (
    id SERIAL PRIMARY KEY,
    violated_directive VARCHAR(255),
    blocked_uri TEXT,
    document_uri TEXT,
    source_file VARCHAR(255),
    line_number INTEGER,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **matching_cache** - AI Performance Cache
```sql
CREATE TABLE matching_cache (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    candidate_id INTEGER REFERENCES candidates(id),
    score DECIMAL(5,2),
    algorithm_version VARCHAR(50),
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(job_id, candidate_id, algorithm_version)
);
```

**Features**:
- **Performance Optimization**: Cache AI matching results
- **Version Tracking**: Algorithm version management
- **Expiration**: Automatic cache invalidation

#### **company_scoring_preferences** - Learning Engine
```sql
CREATE TABLE company_scoring_preferences (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    semantic_weight DECIMAL(3,2) DEFAULT 0.40,
    experience_weight DECIMAL(3,2) DEFAULT 0.30,
    skills_weight DECIMAL(3,2) DEFAULT 0.20,
    location_weight DECIMAL(3,2) DEFAULT 0.10,
    cultural_fit_bonus DECIMAL(3,2) DEFAULT 0.10,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(client_id)
);
```

**Features**:
- **Adaptive Learning**: Company-specific scoring weights
- **Phase 3 Engine**: Advanced AI learning capabilities
- **Weight Optimization**: Based on hiring feedback

---

## 🔧 Database Features

### **1. Performance Optimization**

#### **Indexes (75+ Total)**
```sql
-- Full-text search indexes
CREATE INDEX idx_candidates_skills_gin ON candidates USING GIN(to_tsvector('english', technical_skills));
CREATE INDEX idx_jobs_requirements_gin ON jobs USING GIN(to_tsvector('english', requirements));

-- Composite indexes for common queries
CREATE INDEX idx_candidates_location_experience ON candidates(location, experience_years);
CREATE INDEX idx_jobs_status_department ON jobs(status, department);
CREATE INDEX idx_feedback_candidate_job ON feedback(candidate_id, job_id);

-- Performance indexes
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_matching_cache_expires ON matching_cache(expires_at);
```

#### **Query Performance**
- **Response Time**: <50ms for typical queries
- **Full-text Search**: GIN indexes for skills and requirements
- **Composite Indexes**: Optimized for common query patterns
- **Partial Indexes**: For filtered queries

### **2. Data Integrity**

#### **Foreign Key Constraints**
```sql
-- Referential integrity
ALTER TABLE feedback ADD CONSTRAINT fk_feedback_candidate 
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE;
ALTER TABLE feedback ADD CONSTRAINT fk_feedback_job 
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE;
ALTER TABLE interviews ADD CONSTRAINT fk_interviews_candidate 
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE;
```

#### **Check Constraints**
```sql
-- Data validation
ALTER TABLE candidates ADD CONSTRAINT chk_experience_positive 
    CHECK (experience_years >= 0);
ALTER TABLE feedback ADD CONSTRAINT chk_integrity_range 
    CHECK (integrity >= 1 AND integrity <= 5);
ALTER TABLE offers ADD CONSTRAINT chk_salary_positive 
    CHECK (salary > 0);
```

### **3. Automated Functions**

#### **Timestamp Management**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_candidates_updated_at 
    BEFORE UPDATE ON candidates 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### **Audit Logging**
```sql
CREATE OR REPLACE FUNCTION audit_table_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (table_name, operation, old_values, new_values, created_at)
    VALUES (
        TG_TABLE_NAME,
        TG_OP,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END,
        CURRENT_TIMESTAMP
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

---

## 📊 Data Management

### **1. Sample Data Structure**

#### **Production Data Overview**
```sql
-- Current production data (as of November 15, 2025)
SELECT 
    'candidates' as table_name, COUNT(*) as record_count 
FROM candidates
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs
UNION ALL
SELECT 'clients', COUNT(*) FROM clients
UNION ALL
SELECT 'feedback', COUNT(*) FROM feedback;

-- Expected results:
-- candidates: 10+
-- jobs: 6+
-- clients: 3+
-- feedback: 5+
```

#### **Data Quality Metrics**
```sql
-- Data completeness check
SELECT 
    COUNT(*) as total_candidates,
    COUNT(technical_skills) as with_skills,
    COUNT(resume_path) as with_resume,
    COUNT(phone) as with_phone
FROM candidates;
```

### **2. Backup & Recovery**

#### **Backup Strategy**
```bash
# Daily automated backups
pg_dump -h hostname -U username -d bhiv_hr > backup_$(date +%Y%m%d).sql

# Point-in-time recovery setup
# WAL archiving enabled for production
```

#### **Recovery Procedures**
```bash
# Full database restore
psql -h hostname -U username -d bhiv_hr < backup_20251115.sql

# Selective table restore
pg_restore -h hostname -U username -d bhiv_hr -t candidates backup.dump
```

---

## 🔒 Security Features

### **1. Access Control**

#### **User Roles & Permissions**
```sql
-- Database roles
CREATE ROLE bhiv_read_only;
CREATE ROLE bhiv_app_user;
CREATE ROLE bhiv_admin;

-- Grant permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bhiv_read_only;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO bhiv_app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_admin;
```

#### **Row Level Security**
```sql
-- Enable RLS for sensitive tables
ALTER TABLE candidates ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY candidate_access_policy ON candidates
    FOR ALL TO bhiv_app_user
    USING (true);  -- Application handles access control
```

### **2. Data Encryption**

#### **Connection Security**
- **SSL/TLS**: All connections encrypted in transit
- **Certificate Validation**: Server certificate verification
- **Connection Pooling**: Secure connection management

#### **Data Protection**
- **Password Hashing**: bcrypt for all passwords
- **Sensitive Data**: PII handling with audit trails
- **GDPR Compliance**: Data retention and deletion policies

---

## 🔧 Maintenance & Operations

### **1. Database Monitoring**

#### **Performance Monitoring**
```sql
-- Query performance analysis
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Connection monitoring
SELECT 
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY state;
```

#### **Health Checks**
```sql
-- Database health check
SELECT 
    'database_size' as metric,
    pg_size_pretty(pg_database_size('bhiv_hr')) as value
UNION ALL
SELECT 
    'active_connections',
    COUNT(*)::text
FROM pg_stat_activity
WHERE state = 'active';
```

### **2. Maintenance Tasks**

#### **Regular Maintenance**
```sql
-- Update table statistics
ANALYZE;

-- Rebuild indexes if needed
REINDEX INDEX CONCURRENTLY idx_candidates_skills_gin;

-- Vacuum for space reclamation
VACUUM ANALYZE candidates;
```

#### **Performance Tuning**
```sql
-- Configuration recommendations
-- shared_buffers = 256MB
-- effective_cache_size = 1GB
-- work_mem = 4MB
-- maintenance_work_mem = 64MB
```

---

## 📈 Schema Evolution

### **1. Version History**

#### **Schema Versions**
- **v4.0.0**: Initial production schema
- **v4.1.0**: Added LangGraph workflow support
- **v4.2.0**: Enhanced security and performance features

#### **Migration Strategy**
```sql
-- Schema version tracking
CREATE TABLE schema_version (
    version VARCHAR(10) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Current version
INSERT INTO schema_version (version, description) 
VALUES ('4.2.0', 'Enhanced security and performance features');
```

### **2. Future Enhancements**

#### **Planned Features**
- **Partitioning**: Table partitioning for large datasets
- **Sharding**: Horizontal scaling preparation
- **Advanced Indexes**: Additional specialized indexes
- **Materialized Views**: Performance optimization views

---

## 🛠️ Development Guide

### **1. Local Setup**

#### **Database Setup**
```bash
# Using Docker Compose
docker-compose -f deployment/docker/docker-compose.production.yml up -d db

# Direct PostgreSQL setup
createdb bhiv_hr
psql bhiv_hr < services/db/consolidated_schema.sql
```

#### **Connection Configuration**
```bash
# Environment variables
DATABASE_URL=postgresql://bhiv_user:password@localhost:5432/bhiv_hr
DB_PASSWORD=your_secure_password
POSTGRES_PASSWORD=your_secure_password
```

### **2. Development Workflow**

#### **Schema Changes**
```bash
# 1. Create migration script
# 2. Test on development database
# 3. Update schema version
# 4. Deploy to production with backup
```

#### **Testing**
```bash
# Run database tests
python tests/database/test_schema.py
python tests/database/test_data_integrity.py
```

---

**BHIV HR Platform Database Documentation** - Complete PostgreSQL 17 database schema with 13 core tables, 75+ indexes, and enterprise security features.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: November 15, 2025 | **Schema**: v4.2.0 | **Tables**: 13 Core | **Status**: ✅ Production Ready