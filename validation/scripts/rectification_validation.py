#!/usr/bin/env python3
"""
Gateway Rectification Validation
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
    
    # Validate Phase 1: No duplicates
    print(f"\nPHASE 1 VALIDATION - DUPLICATE REMOVAL:")
    duplicate_checks = [
        ("/v1/2fa/setup", "Should be removed"),
        ("/v1/password/validate", "Should be removed"), 
        ("/v1/csp/policies", "Should be removed"),
        ("/v1/auth/2fa/setup", "Should be kept"),
        ("/v1/auth/password/validate", "Should be kept"),
        ("/v1/security/csp-policies", "Should be kept")
    ]
    
    phase1_pass = True
    for endpoint, expected in duplicate_checks:
        found = endpoint.replace("/", "\\/") in content
        should_exist = "kept" in expected
        if found == should_exist:
            print(f"  [PASS] {endpoint}: {expected}")
        else:
            print(f"  [FAIL] {endpoint}: {expected}")
            phase1_pass = False
    
    print(f"  Phase 1 Status: {'PASS' if phase1_pass else 'FAIL'}")
    
    # Validate Phase 3: Core endpoints added
    print(f"\nPHASE 3 VALIDATION - CORE ENDPOINTS:")
    core_endpoints = ["/openapi.json", "/docs"]
    phase3_pass = True
    
    for endpoint in core_endpoints:
        found = endpoint.replace("/", "\\/") in content
        if found:
            print(f"  [PASS] {endpoint}: Added")
        else:
            print(f"  [FAIL] {endpoint}: Missing")
            phase3_pass = False
    
    print(f"  Phase 3 Status: {'PASS' if phase3_pass else 'FAIL'}")
    
    # Validate Phase 4: API versioning
    print(f"\nPHASE 4 VALIDATION - API VERSIONING:")
    versioning_checks = [
        ("/v1/test-candidates", "Should be versioned"),
        ("/v1/candidates/stats", "Should be versioned"),
        ('@app.get("/"', "Should remain unversioned"),
        ('@app.get("/health"', "Should remain unversioned"),
        ('@app.get("/metrics"', "Should remain unversioned")
    ]
    
    phase4_pass = True
    for check, expected in versioning_checks:
        found = check in content
        should_exist = "Should" in expected and "remain" not in expected
        if found == should_exist or ("remain" in expected and found):
            print(f"  [PASS] {check}: {expected}")
        else:
            print(f"  [FAIL] {check}: {expected}")
            phase4_pass = False
    
    print(f"  Phase 4 Status: {'PASS' if phase4_pass else 'FAIL'}")
    
    # Validate Phase 5: Documentation
    print(f"\nPHASE 5 VALIDATION - DOCUMENTATION:")
    description_match = re.search(r'description="([^"]*)"', content)
    phase5_pass = False
    
    if description_match:
        desc = description_match.group(1)
        # Check if description contains reasonable endpoint count
        endpoint_in_desc = re.search(r'(\d+)\s+Endpoints?', desc)
        if endpoint_in_desc:
            documented_count = int(endpoint_in_desc.group(1))
            if 60 <= documented_count <= 70:  # Reasonable range
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
    print(f"RECTIFICATION STATUS: {'COMPLETE - ALL VALIDATIONS PASS' if overall_status else 'INCOMPLETE - SOME VALIDATIONS FAILED'}")
    print(f"{'='*50}")
    
    return {
        "total_endpoints": total_endpoints,
        "phase1_pass": phase1_pass,
        "phase3_pass": phase3_pass, 
        "phase4_pass": phase4_pass,
        "phase5_pass": phase5_pass,
        "overall_pass": overall_status
    }

if __name__ == "__main__":
    result = validate_rectification()
    exit_code = 0 if result["overall_pass"] else 1
    exit(exit_code)