#!/usr/bin/env python3
"""
String Generator Module
Provides functions to generate random strings for testing the LCS algorithms.
"""

import random
import string
import json
import os

def generate_random_string(length):
    """
    Generates a random string of specified length using English letters.
    
    Args:
        length (int): Length of the string to generate
        
    Returns:
        str: Random string containing only English letters
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def generate_test_cases(min_length=10, max_length=1000, step=100, num_cases=3):
    """
    Generates test cases with varying string lengths according to the project requirements.
    
    Args:
        min_length (int): Minimum string length (default 10 per requirements)
        max_length (int): Maximum string length (default 1000 per requirements)
        step (int): Step size for increasing string length
        num_cases (int): Number of test cases per size combination
        
    Returns:
        list: List of test cases, where each test case is a tuple (str1, str2, len1, len2)
    """
    test_cases = []
    
    # Generate test cases with different size combinations
    for len1 in range(min_length, max_length + 1, step):
        for len2 in range(min_length, max_length + 1, step):
            for _ in range(num_cases):
                str1 = generate_random_string(len1)
                str2 = generate_random_string(len2)
                test_cases.append((str1, str2, len1, len2))
    
    return test_cases


def save_test_cases(test_cases, filename='data/test_cases.json'):
    """
    Saves test cases to a JSON file.
    
    Args:
        test_cases (list): List of test cases
        filename (str): Path to save the file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    test_data = []
    for i, (str1, str2, len1, len2) in enumerate(test_cases):
        test_data.append({
            'id': i,
            'str1': str1,
            'str2': str2,
            'len1': len1,
            'len2': len2
        })
    
    with open(filename, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    return filename


def load_test_cases(filename='data/test_cases.json'):
    """
    Loads test cases from a JSON file.
    
    Args:
        filename (str): Path to the file
        
    Returns:
        list: List of test cases, where each test case is a tuple (str1, str2, len1, len2)
    """
    with open(filename, 'r') as f:
        test_data = json.load(f)
    
    test_cases = []
    for case in test_data:
        test_cases.append((case['str1'], case['str2'], case['len1'], case['len2']))
    
    return test_cases


if __name__ == "__main__":
    # Example usage
    test_cases = generate_test_cases(min_length=10, max_length=1000, step=150, num_cases=3)
    save_test_cases(test_cases)
    print(f"Generated {len(test_cases)} test cases and saved to data/test_cases.json")