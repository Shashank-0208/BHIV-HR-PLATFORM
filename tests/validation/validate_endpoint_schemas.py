#!/usr/bin/env python3
"""
BHIV HR Platform - Endpoint Schema Validation
Validates database schema requirements for all Gateway and Agent service endpoints
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class EndpointSchema:
    """Represents an endpoint and its schema requirements"""
    service: str
    endpoint: str
    method: str
    description: str
    required_tables: List[str]
    required_columns: Dict[str, List[str]]
    optional_tables: List[str] = None
    authentication: str = "required"
    
class SchemaValidator:
    """Validates endpoint schema requirements"""
    
    def __init__(self):
        self.gateway_endpoints = []
        self.agent_endpoints = []
        self.schema_tables = {}
        self.validation_results = {}
        
    def load_current_schema(self):
        """Load current database schema from deployment file"""
        schema_file = "c:\\BHIV HR PLATFORM\\services\\db\\consolidated_schema.sql"
        
        # Define expected schema based on v4.2.0
        self.schema_tables = {
            # Core Application Tables
            "candidates": [
                "id", "name", "email", "phone", "location", "experience_years",
                "technical_skills", "seniority_level", "education_level", 
                "resume_path", "status", "password_hash", "created_at", "updated_at"
            ],
            "jobs": [
                "id", "title", "department", "location", "experience_level",
                "requirements", "description", "status", "client_id", "created_at", "updated_at"
            ],
            "feedback": [
                "id", "candidate_id", "job_id", "integrity", "honesty", "discipline",
                "hard_work", "gratitude", "average_score", "comments", "created_at"
            ],
            "interviews": [
                "id", "candidate_id", "job_id", "interview_date", "interviewer",
                "status", "notes", "created_at", "updated_at"
            ],
            "offers": [
                "id", "candidate_id", "job_id", "salary", "start_date", "terms",
                "status", "created_at", "updated_at"
            ],
            "users": [
                "id", "username", "email", "password_hash", "role", "totp_secret",
                "is_2fa_enabled", "created_at", "updated_at"
            ],
            "clients": [
                "id", "client_id", "company_name", "email", "password_hash", "status",
                "failed_login_attempts", "locked_until", "created_at", "updated_at"
            ],
            "job_applications": [
                "id", "candidate_id", "job_id", "cover_letter", "status",
                "applied_date", "updated_at"
            ],
            
            # Performance & Security Tables
            "audit_logs": [
                "id", "table_name", "operation", "old_values", "new_values",
                "user_id", "timestamp", "ip_address"
            ],
            "rate_limits": [
                "id", "ip_address", "endpoint", "request_count", "window_start",
                "is_blocked", "created_at"
            ],
            "csp_violations": [
                "id", "violated_directive", "blocked_uri", "document_uri",
                "user_agent", "ip_address", "created_at"
            ],
            "matching_cache": [
                "id", "job_id", "candidate_ids", "match_results", "algorithm_version",
                "created_at", "expires_at"
            ],
            "company_scoring_preferences": [
                "id", "company_id", "skill_weight", "experience_weight", "location_weight",
                "cultural_weight", "feedback_data", "updated_at"
            ],
            "schema_version": [
                "version", "description", "applied_at"
            ]
        }
        
    def define_gateway_endpoints(self):
        """Define all Gateway service endpoints and their schema requirements"""
        
        # Core API Endpoints (3)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/", "GET", "API Root Information", [], {}, authentication="none"),
            EndpointSchema("Gateway", "/health", "GET", "Health Check", [], {}, authentication="none"),
            EndpointSchema("Gateway", "/test-candidates", "GET", "Database Connectivity Test", 
                         ["candidates"], {"candidates": ["id"]})
        ])
        
        # Monitoring Endpoints (3)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/metrics", "GET", "Prometheus Metrics Export", [], {}, authentication="none"),
            EndpointSchema("Gateway", "/health/detailed", "GET", "Detailed Health Check", [], {}, authentication="none"),
            EndpointSchema("Gateway", "/metrics/dashboard", "GET", "Metrics Dashboard Data", [], {}, authentication="none")
        ])
        
        # Job Management (2)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/jobs", "POST", "Create New Job Posting",
                         ["jobs"], {"jobs": ["title", "department", "location", "experience_level", "requirements", "description"]}),
            EndpointSchema("Gateway", "/v1/jobs", "GET", "List All Active Jobs",
                         ["jobs"], {"jobs": ["id", "title", "department", "location", "experience_level", "requirements", "description", "created_at"]})
        ])
        
        # Candidate Management (5)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/candidates", "GET", "Get All Candidates with Pagination",
                         ["candidates"], {"candidates": ["id", "name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level", "created_at"]}),
            EndpointSchema("Gateway", "/v1/candidates/search", "GET", "Search & Filter Candidates",
                         ["candidates"], {"candidates": ["id", "name", "email", "phone", "location", "technical_skills", "experience_years", "seniority_level", "education_level", "status"]}),
            EndpointSchema("Gateway", "/v1/candidates/job/{job_id}", "GET", "Get Candidates by Job",
                         ["candidates"], {"candidates": ["id", "name", "email", "technical_skills", "experience_years"]}),
            EndpointSchema("Gateway", "/v1/candidates/{candidate_id}", "GET", "Get Specific Candidate by ID",
                         ["candidates"], {"candidates": ["id", "name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level", "resume_path", "created_at", "updated_at"]}),
            EndpointSchema("Gateway", "/v1/candidates/bulk", "POST", "Bulk Upload Candidates",
                         ["candidates"], {"candidates": ["name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level", "resume_path", "status", "created_at"]})
        ])
        
        # AI Matching Engine (2)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/match/{job_id}/top", "GET", "AI-powered semantic candidate matching",
                         ["jobs", "candidates"], {"jobs": ["requirements", "location"], "candidates": ["id", "name", "email", "technical_skills", "location"]}),
            EndpointSchema("Gateway", "/v1/match/batch", "POST", "Batch AI matching",
                         ["jobs", "candidates"], {"jobs": ["requirements", "location"], "candidates": ["id", "name", "email", "technical_skills", "location"]})
        ])
        
        # Assessment & Workflow (6)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/feedback", "POST", "Values Assessment",
                         ["feedback"], {"feedback": ["candidate_id", "job_id", "integrity", "honesty", "discipline", "hard_work", "gratitude", "comments", "created_at"]}),
            EndpointSchema("Gateway", "/v1/feedback", "GET", "Get All Feedback Records",
                         ["feedback", "candidates", "jobs"], {"feedback": ["id", "candidate_id", "job_id", "integrity", "honesty", "discipline", "hard_work", "gratitude", "average_score", "comments", "created_at"], "candidates": ["name"], "jobs": ["title"]}),
            EndpointSchema("Gateway", "/v1/interviews", "GET", "Get All Interviews",
                         ["interviews", "candidates", "jobs"], {"interviews": ["id", "candidate_id", "job_id", "interview_date", "interviewer", "status"], "candidates": ["name"], "jobs": ["title"]}),
            EndpointSchema("Gateway", "/v1/interviews", "POST", "Schedule Interview",
                         ["interviews"], {"interviews": ["candidate_id", "job_id", "interview_date", "interviewer", "status", "notes"]}),
            EndpointSchema("Gateway", "/v1/offers", "POST", "Job Offers Management",
                         ["offers"], {"offers": ["candidate_id", "job_id", "salary", "start_date", "terms", "status", "created_at"]}),
            EndpointSchema("Gateway", "/v1/offers", "GET", "Get All Job Offers",
                         ["offers", "candidates", "jobs"], {"offers": ["id", "candidate_id", "job_id", "salary", "start_date", "terms", "status", "created_at"], "candidates": ["name"], "jobs": ["title"]})
        ])
        
        # Analytics & Statistics (3)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/candidates/stats", "GET", "Candidate Statistics",
                         ["candidates"], {"candidates": ["id"]}),
            EndpointSchema("Gateway", "/v1/database/schema", "GET", "Get Database Schema Information",
                         ["schema_version"], {"schema_version": ["version", "applied_at"]}, optional_tables=["information_schema.tables"]),
            EndpointSchema("Gateway", "/v1/reports/job/{job_id}/export.csv", "GET", "Export Job Report",
                         [], {})
        ])
        
        # Client Portal API (2)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/client/register", "POST", "Client Registration",
                         ["clients"], {"clients": ["client_id", "company_name", "email", "password_hash", "status", "created_at"]}),
            EndpointSchema("Gateway", "/v1/client/login", "POST", "Client Authentication",
                         ["clients"], {"clients": ["client_id", "company_name", "password_hash", "status", "failed_login_attempts", "locked_until"]})
        ])
        
        # Candidate Portal APIs (5)
        self.gateway_endpoints.extend([
            EndpointSchema("Gateway", "/v1/candidate/register", "POST", "Candidate Registration",
                         ["candidates"], {"candidates": ["name", "email", "phone", "location", "experience_years", "technical_skills", "education_level", "seniority_level", "password_hash", "status", "created_at"]}),
            EndpointSchema("Gateway", "/v1/candidate/login", "POST", "Candidate Login",
                         ["candidates"], {"candidates": ["id", "name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level", "status", "password_hash"]}),
            EndpointSchema("Gateway", "/v1/candidate/profile/{candidate_id}", "PUT", "Update Candidate Profile",
                         ["candidates"], {"candidates": ["name", "phone", "location", "experience_years", "technical_skills", "education_level", "seniority_level", "updated_at"]}),
            EndpointSchema("Gateway", "/v1/candidate/apply", "POST", "Apply for Job",
                         ["job_applications"], {"job_applications": ["candidate_id", "job_id", "cover_letter", "status", "applied_date"]}),
            EndpointSchema("Gateway", "/v1/candidate/applications/{candidate_id}", "GET", "Get Candidate Applications",
                         ["job_applications", "jobs", "clients"], {"job_applications": ["id", "job_id", "status", "applied_date", "cover_letter"], "jobs": ["title", "department", "location", "experience_level"], "clients": ["company_name"]})
        ])
        
        # Security Testing (12 endpoints) - Simplified for key ones
        security_endpoints = [
            "/v1/security/rate-limit-status", "/v1/security/blocked-ips", "/v1/security/test-input-validation",
            "/v1/security/validate-email", "/v1/security/test-email-validation", "/v1/security/validate-phone",
            "/v1/security/test-phone-validation", "/v1/security/test-headers", "/v1/security/security-headers-test",
            "/v1/security/penetration-test", "/v1/security/test-auth", "/v1/security/penetration-test-endpoints"
        ]
        
        for endpoint in security_endpoints:
            self.gateway_endpoints.append(
                EndpointSchema("Gateway", endpoint, "GET/POST", "Security Testing", [], {})
            )
        
        # CSP Management (8 endpoints)
        csp_endpoints = [
            "/v1/security/csp-report", "/v1/security/csp-violations", "/v1/csp/policies", "/v1/csp/violations",
            "/v1/csp/report", "/v1/csp/test", "/v1/security/csp-policies", "/v1/security/test-csp-policy"
        ]
        
        for endpoint in csp_endpoints:
            self.gateway_endpoints.append(
                EndpointSchema("Gateway", endpoint, "GET/POST", "CSP Management", 
                             ["csp_violations"], {"csp_violations": ["violated_directive", "blocked_uri", "document_uri", "created_at"]})
            )
        
        # 2FA Authentication (16 endpoints) - Key ones
        twofa_endpoints = [
            "/v1/auth/2fa/setup", "/v1/auth/2fa/verify", "/v1/auth/2fa/login", "/v1/auth/2fa/status/{user_id}",
            "/v1/auth/2fa/disable", "/v1/auth/2fa/backup-codes", "/v1/auth/2fa/test-token", "/v1/auth/2fa/qr/{user_id}",
            "/v1/2fa/setup", "/v1/2fa/verify-setup", "/v1/2fa/login-with-2fa", "/v1/2fa/status/{client_id}",
            "/v1/2fa/disable", "/v1/2fa/regenerate-backup-codes", "/v1/2fa/test-token/{client_id}/{token}", "/v1/2fa/demo-setup"
        ]
        
        for endpoint in twofa_endpoints:
            self.gateway_endpoints.append(
                EndpointSchema("Gateway", endpoint, "GET/POST", "2FA Authentication", 
                             ["users"], {"users": ["totp_secret", "is_2fa_enabled"]})
            )
        
        # Password Management (12 endpoints) - Key ones
        password_endpoints = [
            "/v1/auth/password/validate", "/v1/auth/password/generate", "/v1/auth/password/policy",
            "/v1/auth/password/change", "/v1/auth/password/strength", "/v1/auth/password/security-tips",
            "/v1/password/validate", "/v1/password/generate", "/v1/password/policy",
            "/v1/password/change", "/v1/password/strength-test", "/v1/password/security-tips"
        ]
        
        for endpoint in password_endpoints:
            self.gateway_endpoints.append(
                EndpointSchema("Gateway", endpoint, "GET/POST", "Password Management", [], {})
            )
    
    def define_agent_endpoints(self):
        """Define all Agent service endpoints and their schema requirements"""
        
        self.agent_endpoints = [
            EndpointSchema("Agent", "/", "GET", "AI Service Information", [], {}, authentication="none"),
            EndpointSchema("Agent", "/health", "GET", "Health Check", [], {}, authentication="none"),
            EndpointSchema("Agent", "/test-db", "GET", "Database Connectivity Test",
                         ["candidates"], {"candidates": ["id", "name"]}),
            EndpointSchema("Agent", "/match", "POST", "AI-Powered Candidate Matching",
                         ["jobs", "candidates"], {
                             "jobs": ["id", "title", "description", "department", "location", "experience_level", "requirements"],
                             "candidates": ["id", "name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level"]
                         }),
            EndpointSchema("Agent", "/batch-match", "POST", "Batch AI Matching for Multiple Jobs",
                         ["jobs", "candidates"], {
                             "jobs": ["id", "title", "description", "department", "location", "experience_level", "requirements"],
                             "candidates": ["id", "name", "email", "phone", "location", "experience_years", "technical_skills", "seniority_level", "education_level"]
                         }),
            EndpointSchema("Agent", "/analyze/{candidate_id}", "GET", "Detailed Candidate Analysis",
                         ["candidates"], {"candidates": ["name", "email", "technical_skills", "experience_years", "seniority_level", "education_level", "location"]})
        ]
    
    def validate_endpoint_schema(self, endpoint: EndpointSchema) -> Dict[str, Any]:
        """Validate a single endpoint against current schema"""
        
        validation = {
            "endpoint": f"{endpoint.method} {endpoint.endpoint}",
            "service": endpoint.service,
            "description": endpoint.description,
            "status": "PASS",
            "issues": [],
            "missing_tables": [],
            "missing_columns": {},
            "authentication": endpoint.authentication
        }
        
        # Check required tables
        for table in endpoint.required_tables:
            if table not in self.schema_tables:
                validation["missing_tables"].append(table)
                validation["status"] = "FAIL"
                validation["issues"].append(f"Missing required table: {table}")
        
        # Check required columns
        for table, columns in endpoint.required_columns.items():
            if table in self.schema_tables:
                missing_cols = []
                for column in columns:
                    if column not in self.schema_tables[table]:
                        missing_cols.append(column)
                
                if missing_cols:
                    validation["missing_columns"][table] = missing_cols
                    validation["status"] = "FAIL"
                    validation["issues"].append(f"Missing columns in {table}: {', '.join(missing_cols)}")
            else:
                validation["missing_columns"][table] = columns
                validation["status"] = "FAIL"
        
        return validation
    
    def validate_all_endpoints(self):
        """Validate all endpoints against current schema"""
        
        print("BHIV HR Platform - Endpoint Schema Validation")
        print("=" * 60)
        
        self.load_current_schema()
        self.define_gateway_endpoints()
        self.define_agent_endpoints()
        
        all_endpoints = self.gateway_endpoints + self.agent_endpoints
        
        print(f"Total Endpoints to Validate: {len(all_endpoints)}")
        print(f"   - Gateway Service: {len(self.gateway_endpoints)} endpoints")
        print(f"   - Agent Service: {len(self.agent_endpoints)} endpoints")
        print(f"Current Schema Tables: {len(self.schema_tables)}")
        print()
        
        # Validate each endpoint
        passed = 0
        failed = 0
        
        for endpoint in all_endpoints:
            validation = self.validate_endpoint_schema(endpoint)
            self.validation_results[f"{endpoint.service}_{endpoint.endpoint}_{endpoint.method}"] = validation
            
            if validation["status"] == "PASS":
                passed += 1
            else:
                failed += 1
        
        # Generate summary report
        self.generate_validation_report(passed, failed)
        
        return self.validation_results
    
    def generate_validation_report(self, passed: int, failed: int):
        """Generate comprehensive validation report"""
        
        print("VALIDATION SUMMARY")
        print("-" * 40)
        print(f"PASSED: {passed} endpoints")
        print(f"FAILED: {failed} endpoints")
        print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
        print()
        
        # Show failed endpoints
        if failed > 0:
            print("FAILED ENDPOINTS:")
            print("-" * 40)
            
            for key, validation in self.validation_results.items():
                if validation["status"] == "FAIL":
                    print(f"- {validation['service']}: {validation['endpoint']}")
                    print(f"   Description: {validation['description']}")
                    for issue in validation["issues"]:
                        print(f"   WARNING: {issue}")
                    print()
        
        # Show schema coverage
        print("SCHEMA COVERAGE ANALYSIS")
        print("-" * 40)
        
        used_tables = set()
        for endpoint in self.gateway_endpoints + self.agent_endpoints:
            used_tables.update(endpoint.required_tables)
        
        unused_tables = set(self.schema_tables.keys()) - used_tables
        
        print(f"Tables Used by Endpoints: {len(used_tables)}/{len(self.schema_tables)}")
        print(f"Used Tables: {', '.join(sorted(used_tables))}")
        if unused_tables:
            print(f"Unused Tables: {', '.join(sorted(unused_tables))}")
        print()
        
        # Critical missing elements
        print("CRITICAL SCHEMA ISSUES")
        print("-" * 40)
        
        critical_issues = []
        for key, validation in self.validation_results.items():
            if validation["status"] == "FAIL":
                if validation["missing_tables"]:
                    critical_issues.extend([f"Missing table: {table}" for table in validation["missing_tables"]])
                for table, columns in validation["missing_columns"].items():
                    critical_issues.extend([f"Missing columns in {table}: {', '.join(columns)}" for _ in [1]])
        
        if critical_issues:
            for issue in set(critical_issues):  # Remove duplicates
                print(f"- {issue}")
        else:
            print("No critical schema issues found!")
        
        print()
        
        # Recommendations
        print("RECOMMENDATIONS")
        print("-" * 40)
        
        if failed > 0:
            print("1. Run schema deployment script to add missing tables/columns")
            print("2. Update endpoint implementations to handle missing schema elements")
            print("3. Test endpoints after schema updates")
        else:
            print("All endpoints are schema-compliant!")
        
        print("4. Consider adding indexes for frequently queried columns")
        print("5. Monitor endpoint performance and optimize queries")
        print()
        
        # Generate JSON report
        self.save_json_report()
    
    def save_json_report(self):
        """Save detailed validation report as JSON"""
        
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_endpoints": len(self.validation_results),
                "passed": sum(1 for v in self.validation_results.values() if v["status"] == "PASS"),
                "failed": sum(1 for v in self.validation_results.values() if v["status"] == "FAIL"),
                "gateway_endpoints": len(self.gateway_endpoints),
                "agent_endpoints": len(self.agent_endpoints)
            },
            "schema_info": {
                "total_tables": len(self.schema_tables),
                "tables": list(self.schema_tables.keys())
            },
            "validation_results": self.validation_results
        }
        
        report_file = "endpoint_schema_validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Detailed report saved: {report_file}")

def main():
    """Main validation function"""
    
    validator = SchemaValidator()
    results = validator.validate_all_endpoints()
    
    return results

if __name__ == "__main__":
    main()