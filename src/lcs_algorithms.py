#!/usr/bin/env python3
"""
Longest Common Subsequence Algorithms
This module implements both brute-force and dynamic programming solutions
for finding the longest common subsequence between two strings.
"""

import itertools

def is_subsequence(subseq, string):
    """Check if subseq is a subsequence of string"""
    it = iter(string)
    return all(c in it for c in subseq)

def brute_force_lcs(str1, str2):
    """
    Finds the longest common subsequence between two strings using brute force.
    Time Complexity: O(2^n) where n is the length of the first string.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        tuple: (longest common subsequence, length of subsequence)
    """
    if not str1 or not str2:
        return "", 0
    
    # Swap strings if the first one is longer (optimization)
    if len(str1) > len(str2):
        str1, str2 = str2, str1
    
    # Start with the longest possible subsequence length
    for length in range(min(len(str1), len(str2)), 0, -1):
        # For each possible subsequence of this length from str1
        for indices in itertools.combinations(range(len(str1)), length):
            # Extract the subsequence
            subsequence = ''.join(str1[i] for i in indices)
            
            # Check if it's a subsequence of str2
            if is_subsequence(subsequence, str2):
                return subsequence, length
    
    return "", 0


def dp_lcs(str1, str2):
    """
    Finds the longest common subsequence between two strings using dynamic programming.
    Time Complexity: O(nm) where n and m are the lengths of the strings.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        tuple: (longest common subsequence, length of subsequence)
    """
    if not str1 or not str2:
        return "", 0
        
    # Create DP table
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Fill the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Backtrack to find the LCS
    i, j = m, n
    lcs = []
    
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            lcs.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    # Reverse the LCS (we built it backwards)
    lcs = ''.join(reversed(lcs))
    return lcs, len(lcs)


def get_dp_table(str1, str2):
    """
    Returns the dynamic programming table used to solve the LCS problem.
    For visualization in the bonus UI component.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        list: 2D DP table
    """
    if not str1 or not str2:
        return [[]]
        
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp


if __name__ == "__main__":
    # Example usage
    str1 = "ABCBDAB"
    str2 = "BDCABA"
    
    print(f"String 1: {str1}")
    print(f"String 2: {str2}")
    
    # Brute force approach
    bf_result, bf_length = brute_force_lcs(str1, str2)
    print(f"Brute Force LCS: {bf_result} (length: {bf_length})")
    
    # Dynamic programming approach
    dp_result, dp_length = dp_lcs(str1, str2)
    print(f"DP LCS: {dp_result} (length: {dp_length})")