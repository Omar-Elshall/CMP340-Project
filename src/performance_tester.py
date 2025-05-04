#!/usr/bin/env python3
"""
Performance Testing Module
"""

import time
import os
import pandas as pd
import gc
import random
import string
from src.lcs_algorithms import brute_force_lcs, dp_lcs

def generate_random_string(length):
    """Generate a random string of given length with both uppercase and lowercase letters."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def run_dp_tests(min_length=10, max_length=1000, step=1):
    """
    Run only the DP algorithm tests.
    
    Args:
        min_length: Minimum string length to test (default: 10)
        max_length: Maximum string length to test (default: 1000)
        step: Step size for testing (default: 1)
    """
    # Clear any existing results
    if os.path.exists('data/dp_results.csv'):
        os.remove('data/dp_results.csv')
    
    # Generate all the string lengths to test
    lengths = list(range(min_length, max_length + 1, step))
    print(f"Testing DP algorithm with strings from length {min_length} to {max_length}")
    print(f"Total test sizes: {len(lengths)}")
    
    # Create all combinations and sort by product size (smaller first)
    all_combinations = []
    for len1 in lengths:
        for len2 in lengths:
            all_combinations.append((len1, len2, len1 * len2))
    
    # Sort by product size (smallest first)
    all_combinations.sort(key=lambda x: x[2])
    
    print(f"Total test combinations: {len(all_combinations)}")
    
    results = []
    
    # Run all DP tests in order of increasing product size
    print("\n===== RUNNING DP TESTS (SMALLEST FIRST) =====")
    for len1, len2, product in all_combinations:
        # Generate random strings with mixed case
        str1 = generate_random_string(len1)
        str2 = generate_random_string(len2)
        
        print(f"DP test for strings of length {len1} and {len2} (product: {product})")
        
        # Run DP algorithm
        gc.collect()  # Clear memory
        dp_start = time.time()
        dp_result, dp_length = dp_lcs(str1, str2)
        dp_time = time.time() - dp_start
        
        result = {
            'case_id': len(results),
            'str1_length': len1,
            'str2_length': len2,
            'product_length': product,
            'dp_time': dp_time,
            'brute_force_time': None,  # Adding None for compatibility with merge operations
            'speedup': None            # Adding None for compatibility with merge operations
        }
        
        results.append(result)
        print(f"  DP time: {dp_time:.6f}s")
        
        # Save after each test
        os.makedirs('data', exist_ok=True)
        pd.DataFrame(results).to_csv('data/dp_results.csv', index=False)
    
    print(f"\nCompleted {len(results)} DP tests")
    
    return pd.DataFrame(results)


def run_brute_force_tests(min_length=10, max_length=30, step=1):
    """
    Run only the brute force algorithm tests.
    
    Args:
        min_length: Minimum string length to test (default: 10)
        max_length: Maximum string length to test (default: 30)
        step: Step size for testing (default: 1)
    """
    # Clear any existing results
    if os.path.exists('data/bf_results.csv'):
        os.remove('data/bf_results.csv')
    
    # Generate all the string lengths to test
    lengths = list(range(min_length, max_length + 1, step))
    print(f"Testing brute force with strings from length {min_length} to {max_length}")
    print(f"Total test sizes: {len(lengths)}")
    
    # Create all combinations and sort by product size (smaller first)
    all_combinations = []
    for len1 in lengths:
        for len2 in lengths:
            all_combinations.append((len1, len2, len1 * len2))
    
    # Sort by product size (smallest first)
    all_combinations.sort(key=lambda x: x[2])
    
    print(f"Total test combinations: {len(all_combinations)}")
    
    results = []
    
    print("\n===== RUNNING BRUTE FORCE TESTS (SMALLEST FIRST) =====")
    for len1, len2, product in all_combinations:
        # Generate random strings with mixed case
        str1 = generate_random_string(len1)
        str2 = generate_random_string(len2)
        
        print(f"Brute force test for strings of length {len1} and {len2} (product: {product})")
        
        # Try to run brute force
        try:
            gc.collect()  # Clear memory
            bf_start = time.time()
            bf_result, bf_length = brute_force_lcs(str1, str2)
            bf_time = time.time() - bf_start
            
            result = {
                'case_id': len(results),
                'str1_length': len1,
                'str2_length': len2,
                'product_length': product,
                'brute_force_time': bf_time,
                'dp_time': None,   # Adding None for compatibility with merge operations
                'speedup': None    # Adding None for compatibility with merge operations
            }
            
            results.append(result)
            print(f"  BF time: {bf_time:.6f}s")
            
            # Save after each test
            os.makedirs('data', exist_ok=True)
            pd.DataFrame(results).to_csv('data/bf_results.csv', index=False)
            
        except (MemoryError, KeyboardInterrupt, Exception) as e:
            print(f"  Brute force test failed: {e}")
            print("Stopping brute force tests as they're becoming too intensive")
            break
    
    print(f"\nCompleted {len(results)} brute force tests")
    
    return pd.DataFrame(results)


def run_basic_tests(min_length=10, max_length=30, step=1):
    """
    Run a very basic performance test with no special handling.
    First runs all DP tests in order of increasing product size, 
    then runs brute force tests until it cannot complete.
    
    Args:
        min_length: Minimum string length to test (always 10)
        max_length: Maximum string length to test (always 30 for brute force)
        step: Step size for testing (always 1)
    """
    # Clear any existing results
    if os.path.exists('data/performance_results.csv'):
        os.remove('data/performance_results.csv')
    
    # Generate all the string lengths to test
    lengths = list(range(min_length, max_length + 1, step))
    print(f"Testing strings from length {min_length} to {max_length} with step {step}")
    print(f"Total test sizes: {len(lengths)}")
    
    # Create all combinations and sort by product size (smaller first)
    all_combinations = []
    for len1 in lengths:
        for len2 in lengths:
            all_combinations.append((len1, len2, len1 * len2))
    
    # Sort by product size (smallest first)
    all_combinations.sort(key=lambda x: x[2])
    
    print(f"Total test combinations: {len(all_combinations)}")
    
    results = []
    
    # First run all DP tests in order of increasing product size
    print("\n===== RUNNING DP TESTS (SMALLEST FIRST) =====")
    for len1, len2, product in all_combinations:
        # Generate random strings with mixed case
        str1 = generate_random_string(len1)
        str2 = generate_random_string(len2)
        
        print(f"DP test for strings of length {len1} and {len2} (product: {product})")
        
        # Run DP algorithm
        gc.collect()  # Clear memory
        dp_start = time.time()
        dp_result, dp_length = dp_lcs(str1, str2)
        dp_time = time.time() - dp_start
        
        result = {
            'case_id': len(results),
            'str1_length': len1,
            'str2_length': len2,
            'product_length': product,
            'dp_time': dp_time,
            'brute_force_time': None,  # Will fill this in if brute force completes
            'speedup': None            # Will calculate if brute force completes
        }
        
        results.append(result)
        print(f"  DP time: {dp_time:.6f}s")
        
        # Save after each test
        os.makedirs('data', exist_ok=True)
        pd.DataFrame(results).to_csv('data/performance_results.csv', index=False)
    
    # Now run brute force tests in the same order until they can't complete
    print("\n===== RUNNING BRUTE FORCE TESTS (SMALLEST FIRST) =====")
    brute_force_crashed = False
    
    for i, result in enumerate(results):
        if brute_force_crashed:
            break
            
        len1 = result['str1_length']
        len2 = result['str2_length']
        product = result['product_length']
        
        # Regenerate the same strings
        str1 = generate_random_string(len1)
        str2 = generate_random_string(len2)
        
        print(f"Brute force test for strings of length {len1} and {len2} (product: {product})")
        
        # Try to run brute force
        try:
            gc.collect()  # Clear memory
            bf_start = time.time()
            bf_result, bf_length = brute_force_lcs(str1, str2)
            bf_time = time.time() - bf_start
            
            # Update the result with brute force time
            result['brute_force_time'] = bf_time
            result['speedup'] = bf_time / result['dp_time'] if result['dp_time'] > 0 else float('inf')
            
            print(f"  BF time: {bf_time:.6f}s, Speedup: {result['speedup']:.2f}x")
            
            # Save after each test
            pd.DataFrame(results).to_csv('data/performance_results.csv', index=False)
            
        except (MemoryError, KeyboardInterrupt, Exception) as e:
            print(f"  Brute force test failed: {e}")
            brute_force_crashed = True
            print("Stopping brute force tests as they're becoming too intensive")
    
    # Create final results with only the complete cases
    complete_results = [r for r in results if r['brute_force_time'] is not None]
    
    print(f"\nCompleted {len(complete_results)} tests with both algorithms")
    print(f"Total tests: {len(results)}")
    
    # Save final results
    pd.DataFrame(results).to_csv('data/performance_results.csv', index=False)
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    run_basic_tests(min_length=10, max_length=100, step=100)