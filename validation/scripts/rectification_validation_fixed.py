#!/usr/bin/env python3
"""
Gateway Rectification Validation - Fixed
Final validation of all completed rectification phases
"""

import re
from pathlib import Path

def validate_rectification():
    """Validate all rectification phases are complete"""
    
    print("GATEWAY RECTIFICATION - FINAL VALIDATION")
    print("=" * 50)
    
    gateway_file = Path("c:/BHIV HR PLATFORM/services/gateway/app/main.py")
    
    with open(gateway_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count total endpoints
    endpoint_patterns = [r'@app\.get\(', r'@app\.post\(', r'@app\.put\(', r'@app\.delete\(', r'@app\.patch\(']
    total_endpoints = sum(len(re.findall(pattern, content)) for pattern in endpoint_patterns)
    
    print(f"ENDPOINT COUNT VALIDATION:")
    print(f"  Total endpoints: {total_endpoints}")
    print(f"  Target range: 63-65 endpoints")
    print(f"  Status: {'PASS' if 63 <= total_endpoints <= 65 else 'FAIL'}")
    
    # Validate Phase 1: Duplicates removed
    print(f"\nPHASE 1 VALIDATION - DUPLICATE REMOVAL:")
    
    # Check removed duplicates
    removed_patterns = [
        '@app.post("/v1/2fa/setup"',
        '@app.post("/v1/password/validate"', 
        '@app.get("/v1/csp/policies"'
    ]
    
    # Check kept primary endpoints
    kept_patterns = [
        '@app.post("/v1/auth/2fa/setup"',
        '@app.post("/v1/auth/password/validate"',
        '@app.get("/v1/security/csp-policies"'
    ]
    
    phase1_pass = True
    
    for pattern in removed_patterns:
        found = pattern in content
        endpoint = pattern.split('"')[1]
        if not found:
            print(f"  [PASS] {endpoint}: Correctly removed")
        else:
            print(f"  [FAIL] {endpoint}: Still present")
            phase1_pass = False
    
    for pattern in kept_patterns:
        found = pattern in content
        endpoint = pattern.split('"')[1]
        if found:
            print(f"  [PASS] {endpoint}: Correctly kept")
        else:
            print(f"  [FAIL] {endpoint}: Missing")
            phase1_pass = False
    
    print(f"  Phase 1 Status: {'PASS' if phase1_pass else 'FAIL'}")
    
    # Validate Phase 3: Core endpoints added
    print(f"\nPHASE 3 VALIDATION - CORE ENDPOINTS:")
    core_patterns = [
        '@app.get("/openapi.json"',
        '@app.get("/docs"'
    ]
    phase3_pass = True
    
    for pattern in core_patterns:
        found = pattern in content
        endpoint = pattern.split('"')[1]
        if found:
            print(f"  [PASS] {endpoint}: Added")
        else:
            print(f"  [FAIL] {endpoint}: Missing")
            phase3_pass = False
    
    print(f"  Phase 3 Status: {'PASS' if phase3_pass else 'FAIL'}")
    
    # Validate Phase 4: API versioning
    print(f"\nPHASE 4 VALIDATION - API VERSIONING:")
    
    versioned_patterns = [
        '@app.get("/v1/test-candidates"',
        '@app.get("/v1/candidates/stats"'
    ]
    
    unversioned_patterns = [
        '@app.get("/"',
        '@app.get("/health"',
        '@app.get("/metrics"'
    ]
    
    phase4_pass = True
    
    for pattern in versioned_patterns:
        found = pattern in content
        endpoint = pattern.split('"')[1]
        if found:
            print(f"  [PASS] {endpoint}: Correctly versioned")
        else:
            print(f"  [FAIL] {endpoint}: Not versioned")
            phase4_pass = False
    
    for pattern in unversioned_patterns:
        found = pattern in content
        endpoint = pattern.split('"')[1]
        if found:
            print(f"  [PASS] {endpoint}: Correctly unversioned")
        else:
            print(f"  [FAIL] {endpoint}: Missing")
            phase4_pass = False
    
    print(f"  Phase 4 Status: {'PASS' if phase4_pass else 'FAIL'}")
    
    # Validate Phase 5: Documentation
    print(f"\nPHASE 5 VALIDATION - DOCUMENTATION:")
    description_match = re.search(r'description="([^"]*)"', content)
    phase5_pass = False
    
    if description_match:
        desc = description_match.group(1)
        endpoint_in_desc = re.search(r'(\d+)\s+Endpoints?', desc)
        if endpoint_in_desc:
            documented_count = int(endpoint_in_desc.group(1))
            if 60 <= documented_count <= 70:
                print(f"  [PASS] Description: '{desc}'")
                phase5_pass = True
            else:
                print(f"  [FAIL] Description count {documented_count} out of range")
        else:
            print(f"  [FAIL] No endpoint count in description")
    else:
        print(f"  [FAIL] No description found")
    
    print(f"  Phase 5 Status: {'PASS' if phase5_pass else 'FAIL'}")
    
    # Overall validation
    print(f"\nOVERALL VALIDATION:")
    all_phases_pass = phase1_pass and phase3_pass and phase4_pass and phase5_pass
    endpoint_count_pass = 63 <= total_endpoints <= 65
    
    print(f"  Phase 1 (Duplicates): {'PASS' if phase1_pass else 'FAIL'}")
    print(f"  Phase 3 (Core endpoints): {'PASS' if phase3_pass else 'FAIL'}")
    print(f"  Phase 4 (Versioning): {'PASS' if phase4_pass else 'FAIL'}")
    print(f"  Phase 5 (Documentation): {'PASS' if phase5_pass else 'FAIL'}")
    print(f"  Endpoint count: {'PASS' if endpoint_count_pass else 'FAIL'}")
    
    overall_status = all_phases_pass and endpoint_count_pass
    print(f"\n{'='*50}")
    print(f"RECTIFICATION STATUS: {'COMPLETE - ALL VALIDATIONS PASS' if overall_status else 'INCOMPLETE - VALIDATIONS FAILED'}")
    print(f"{'='*50}")
    
    return overall_status

if __name__ == "__main__":
    success = validate_rectification()
    print(f"\nFINAL RESULT: {'SUCCESS' if success else 'NEEDS ATTENTION'}")