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
    
    # 1. Runtime vs Product Length (simple comparison)
    plt.figure(figsize=(10, 6))
    
    # Filter out infinite values (skipped tests)
    filtered_df = results_df[results_df['brute_force_time'] != float('inf')]
    
    # Create scatter plot with trend lines
    plt.scatter(filtered_df['product_length'], filtered_df['brute_force_time'], 
                label='Brute Force', marker='o', alpha=0.7)
    plt.scatter(filtered_df['product_length'], filtered_df['dp_time'], 
                label='Dynamic Programming', marker='x', alpha=0.7)
    
    # Add trend lines
    bf_z = np.polyfit(filtered_df['product_length'], filtered_df['brute_force_time'], 1)
    bf_p = np.poly1d(bf_z)
    
    dp_z = np.polyfit(filtered_df['product_length'], filtered_df['dp_time'], 1)
    dp_p = np.poly1d(dp_z)
    
    # Get x values for plotting the fitted functions
    x_range = np.linspace(filtered_df['product_length'].min(), filtered_df['product_length'].max(), 100)
    
    plt.plot(x_range, bf_p(x_range), "--", color='blue')
    plt.plot(x_range, dp_p(x_range), "--", color='orange')
    
    plt.title('Runtime Comparison: Brute Force vs Dynamic Programming')
    plt.xlabel('Product of String Lengths (len1 × len2)')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    
    plot_path = os.path.join(output_dir, 'runtime_comparison.png')
    plt.savefig(plot_path)
    plot_files.append(plot_path)
    plt.close()
    
    # 2. Speedup Visualization with improved x-axis
    plt.figure(figsize=(10, 6))
    
    # Sort by product length for clearer visualization
    sorted_df = filtered_df.sort_values('product_length')
    
    # Create indices for the bars
    indices = range(len(sorted_df))
    
    # Plot speedup
    bars = plt.bar(indices, sorted_df['speedup'])
    
    # Improve x-axis labels
    # Only show a subset of the x-tick labels to avoid crowding
    if len(sorted_df) > 10:
        # Show approximately 10 labels evenly spaced
        step = max(1, len(sorted_df) // 10)
        plt.xticks(
            indices[::step], 
            sorted_df['product_length'].iloc[::step], 
            rotation=30, 
            ha='right'
        )
    else:
        plt.xticks(indices, sorted_df['product_length'], rotation=30, ha='right')
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.1,
            f'{height:.1f}',
            ha='center', 
            va='bottom',
            fontsize=8
        )
    
    plt.title('Speedup of Dynamic Programming over Brute Force')
    plt.xlabel('Product of String Lengths (len1 × len2)')
    plt.ylabel('Speedup Factor (Brute Force Time / DP Time)')
    plt.grid(True, axis='y')
    plt.tight_layout()  # Ensure all labels fit within the figure
    
    plot_path = os.path.join(output_dir, 'speedup.png')
    plt.savefig(plot_path)
    plot_files.append(plot_path)
    plt.close()
    
    # 3. Theoretical vs Experimental Complexity
    plt.figure(figsize=(10, 6))
    
    # For brute force, theoretical complexity is O(n^2 * m)
    # For DP, theoretical complexity is O(n * m)
    sorted_df['bf_theoretical'] = sorted_df['str1_length']**2 * sorted_df['str2_length'] / 1e9
    sorted_df['dp_theoretical'] = sorted_df['str1_length'] * sorted_df['str2_length'] / 1e6
    
    # Scale the theoretical curves
    bf_scale = sorted_df['brute_force_time'].mean() / sorted_df['bf_theoretical'].mean()
    dp_scale = sorted_df['dp_time'].mean() / sorted_df['dp_theoretical'].mean()
    
    sorted_df['bf_theoretical'] *= bf_scale
    sorted_df['dp_theoretical'] *= dp_scale
    
    plt.scatter(sorted_df['product_length'], sorted_df['brute_force_time'], 
               label='BF Experimental', marker='o')
    plt.scatter(sorted_df['product_length'], sorted_df['bf_theoretical'], 
               label='BF Theoretical O(n²m)', marker='+')
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
    ax.set_title("Dynamic Programming Table for Longest Common Substring")
    
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