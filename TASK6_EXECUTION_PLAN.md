# Task 6 Execution Plan: BHIV HR Critical Handover & Systemization

**Product:** BHIV HR (Tenant-Ready, Mode A)  
**Sprint Type:** Critical Handover + Systemization  
**Duration:** 3 Days (Hard Stop)  
**Objective:** Zero-dependency handover for team continuation  

---

## Overview

This document outlines the complete execution plan for converting the existing BHIV HR system into a clean, handover-ready, tenant-safe, auditable system package. The plan follows the strict 3-day timeline with specific deliverables for each day.

**Key Principles:**
- ❌ NO new features
- ❌ NO aggressive refactoring  
- ❌ NO assumptions
- ✅ Document actual behavior
- ✅ Freeze contracts
- ✅ Surface edge cases

---

## System Analysis Summary

**Current State:**
- 6 microservices (Gateway, AI Agent, LangGraph, 3 Portals)
- 119 endpoints (80 Gateway + 6 Agent + 33 LangGraph)
- PostgreSQL database with 19 tables (13 core + 6 RL)
- Triple authentication (API Key, Client JWT, Candidate JWT)
- Basic tenant awareness via `client_id` field
- Minimal role-based access control

**Handover Recipients:**
- **Ishan Shirode:** Backend continuation, AI/decision layers
- **Nikhil:** Frontend/UI consumption
- **Vinayak:** Testing & validation
- **Ashmit:** Integration (read-only reference)

---

# DAY 1: System Truth & Freeze

## Step 1.1: Create SYSTEM_BEHAVIOR.md

### **Objective**
Document the actual behavior of all 119 endpoints, authentication flows, and system interactions as they currently exist in the codebase.

### **Implementation Tasks**
1. Analyze Gateway service (`services/gateway/app/main.py`) - 80 endpoints
2. Analyze AI Agent service (`services/agent/app.py`) - 6 endpoints  
3. Analyze LangGraph service (`services/langgraph/app/main.py`) - 33 endpoints
4. Document authentication behavior for all three methods
5. Document error handling patterns and rate limiting
6. Document workflow execution patterns and RL feedback loops

### **Files Touched**
- **Create:** `handover/SYSTEM_BEHAVIOR.md`
- **Reference:** 
  - `services/gateway/app/main.py`
  - `services/agent/app.py`
  - `services/langgraph/app/main.py`
  - `services/db/consolidated_schema.sql`

### **Expected Output**
Complete behavior documentation covering:
- Authentication behavior (API Key, Client JWT, Candidate JWT)
- Endpoint behavior with actual request/response examples
- Error handling patterns with status codes
- Rate limiting behavior (dynamic 60-500 req/min)
- Workflow execution patterns
- RL feedback loop behavior
- Database interaction patterns

### **Questions for User**

#### **Q1.1: Authentication Behavior**
1. Looking at `get_auth()` function in gateway, it accepts any of 3 auth methods (API Key, Client JWT, Candidate JWT). Is this the intended behavior for all endpoints?
2. Should I document which specific endpoints use which authentication method, or is the flexible approach intentional?
3. Are there endpoints that should require specific auth types but currently don't enforce it?

#### **Q1.2: Endpoint Behavior Documentation**
1. Should I document the actual response format I see in the code, or are there standardized response formats I should reference?
2. For endpoints with fallback behavior (e.g., AI Agent fallback when Phase 3 unavailable), should I document both paths?
3. Should I include performance characteristics (response times) or focus only on functional behavior?

#### **Q1.3: Error Handling Patterns**
1. I see various error responses (400, 401, 404, 500). Should I document the exact error messages as they appear in code?
2. Are there specific error scenarios that are critical for the handover team to understand?
3. Should I document database connection failure behavior and retry patterns?

---

## Step 1.2: Create TENANT_ASSUMPTIONS.md

### **Objective**
Document the tenant/client isolation model, clearly stating what exists versus what doesn't exist in the current implementation.

### **Implementation Tasks**
1. Analyze `clients` table structure and usage
2. Examine `client_id` field usage across tables (jobs, etc.)
3. Review client authentication and session management
4. Identify tenant isolation gaps in queries and endpoints
5. Document cross-tenant access patterns (intended vs actual)

### **Files Touched**
- **Create:** `handover/TENANT_ASSUMPTIONS.md`
- **Reference:**
  - `services/db/consolidated_schema.sql`
  - `services/gateway/app/main.py` (client endpoints)
  - `services/client_portal/app.py`
  - `services/portal/app.py`

### **Expected Output**
Clear documentation of:
- Client/tenant data model (clients table structure)
- What IS implemented (client_id in jobs, client authentication)
- What is NOT implemented (row-level security, tenant data isolation)
- Cross-tenant access patterns and vulnerabilities
- Data visibility rules and enforcement points

### **Questions for User**

#### **Q1.4: Tenant Model Clarification**
1. Is the `clients` table with `client_id` field the intended tenant model, or is this a simplified version?
2. Should clients be able to see ONLY their own jobs/candidates, or is there intended shared visibility?
3. Looking at queries in gateway, I don't see tenant filtering in most endpoints. Is this a gap or intentional?

#### **Q1.5: Current vs Intended Behavior**
1. Should I document what currently EXISTS (minimal tenant awareness) or what SHOULD exist (full isolation)?
2. Are there specific tenant isolation requirements I should reference, or should I infer from the code?
3. Should cross-tenant access be treated as a security vulnerability or acceptable behavior?

#### **Q1.6: Data Ownership**
1. Who owns candidates - are they shared across all clients or belong to specific clients?
2. Can Client A see applications from candidates who applied to Client B's jobs?
3. Should matching results be tenant-specific or global?

---

## Step 1.3: Create ROLE_MATRIX.md

### **Objective**
Document role-based access control, permissions matrix, and enforcement points as they currently exist in the system.

### **Implementation Tasks**
1. Analyze `users` table roles (admin, hr_manager, recruiter, user)
2. Examine role enforcement in gateway endpoints
3. Document client vs internal user permissions
4. Identify candidate permissions and restrictions
5. Map roles to endpoint access patterns

### **Files Touched**
- **Create:** `handover/ROLE_MATRIX.md`
- **Reference:**
  - `services/gateway/app/main.py` (role checking)
  - `services/db/consolidated_schema.sql` (users table)
  - `services/portal/auth_manager.py`
  - `services/client_portal/auth_manager.py`

### **Expected Output**
Matrix showing:
- Roles: admin, hr_manager, recruiter, client, candidate
- Permissions per role per endpoint category
- Enforcement points in code (where role checking occurs)
- What IS enforced vs what is NOT enforced
- Role hierarchy and inheritance

### **Questions for User**

#### **Q1.7: Role Enforcement Reality**
1. Looking at the gateway code, I see limited role checking. Are roles actively enforced or is this a gap?
2. Should I document the intended role matrix or the actual implementation?
3. Are there critical endpoints that should have role restrictions but currently don't?

#### **Q1.8: Role Definitions**
1. What's the difference between hr_manager and recruiter roles in terms of permissions?
2. Do clients have different permission levels (e.g., enterprise vs basic clients)?
3. Should candidates be able to access any admin/HR endpoints, or should they be completely restricted?

#### **Q1.9: Cross-Role Access**
1. Can hr_manager access client-specific data, or should they be restricted to their own organization?
2. Should admin role have access to all tenant data, or should tenant isolation apply to admins too?
3. Are there any "super admin" capabilities that bypass normal restrictions?

---

# DAY 2: Handover Artifacts

## Step 2.1: Create FAQ.md

### **Objective**
Answer "What happens if X?" scenarios based on actual code behavior, covering edge cases and system limitations.

### **Implementation Tasks**
1. Analyze common failure scenarios in code
2. Document "What is intentionally refused?" cases
3. Identify "What is NOT implemented?" gaps
4. Create edge case scenarios with actual responses
5. Reference existing FAQ.md for operational questions

### **Files Touched**
- **Create:** `handover/FAQ.md`
- **Reference:**
  - All service code for error handling
  - `handover/FAQ.md` (existing)
  - `handover/issues/ISSUES_AND_LIMITATIONS.md`

### **Expected Output**
FAQ covering:
- Authentication failure scenarios
- Cross-tenant access attempts
- Invalid data handling
- Service unavailability responses
- Rate limiting behavior
- Workflow failure scenarios

### **Questions for User**

#### **Q2.1: Critical Scenarios**
1. What are the most important "What happens if..." scenarios for the handover team?
2. Should I focus on security-related scenarios (unauthorized access) or functional scenarios (service failures)?
3. Are there specific edge cases that have caused issues in the past?

#### **Q2.2: Intentional Refusals**
1. What access patterns are intentionally blocked by the system?
2. Should I document security measures as "refusals" or as "features"?
3. Are there business rule violations that should be highlighted?

---

## Step 2.2: Create QA_CHECKLIST.md

### **Objective**
Create test scenarios for tenant validation, role violations, and missing-context refusals that Vinayak can execute.

### **Implementation Tasks**
1. Design tenant isolation test cases
2. Create role violation test scenarios
3. Develop missing-context refusal tests
4. Reference existing test files for patterns
5. Create authentication failure test cases

### **Files Touched**
- **Create:** `handover/QA_CHECKLIST.md`
- **Reference:**
  - `handover/QA_CHECKLIST.md` (existing)
  - `tests/` directory structure
  - `handover/postman_collection.json`

### **Expected Output**
Checklist with:
- Tenant validation tests (client isolation)
- Role violation tests (unauthorized access)
- Missing-context refusal tests (invalid IDs)
- Authentication failure tests
- Rate limiting tests
- Cross-service integration tests

### **Questions for User**

#### **Q2.3: Test Priorities**
1. Which test scenarios are highest priority for Vinayak's validation?
2. Should I focus on security tests (unauthorized access) or functional tests (feature validation)?
3. Are there specific test data sets I should reference or create?

#### **Q2.4: Test Environment**
1. Should tests be designed for production URLs or local development environment?
2. What test credentials should be used for different roles?
3. Should I include destructive tests (data modification) or only read-only tests?

---

## Step 2.3: Create KNOWN_GAPS.md

### **Objective**
Explicitly list unfinished features, mocked data, and system limitations without judgment.

### **Implementation Tasks**
1. Identify mocked or fallback behaviors in code
2. Document incomplete features and workarounds
3. List performance limitations and constraints
4. Reference existing issues and limitations
5. Identify security gaps and temporary solutions

### **Files Touched**
- **Create:** `handover/KNOWN_GAPS.md`
- **Reference:**
  - `handover/issues/ISSUES_AND_LIMITATIONS.md`
  - Code comments indicating TODOs or limitations
  - Service fallback implementations

### **Expected Output**
Honest documentation of:
- Mocked behaviors (AI Agent fallback)
- Incomplete features (full tenant isolation)
- Simplified implementations (basic role checking)
- Performance limitations (free tier constraints)
- Security gaps (missing validations)

### **Questions for User**

#### **Q2.5: Gap Classification**
1. Should I distinguish between "planned features" and "current limitations"?
2. Are there gaps that should NOT be documented publicly (security-sensitive)?
3. Should I include workarounds for each gap, or just document the limitation?

#### **Q2.6: Scope of Gaps**
1. Should I include infrastructure limitations (Render free tier) or focus on code gaps?
2. Are there third-party service limitations (Twilio, Gmail) that should be documented?
3. Should I document performance characteristics as gaps or as current specifications?

---

# DAY 3: Testability & Exit

## Step 3.1: Create HOW_TO_TEST.md

### **Objective**
Provide a clean walkthrough for testing all critical scenarios with curl/Postman examples.

### **Implementation Tasks**
1. Create step-by-step testing guide
2. Provide curl examples for critical flows
3. Document test user setup and credentials
4. Create tenant scenario testing procedures
5. Include expected responses for success/failure cases

### **Files Touched**
- **Create:** `handover/HOW_TO_TEST.md`
- **Reference:**
  - `handover/postman_collection.json`
  - `handover/POSTMAN_README.md`
  - Production and local service URLs

### **Expected Output**
Step-by-step guide with:
- Test environment setup
- User/client/candidate creation
- Authentication testing
- Tenant isolation verification
- Role-based access testing
- Workflow testing procedures

### **Questions for User**

#### **Q3.1: Testing Approach**
1. Should the guide focus on production testing (Render URLs) or local testing (Docker)?
2. What's the preferred testing method - curl commands or Postman collection?
3. Should I include automated test scripts or focus on manual testing procedures?

#### **Q3.2: Test Data**
1. Should I create new test data or use existing test clients (TECH001, STARTUP01)?
2. What test scenarios are most critical for validating the handover?
3. Should I include performance testing or focus on functional testing?

---

## Step 3.2: Update Test Artifacts

### **Objective**
Ensure Postman collection and test files cover tenant/role scenarios for Vinayak's testing.

### **Implementation Tasks**
1. Review existing Postman collection
2. Add tenant/role test cases if missing
3. Verify test data covers critical scenarios
4. Update collection with current endpoints
5. Validate test credentials and URLs

### **Files Touched**
- **Update:** `handover/postman_collection.json` (if needed)
- **Verify:** `tests/` directory
- **Update:** Test documentation

### **Expected Output**
- Updated Postman collection with tenant/role tests
- Verified test data for multiple clients/users
- Confirmation that existing tests cover critical paths

### **Questions for User**

#### **Q3.3: Test Coverage**
1. Does the existing Postman collection adequately cover tenant scenarios?
2. Are there missing test cases that should be added for the handover?
3. Should I create new test environments or use existing ones?

---

## Step 3.3: Tag Release & Final Verification

### **Objective**
Create git tag, verify all deliverables are present and complete.

### **Implementation Tasks**
1. Verify all 7 documents are complete
2. Create git tag `bhiv-hr-handover-v1`
3. Update repository README with handover status
4. Prepare notification for Vinayak
5. Final verification checklist

### **Files Touched**
- **Git:** Create tag `bhiv-hr-handover-v1`
- **Update:** `README.md` (handover status)
- **Verify:** All deliverable files

### **Expected Output**
- Git tag: `bhiv-hr-handover-v1`
- All 7 documents present and complete
- README updated with handover completion status
- Notification prepared for Vinayak

### **Questions for User**

#### **Q3.4: Release Process**
1. Should the git tag include any specific commit message or description?
2. How should I notify Vinayak for testing - GitHub issue, email, or other method?
3. Are there any post-handover tasks or follow-up requirements?

#### **Q3.5: Verification Criteria**
1. What constitutes "complete" for each document - word count, section coverage, or specific content?
2. Should I include a completion checklist in the README?
3. Are there any final review requirements before tagging the release?

---

# Deliverables Checklist

## Required Documents (Non-Negotiable)

- [ ] **SYSTEM_BEHAVIOR.md** - Complete system behavior documentation
- [ ] **TENANT_ASSUMPTIONS.md** - Tenant/client isolation model
- [ ] **ROLE_MATRIX.md** - Role-based access control matrix
- [ ] **FAQ.md** - "What happens if X?" scenarios
- [ ] **QA_CHECKLIST.md** - Test scenarios for validation
- [ ] **KNOWN_GAPS.md** - Unfinished features and limitations
- [ ] **HOW_TO_TEST.md** - Testing walkthrough guide

## Additional Deliverables

- [ ] **Tagged repo release** - `bhiv-hr-handover-v1`
- [ ] **Test artifacts for Vinayak** - Updated Postman collection and test data

## Success Criteria

✅ **Zero-dependency handover achieved**  
✅ **Team can continue without original developer**  
✅ **All system behavior documented accurately**  
✅ **No assumptions or fabricated details**  
✅ **All edge cases and limitations surfaced**  

---

# Next Steps

1. **Answer Critical Questions** (Q1.1 - Q3.5) to ensure accurate documentation
2. **Begin Day 1 execution** with SYSTEM_BEHAVIOR.md
3. **Daily check-ins** to verify progress and address questions
4. **Final verification** before tagging release

**Timeline:** 3 days strict - no extensions without explicit approval.

**Contact:** Notify Vinayak upon completion for independent testing and validation.