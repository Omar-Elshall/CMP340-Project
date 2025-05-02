"""
Longest Common Substring Project
This package contains the implementation and visualization tools for
the LCS algorithms.
"""

from .lcs_algorithms import dp_lcs, brute_force_lcs, get_dp_table
from .string_generator import generate_test_cases, save_test_cases, load_test_cases
from .performance_tester import run_performance_tests
from .visualizer import plot_performance_comparison, visualize_dp_table

__all__ = [
    'dp_lcs', 
    'brute_force_lcs',
    'get_dp_table',
    'generate_test_cases', 
    'save_test_cases', 
    'load_test_cases',
    'run_performance_tests',
    'plot_performance_comparison', 
    'visualize_dp_table'
]