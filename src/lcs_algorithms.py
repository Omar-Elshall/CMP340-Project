#!/usr/bin/env python3
"""
Longest Common Substring Algorithms
This module implements both brute-force and dynamic programming solutions
for finding the longest common substring between two strings.
"""

def brute_force_lcs(str1, str2):
    """
    Finds the longest common substring between two strings using brute force.
    Time Complexity: O(n²m) where n is the length of str1 and m is the length of str2.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        tuple: (longest common substring, length of substring)
    """
    if not str1 or not str2:
        return "", 0
        
    longest = ""
    max_length = 0
    
    # Check all possible substrings of str1
    for i in range(len(str1)):
        for j in range(i + 1, len(str1) + 1):
            substring = str1[i:j]
            # If this substring is longer than our current longest and exists in str2
            if len(substring) > max_length and substring in str2:
                max_length = len(substring)
                longest = substring
    
    return longest, max_length


def dp_lcs(str1, str2):
    """
    Finds the longest common substring between two strings using dynamic programming.
    Time Complexity: O(nm) where n and m are the lengths of the strings.
    
    Args:
        str1 (str): First input string
        str2 (str): Second input string
        
    Returns:
        tuple: (longest common substring, length of substring)
    """
    if not str1 or not str2:
        return "", 0
        
    # Create DP table
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Variables to store result
    max_length = 0
    end_index = 0
    
    # Fill the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_index = i
            else:
                dp[i][j] = 0
    
    # Extract the longest common substring
    if max_length == 0:
        return "", 0
        
    start_index = end_index - max_length
    longest = str1[start_index:end_index]
    
    return longest, max_length


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
                dp[i][j] = 0
    
    return dp