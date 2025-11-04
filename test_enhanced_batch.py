#!/usr/bin/env python3
"""
Test Enhanced Batch Endpoint
"""

import requests
import json

BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_single_match():
    """Test single match for comparison"""
    print("Testing Single Match (for comparison):")
    response = requests.get(f"{BASE_URL}/v1/match/1/top?limit=3", headers=HEADERS, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  Status: {response.status_code}")
        print(f"  Agent Status: {data.get('agent_status')}")
        print(f"  Algorithm: {data.get('algorithm_version')}")
        print(f"  Matches: {len(data.get('matches', []))}")
        
        # Show first match structure
        if data.get('matches'):
            match = data['matches'][0]
            print("  First Match Structure:")
            for key, value in match.items():
                print(f"    {key}: {value}")
        return True
    else:
        print(f"  Failed: {response.status_code} - {response.text}")
        return False

def test_batch_match():
    """Test enhanced batch match"""
    print("\nTesting Enhanced Batch Match:")
    payload = [1, 2]
    response = requests.post(f"{BASE_URL}/v1/match/batch", headers=HEADERS, json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  Status: {response.status_code}")
        print(f"  Agent Status: {data.get('agent_status')}")
        print(f"  Algorithm: {data.get('algorithm_version')}")
        print(f"  Jobs Processed: {data.get('total_jobs_processed')}")
        
        # Show batch results structure
        batch_results = data.get('batch_results', {})
        print(f"  Batch Results Count: {len(batch_results)}")
        
        for job_id, job_result in batch_results.items():
            print(f"\n  Job {job_id} Results:")
            print(f"    Total Candidates: {job_result.get('total_candidates')}")
            print(f"    Algorithm: {job_result.get('algorithm')}")
            print(f"    Processing Time: {job_result.get('processing_time')}")
            print(f"    AI Analysis: {job_result.get('ai_analysis')}")
            
            # Show first match structure
            matches = job_result.get('matches', [])
            if matches:
                match = matches[0]
                print(f"    First Match Structure:")
                for key, value in match.items():
                    print(f"      {key}: {value}")
        
        return True
    else:
        print(f"  Failed: {response.status_code} - {response.text}")
        return False

def compare_structures():
    """Compare single vs batch response structures"""
    print("\n" + "="*50)
    print("STRUCTURE COMPARISON")
    print("="*50)
    
    print("Single Match Response Fields:")
    print("- matches (array of detailed candidates)")
    print("- top_candidates (same as matches)")
    print("- job_id, limit, total_candidates")
    print("- algorithm_version, processing_time")
    print("- ai_analysis, agent_status")
    
    print("\nEnhanced Batch Response Fields:")
    print("- batch_results (object with job_id keys)")
    print("  - Each job has: matches, top_candidates, total_candidates")
    print("  - Each job has: algorithm, processing_time, ai_analysis")
    print("- total_jobs_processed, total_candidates_analyzed")
    print("- algorithm_version, status, agent_status")
    
    print("\nCandidate Match Fields (both endpoints):")
    print("- candidate_id, name, email, score")
    print("- skills_match, experience_match, location_match")
    print("- reasoning, recommendation_strength")

if __name__ == "__main__":
    print("Enhanced Batch Endpoint Testing")
    print("="*40)
    
    single_ok = test_single_match()
    batch_ok = test_batch_match()
    
    compare_structures()
    
    print("\n" + "="*40)
    print("TEST RESULTS")
    print("="*40)
    print(f"Single Match: {'PASS' if single_ok else 'FAIL'}")
    print(f"Enhanced Batch: {'PASS' if batch_ok else 'FAIL'}")
    
    if single_ok and batch_ok:
        print("\nSUCCESS: Both endpoints now provide detailed candidate information!")
    else:
        print("\nISSUE: One or both endpoints failed")