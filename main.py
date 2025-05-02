#!/usr/bin/env python3
"""
Main Runner Script for LCS Project
Executes the workflow for testing, analyzing, and visualizing 
the performance of the LCS algorithms.
"""

import os
import argparse
import pandas as pd
import importlib.util
import subprocess
import sys
from src.string_generator import generate_test_cases, save_test_cases, load_test_cases
from src.performance_tester import run_performance_tests
from src.visualizer import plot_performance_comparison, visualize_dp_table
from src.lcs_algorithms import dp_lcs

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Longest Common Substring Algorithm Comparison')
    
    parser.add_argument('--generate', action='store_true',
                       help='Generate new test cases (otherwise uses existing ones if available)')
    parser.add_argument('--min-length', type=int, default=10,
                       help='Minimum string length for test cases')
    parser.add_argument('--max-length', type=int, default=500,
                       help='Maximum string length for test cases')
    parser.add_argument('--step', type=int, default=100, 
                       help='Step size for increasing string length')
    parser.add_argument('--cases', type=int, default=3,
                       help='Number of test cases per size combination')
    parser.add_argument('--runs', type=int, default=3,
                       help='Number of runs to average for each performance test')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Skip performance tests (use existing results)')
    parser.add_argument('--example', action='store_true',
                       help='Visualize a DP table example')
    parser.add_argument('--str1', type=str, default='abcdef',
                       help='First string for DP table visualization example')
    parser.add_argument('--str2', type=str, default='acbcf',
                       help='Second string for DP table visualization example')
    parser.add_argument('--visualizer', action='store_true',
                       help='Start the interactive DP table visualizer in a web browser')
    
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Start the interactive visualizer if requested
    if args.visualizer:
        print("Starting the interactive DP table visualizer...")
        try:
            # Try to import the module directly
            from src.dp_visualizer_ui import start_server
            start_server()
            return
        except ImportError:
            # If that fails, try to run it as a script
            try:
                subprocess.run([sys.executable, 'src/dp_visualizer_ui.py'], check=True)
                return
            except subprocess.CalledProcessError:
                print("Failed to start the visualizer. Make sure src/dp_visualizer_ui.py exists and is executable.")
                return
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    
    # Generate or load test cases
    if args.generate or not os.path.exists('data/test_cases.json'):
        print(f"Generating test cases from length {args.min_length} to {args.max_length}")
        test_cases = generate_test_cases(
            min_length=args.min_length,
            max_length=args.max_length,
            step=args.step,
            num_cases=args.cases
        )
        save_test_cases(test_cases)
        print(f"Generated {len(test_cases)} test cases")
    else:
        test_cases = load_test_cases()
        print(f"Loaded {len(test_cases)} test cases from file")
    
    # Run performance tests
    if not args.skip_tests or not os.path.exists('data/performance_results.csv'):
        print("Running performance tests...")
        results_df = run_performance_tests(test_cases, args.runs)
    else:
        print("Loading existing performance results...")
        results_df = pd.read_csv('data/performance_results.csv')
    
    # Generate visualization plots
    print("Generating performance visualization plots...")
    plot_files = plot_performance_comparison(results_df)
    print(f"Created {len(plot_files)} plots in the figures directory")
    
    # Visualize a DP table example (if requested)
    if args.example:
        print(f"Visualizing DP table for example strings:")
        print(f"String 1: '{args.str1}'")
        print(f"String 2: '{args.str2}'")
        
        # Get the longest common substring using DP
        lcs, length = dp_lcs(args.str1, args.str2)
        print(f"Longest Common Substring: '{lcs}' (length: {length})")
        
        # Visualize the DP table
        fig = visualize_dp_table(args.str1, args.str2)
        example_path = 'figures/dp_table_example.png'
        fig.savefig(example_path)
        print(f"Saved DP table visualization to {example_path}")
    
    print("\nAll tasks completed successfully!")
    print("\nSummary of files created:")
    print("- data/test_cases.json: Test strings")
    print("- data/performance_results.csv: Performance measurements")
    print("- figures/runtime_comparison.png: Runtime comparison")
    print("- figures/speedup.png: Speedup visualization")
    print("- figures/theoretical_vs_experimental.png: Theoretical vs. experimental complexity")
    if args.example:
        print("- figures/dp_table_example.png: DP table visualization")
    
    # Print information about the interactive visualizer
    print("\nFor interactive visualization, run:")
    print("  python3 main.py --visualizer")


if __name__ == "__main__":
    main()