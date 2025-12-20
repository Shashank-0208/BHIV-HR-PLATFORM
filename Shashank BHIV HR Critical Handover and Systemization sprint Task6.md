Product: BHIV HR (Tenant-Ready, Mode A)

Sprint Type: Critical Handover + Systemization Sprint Duration: 3 Days (Hard Stop)

Delivery Deadline: Saturday (preferred) / Monday latest

⸻

READ THIS FIRST (MANDATORY)

You are not building new features.

Your responsibility is to convert the existing BHIV HR system into a clean, handover-ready, tenant-safe, auditable system package so that:
                • Ishan Shirode and Nikhil can continue without you 
                • Vinayak can test independently
                • Integration can proceed without needing you again unless absolutely required

Do NOT add logic
Do NOT refactor aggressively 
Do NOT introduce assumptions

Document
Freeze contracts 
Explain behavior
Surface edge cases

Outcome: Zero-dependency handover

⸻

INTEGRATION BLOCK

You must assume no future access to you.
                • Ishan Shirode — Backend continuation, AI/decision layers
                • Nikhil — Frontend / UI consumption
                • Vinayak — Testing & validation
                • Ashmit — Integration (read-only reference)
You are handing over to the system, not to a person.

⸻

TIMELINE

Total: 3 Days (Strict)
No extension unless explicitly approved.

⸻

DAY-BY-DAY BREAKDOWN
Day 1 — System Truth & Freeze

Finalize and freeze:
                • API contracts (request/response, error cases)
                • Tenant assumptions (what exists, what does NOT) 
                • Role enforcement points Produce:
                • SYSTEM_BEHAVIOR.md
                • TENANT_ASSUMPTIONS.md • ROLE_MATRIX.md

⸻

Day 2 — Handover Artifacts

                • Create FAQ.md
                • “What happens if X?”
                • “What is intentionally refused?” 
                • “What is NOT implemented?”
                • Create QA_CHECKLIST.md 
                • Tenant validation
                • Role violation cases
                • Missing-context refusal cases 
                • Create KNOWN_GAPS.md
                • Explicitly list what is unfinished or mocked

⸻

Day 3 — Testability & Exit • Provide:

                • Postman collection / curl examples • Test user roles & tenant scenarios
                • One clean walkthrough doc: HOW_TO_TEST.md 
                • Final task:
                • Push everything to Repo Depository 
                • Tag release: bhiv-hr-handover-v1
                • Notify Vinayak for testing

After this → You are DONE.

⸻

LEARNING KITS (REFERENCE ONLY — NO BUILD)

Use only to explain, not extend

Reading:
                • “Multi-tenant SaaS access control patterns” 
                •“RBAC vs ABAC — practical enforcement”
                •“Audit-first system design”

LLM PROMPTS (Optional):
                • “Explain tenant isolation failures in HR systems” 
                • “List refusal-first scenarios in regulated software”
                • “How to document APIs for zero-context takeover”

⸻

DELIVERABLES (NON-NEGOTIABLE)

You must submit:

1. SYSTEM_BEHAVIOR.md
2. TENANT_ASSUMPTIONS.md 
3. ROLE_MATRIX.md
4. FAQ.md
5. QA_CHECKLIST.md 
6. KNOWN_GAPS.md 
7. HOW_TO_TEST.md 
8. Tagged repo release
9.Test artifacts for Vinayak

If any are missing → task is INCOMPLETE.