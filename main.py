#!/usr/bin/env python3
"""
Simple main script for LCS project
"""

import os
import argparse
import pandas as pd
from src.visualizer import plot_performance_comparison
from src.performance_tester import run_basic_tests, run_dp_tests, run_brute_force_tests

def main():
    parser = argparse.ArgumentParser(description='Longest Common Subsequence Algorithm Comparison')
    parser.add_argument('--test', action='store_true', help='Run both algorithms with fixed parameters')
    parser.add_argument('--test-dp', action='store_true', help='Run only DP tests from length 10 to 1000')
    parser.add_argument('--test-bf', action='store_true', help='Run only brute force tests from length 10 to 30')
    parser.add_argument('--skip-tests', action='store_true', help='Skip tests and only generate visualizations')
    parser.add_argument('--visualizer', action='store_true', help='Start the interactive visualizer')
    args = parser.parse_args()

    # Make sure output directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    
    print("Longest Common Subsequence Algorithm Comparison")
    print("-----------------------------------------------")
    print("- Brute force: O(2^n) time complexity (tests take ~2 hours to complete)")
    print("- Dynamic programming: O(nm) time complexity")
    
    # Start interactive visualizer if requested
    if args.visualizer:
        try:
            from src.dp_visualizer_ui import start_server
            print("Starting interactive visualizer...")
            start_server()
            return
        except ImportError:
            print("Could not start visualizer. Make sure dp_visualizer_ui.py exists.")
            return
    
    # Run tests based on command line options
    if args.test:
        print("\nRunning performance tests with fixed parameters:")
        print("- Min length: 10")
        print("- Max length for brute force: 30")
        print("- Step size: 1")
        print("\nNote: Brute force tests will take approximately 2 hours to complete.")
        results = run_basic_tests(min_length=10, max_length=30, step=1)
    elif args.test_dp:
        print("\nRunning only DP tests with fixed parameters:")
        print("- Min length: 10")
        print("- Max length: 1000")
        print("- Step size: 1")
        results = run_dp_tests(min_length=10, max_length=1000, step=1)
    elif args.test_bf:
        print("\nRunning only brute force tests with fixed parameters:")
        print("- Min length: 10")
        print("- Max length: 30")
        print("- Step size: 1")
        print("\nNote: Brute force tests will take approximately 2 hours to complete.")
        results = run_brute_force_tests(min_length=10, max_length=30, step=1)
    
    # Skip tests if specified
    if args.skip_tests:
        print("\nSkipping tests, using existing results...")
        
    # Generate visualizations from results
    performance_file = 'data/performance_results.csv'
    dp_file = 'data/dp_results.csv'
    bf_file = 'data/bf_results.csv'
    
    # First check for combined results
    if os.path.exists(performance_file):
        print("\nGenerating visualization plots from combined results...")
        results_df = pd.read_csv(performance_file)
        
        # Filter for completed tests (both algorithms)
        complete_results = results_df[results_df['brute_force_time'].notna()]
        
        if len(complete_results) > 0:
            print(f"Found {len(complete_results)} tests with both algorithms")
            plot_files = plot_performance_comparison(complete_results)
            print(f"Created {len(plot_files)} plots in the figures directory")
        else:
            print("No completed tests found with both algorithms")
    
    # If no combined results but we have separate tests, try to merge them
    elif os.path.exists(dp_file) and os.path.exists(bf_file):
        print("\nFound separate DP and brute force test results. Merging for visualization...")
        
        dp_results = pd.read_csv(dp_file)
        bf_results = pd.read_csv(bf_file)
        
        # Merge based on common string lengths
        merged_results = pd.merge(
            dp_results, bf_results,
            on=['str1_length', 'str2_length', 'product_length'],
            how='inner',
            suffixes=('', '_bf')
        )
        
        # Calculate speedup
        if len(merged_results) > 0:
            merged_results['speedup'] = merged_results['brute_force_time'] / merged_results['dp_time']
            merged_results.to_csv(performance_file, index=False)
            
            print(f"Created merged dataset with {len(merged_results)} tests")
            plot_files = plot_performance_comparison(merged_results)
            print(f"Created {len(plot_files)} plots in the figures directory")
        else:
            print("No matching test combinations found between DP and brute force results")
    
    # If we only have DP results
    elif os.path.exists(dp_file):
        print("\nFound only DP test results. Cannot create comparison visualizations.")
        print("Run brute force tests with --test-bf to enable comparisons.")
    
    # If we only have BF results
    elif os.path.exists(bf_file):
        print("\nFound only brute force test results. Cannot create comparison visualizations.")
        print("Run DP tests with --test-dp to enable comparisons.")
    
    else:
        print("No test results found. Please run tests first with --test, --test-dp, or --test-bf")
        
    print("\nFinished!")
    print("\nUsage:")
    print("  python3 main.py --test       # Run both algorithms with fixed parameters")
    print("  python3 main.py --test-dp    # Run only DP tests (10-1000)")
    print("  python3 main.py --test-bf    # Run only brute force tests (10-30)")
    print("  python3 main.py --visualizer # Start interactive visualizer")
    print("  python3 main.py --skip-tests # Only generate visualizations")

if __name__ == "__main__":
    main()