#!/usr/bin/env python3
"""
Performance Testing Module
Measures and compares the performance of the LCS algorithms.
"""

import time
import os
import pandas as pd
from src.lcs_algorithms import brute_force_lcs, dp_lcs
from src.string_generator import generate_test_cases, save_test_cases, load_test_cases

def time_algorithm(algorithm, str1, str2, runs=3):
    """
    Measures the execution time of an algorithm.
    
    Args:
        algorithm (function): The algorithm to test
        str1 (str): First input string
        str2 (str): Second input string
        runs (int): Number of runs to average
        
    Returns:
        float: Average execution time in seconds
    """
    times = []
    
    for _ in range(runs):
        start_time = time.time()
        algorithm(str1, str2)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return sum(times) / len(times)


def run_performance_tests(test_cases, runs=3):
    """
    Runs performance tests on both algorithms for given test cases.
    
    Args:
        test_cases (list): List of test cases
        runs (int): Number of runs to average for each test
        
    Returns:
        pd.DataFrame: DataFrame containing the test results
    """
    results = []
    
    print(f"Running performance tests on {len(test_cases)} test cases...")
    
    for i, (str1, str2, len1, len2) in enumerate(test_cases):
        print(f"Testing case {i+1}/{len(test_cases)}: string lengths {len1}, {len2}")
        
        # Skip very large inputs for brute force to avoid excessive runtime
        if len1 * len2 <= 500000:  # Lower threshold to speed up tests
            bf_time = time_algorithm(brute_force_lcs, str1, str2, runs)
        else:
            bf_time = float('inf')  # Skip brute force for very large inputs
            print(f"  Skipping brute force for large input ({len1}x{len2})")
            
        dp_time = time_algorithm(dp_lcs, str1, str2, runs)
        
        result = {
            'case_id': i,
            'str1_length': len1,
            'str2_length': len2,
            'product_length': len1 * len2,
            'brute_force_time': bf_time,
            'dp_time': dp_time,
            'speedup': bf_time / dp_time if dp_time > 0 and bf_time != float('inf') else float('inf')
        }
        
        results.append(result)
        print(f"  Brute Force: {bf_time:.6f}s, DP: {dp_time:.6f}s, Speedup: {result['speedup']:.2f}x")
    
    # Create DataFrame and save results
    results_df = pd.DataFrame(results)
    os.makedirs('data', exist_ok=True)
    results_df.to_csv('data/performance_results.csv', index=False)
    print(f"Results saved to data/performance_results.csv")
    
    return results_df


if __name__ == "__main__":
    # Generate test cases with simpler parameters
    test_cases = generate_test_cases(min_length=10, max_length=500, step=100, num_cases=2)
    save_test_cases(test_cases)
    
    # Run performance tests
    results = run_performance_tests(test_cases)
    print("Performance testing completed")