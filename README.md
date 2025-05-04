# Longest Common Subsequence Algorithms

This project implements and compares two algorithms for solving the Longest Common Subsequence (LCS) problem:

1. Brute-force approach
2. Dynamic programming approach

> **Note:** While the original project requirements document mentions "Longest Common Substring", this implementation focuses on the Longest Common Subsequence problem as clarified by the instructor.
>
> **Substring vs. Subsequence:**
>
> - A **substring** is a contiguous sequence of characters within a string
> - A **subsequence** is a sequence of characters that appear in the same order but not necessarily contiguously
> - Example: For strings "ABCDE" and "ACE", the longest common substring is "A" (length 1), while the longest common subsequence is "ACE" (length 3)

## Project Structure

```
.
├── data/                       # Generated test data and results
├── figures/                    # Generated visualization plots
├── src/
│   ├── __init__.py             # Package initialization
│   ├── lcs_algorithms.py       # Core algorithms implementation
│   ├── string_generator.py     # Random string generation utilities
│   ├── performance_tester.py   # Performance measurement
│   ├── visualizer.py           # Data visualization
│   └── dp_visualizer_ui.py     # Interactive DP table visualization
├── main.py                     # Main runner script
├── lcs_visualizer_executable.py # Standalone executable script
├── LCS_Visualizer.exe          # Windows executable (bonus component)
├── EXECUTABLE_INSTRUCTIONS.md  # Instructions for creating executable
├── VISUALIZER_INSTRUCTIONS.md  # Instructions for using the visualizer
└── README.md                   # This file
```

## Requirements

- Python 3.7+
- Required packages:
  - numpy
  - pandas
  - matplotlib
  - seaborn

## Installation

Install the required packages:

```
pip install -r requirements.txt
```

## Usage

```
# Run all tests from length 10 to 1000
python main.py --test

# Skip tests and just visualize existing results
python main.py --skip-tests

# Start the interactive DP table visualizer
python main.py --visualizer
```

**How the testing works:**

1. The program will first run all DP algorithm tests from length 10 to 1000, starting with the smallest combinations
2. Then it will run brute force tests from length 10 to 30 (also starting with the smallest) until they become too intensive and crash/timeout
3. Only results where both algorithms completed will be used for speedup comparisons
4. Results will be saved to CSV and visualized with 4 different plots

**Important Performance Notes:**

- The brute force algorithm has exponential complexity O(2^n), so it will only complete for small input sizes. The dynamic programming algorithm has polynomial complexity O(n\*m), so it can handle all input sizes.
- Running the brute force tests (with lengths 10-30) takes approximately 2 hours to complete. You can run only the DP tests with `--test-dp` which complete much faster.
- All parameters are fixed:
  - min_length is always 10
  - max_length is 30 for brute force and 1000 for DP
  - step is always 1

### Command Line Options

```
python main.py --help
```

Available options:

- `--test`: Run performance tests for both algorithms with fixed parameters
- `--test-dp`: Run only DP tests from length 10 to 1000
- `--test-bf`: Run only brute force tests from length 10 to 30
- `--skip-tests`: Skip tests and use existing results
- `--visualizer`: Start the interactive DP table visualizer

### Executable Visualizer

For the bonus visualization component, an executable is provided:

- Windows: Run `LCS_Visualizer.exe`
- See `EXECUTABLE_INSTRUCTIONS.md` for more details on using the executable

You can also run the Python script directly:

```
python lcs_visualizer_executable.py
```

## Algorithms

### Brute Force Approach

The brute force algorithm:

- Generates all possible subsequences of the first string
- Checks which ones are present in the second string
- Returns the longest matching subsequence

**Time Complexity**: O(2^n) where n is the length of the first string.

### Dynamic Programming Approach

The DP algorithm:

- Creates a 2D table of size (m+1) × (n+1)
- When matching characters are found, sets DP[i][j] = DP[i-1][j-1] + 1
- Otherwise, sets DP[i][j] = max(DP[i-1][j], DP[i][j-1])
- Backtracks through the table to reconstruct the subsequence

**Time Complexity**: O(nm) where n and m are the lengths of the strings.

**Note on Solution Non-uniqueness**: For some input strings, there may be multiple valid longest common subsequences of the same length. In such cases, the brute force and dynamic programming algorithms might return different subsequences, but both would have the correct maximum length.

## Performance Analysis

The project analyzes algorithm performance by:

1. Generating random strings of varying lengths
2. Measuring execution time for both algorithms
3. Creating visualizations to compare:
   - Runtime comparison between algorithms
   - Speedup factor of DP vs brute force
   - Theoretical vs experimental complexity

The results are saved to:

- CSV data in the `data/performance_results.csv` file
- Visualization plots in the `figures/` directory:
  - `runtime_comparison.png` - Compares runtime of both algorithms as input size increases
  - `speedup.png` - Shows the speedup factor of DP over brute force as a scatter plot
  - `theoretical_vs_experimental.png` - Compares measured runtime with theoretical complexity

### Interpreting the Results

1. **Runtime Comparison Plot**: Shows how dynamic programming runtime grows linearly with input size while brute force grows exponentially. The plot only includes tests where both algorithms completed successfully.

2. **Speedup Visualization**:

   - Scatter plot showing the speedup factor (brute force time / DP time) for each test case
   - Maximum and minimum speedup points are labeled
   - Horizontal line showing the median speedup across all test cases
   - Only includes tests where both algorithms successfully completed

3. **Theoretical vs Experimental**: Points represent actual measured times, while trend lines represent theoretical growth rates.

## Project Requirements

This project was developed to meet the requirements of comparing brute force and dynamic programming approaches for the Longest Common Subsequence problem using strings of lengths from 10 to 1000 characters.
