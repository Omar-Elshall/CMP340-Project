#!/usr/bin/env python3
"""
Visualization Module
Generates visualizations of the performance results.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_performance_comparison(results_df, output_dir='figures'):
    """
    Creates basic performance comparison plots from test results.
    Only includes data points where both algorithms successfully completed.
    
    Args:
        results_df (pd.DataFrame): DataFrame containing test results
        output_dir (str): Directory to save the plots
        
    Returns:
        list: Paths to the saved plot files
    """
    os.makedirs(output_dir, exist_ok=True)
    plot_files = []
    
    # Set the style
    sns.set(style="whitegrid", font_scale=1.2)
    
    # Filter for tests where both algorithms completed
    complete_df = results_df[results_df['brute_force_time'].notna() & results_df['dp_time'].notna()].copy()
    
    # Calculate total test count and complete test count
    total_tests = len(results_df)
    complete_tests = len(complete_df)
    
    # 1. Runtime Comparison Plot
    plt.figure(figsize=(10, 6))
    
    # Add title with completion info
    plt.title(f'Runtime Comparison: Brute Force vs Dynamic Programming\n'
              f'({complete_tests} of {total_tests} tests have results from both algorithms)')
    
    plt.scatter(complete_df['product_length'], complete_df['brute_force_time'], 
                label='Brute Force', marker='o', alpha=0.7)
    plt.scatter(complete_df['product_length'], complete_df['dp_time'], 
                label='Dynamic Programming', marker='x', alpha=0.7)
    
    plt.xlabel('Product of String Lengths (len1 × len2)')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    
    plot_path = os.path.join(output_dir, 'runtime_comparison.png')
    plt.savefig(plot_path)
    plot_files.append(plot_path)
    plt.close()
    
    # 2. Speedup Scatter Plot
    plt.figure(figsize=(10, 6))
    
    # Sort by product length
    sorted_df = complete_df.sort_values('product_length').copy()
    sorted_df['speedup'] = sorted_df['brute_force_time'] / sorted_df['dp_time']
    
    # Create scatter plot showing speedup vs product length (just points, no lines)
    plt.scatter(sorted_df['product_length'], sorted_df['speedup'], 
                s=50, alpha=0.7, marker='o', edgecolors='k', linewidths=0.5)
    
    # Add a horizontal grid for better readability of values
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Label the most significant points on the graph
    max_idx = sorted_df['speedup'].idxmax()
    min_idx = sorted_df['speedup'].idxmin()
    
    # Label max point
    max_product = sorted_df.loc[max_idx, 'product_length']
    max_speedup = sorted_df.loc[max_idx, 'speedup']
    plt.annotate(f'Max: {max_speedup:.1f}x', 
                xy=(max_product, max_speedup),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center', va='bottom',
                fontweight='bold')
    
    # Label min point
    min_product = sorted_df.loc[min_idx, 'product_length']
    min_speedup = sorted_df.loc[min_idx, 'speedup']
    plt.annotate(f'Min: {min_speedup:.1f}x', 
                xy=(min_product, min_speedup),
                xytext=(0, -15),
                textcoords='offset points',
                ha='center', va='top')
    
    # Add median line
    median_speedup = sorted_df['speedup'].median()
    plt.axhline(y=median_speedup, color='green', linestyle='--', alpha=0.5)
    plt.annotate(f'Median: {median_speedup:.1f}x', 
                xy=(sorted_df['product_length'].max(), median_speedup),
                xytext=(-10, 0),
                textcoords='offset points',
                ha='right', va='center',
                color='green')
    
    plt.title(f'Speedup of Dynamic Programming over Brute Force\n'
              f'(Based on {complete_tests} tests with both algorithms)')
    plt.xlabel('Product of String Lengths (len1 × len2)')
    plt.ylabel('Speedup Factor (BF time / DP time)')
    
    # Format the x-axis to avoid overcrowding of labels
    if len(sorted_df) > 20:
        plt.locator_params(axis='x', nbins=10)
    
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, 'speedup.png')
    plt.savefig(plot_path)
    plot_files.append(plot_path)
    plt.close()
    
    # 3. Theoretical vs Experimental
    plt.figure(figsize=(10, 6))
    
    # Theoretical model
    # For DP: O(n*m) 
    # For BF: O(2^(n+m))
    sorted_df['bf_theoretical'] = np.power(2, sorted_df['str1_length'] + sorted_df['str2_length']) / 1e12
    sorted_df['dp_theoretical'] = sorted_df['str1_length'] * sorted_df['str2_length'] / 1e6
    
    # Scale factors
    bf_scale = sorted_df['brute_force_time'].mean() / sorted_df['bf_theoretical'].mean()
    dp_scale = sorted_df['dp_time'].mean() / sorted_df['dp_theoretical'].mean()
    
    sorted_df['bf_theoretical'] = sorted_df['bf_theoretical'] * bf_scale
    sorted_df['dp_theoretical'] = sorted_df['dp_theoretical'] * dp_scale
    
    plt.scatter(sorted_df['product_length'], sorted_df['brute_force_time'], 
                label='BF Experimental', marker='o')
    plt.scatter(sorted_df['product_length'], sorted_df['bf_theoretical'], 
                label='BF Theoretical O(2^(n+m))', marker='+')
    plt.scatter(sorted_df['product_length'], sorted_df['dp_time'], 
                label='DP Experimental', marker='x')
    plt.scatter(sorted_df['product_length'], sorted_df['dp_theoretical'], 
                label='DP Theoretical O(nm)', marker='*')
    
    plt.title('Theoretical vs Experimental Complexity')
    plt.xlabel('Product of String Lengths')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    
    plot_path = os.path.join(output_dir, 'theoretical_vs_experimental.png')
    plt.savefig(plot_path)
    plot_files.append(plot_path)
    plt.close()
    
    
    return plot_files


def visualize_dp_table(str1, str2):
    """
    Visualizes the dynamic programming table for the LCS problem.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    from src.lcs_algorithms import get_dp_table
    
    # Get the DP table
    table = get_dp_table(str1, str2)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create the heatmap
    sns.heatmap(table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    
    # Add labels
    ax.set_xlabel(f"String 2: '{str2}'")
    ax.set_ylabel(f"String 1: '{str1}'")
    ax.set_title("Dynamic Programming Table for Longest Common Subsequence")
    
    # Add string characters as labels
    x_labels = [''] + list(str2)
    y_labels = [''] + list(str1)
    
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Example usage
    try:
        results = pd.read_csv('data/performance_results.csv')
        plots = plot_performance_comparison(results)
        print(f"Created {len(plots)} plots in the figures directory")
    except FileNotFoundError:
        print("No performance results found. Run performance_tester.py first.")