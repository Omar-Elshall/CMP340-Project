# Longest Common Substring Algorithms

This project implements and compares two algorithms for solving the Longest Common Substring (LCS) problem:
1. Brute-force approach
2. Dynamic programming approach

## Project Structure

```
.
├── data/                          # Generated test data and results
├── figures/                       # Generated visualization plots
├── src/
│   ├── __init__.py                # Package initialization
│   ├── lcs_algorithms.py          # Core algorithms implementation
│   ├── string_generator.py        # Random string generation utilities
│   ├── performance_tester.py      # Performance measurement
│   ├── visualizer.py              # Data visualization
│   └── dp_visualizer_ui.py        # Interactive DP table visualization
├── main.py                        # Main runner script
├── lcs_visualizer_executable.py   # Standalone executable script
├── EXECUTABLE_INSTRUCTIONS.md     # Instructions for creating executable
├── VISUALIZER_INSTRUCTIONS.md     # Instructions for using the visualizer
└── README.md                      # This file
```

## Requirements

- Python 3.7+
- Required packages:
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - tkinter (for the DP visualizer UI)

## Installation

1. Install the required packages:
```
pip3 install numpy pandas matplotlib seaborn
sudo apt-get install python3-tk  # For the DP visualizer UI
```

## Usage

### Running the Analysis

To run the full analysis with default settings:

```
python3 main.py
```

### Command Line Options

The main script supports various command line options:

```
python3 main.py --help
```

Options include:
- `--generate`: Generate new test cases
- `--min-length`: Minimum string length (default: 10)
- `--max-length`: Maximum string length (default: 500)
- `--step`: Step size for increasing length (default: 100)
- `--cases`: Number of test cases per size combination (default: 3)
- `--runs`: Number of runs for performance averaging (default: 3)
- `--skip-tests`: Skip performance tests (use existing results)
- `--example`: Create a DP table visualization for example strings
- `--str1`: First string for example (default: "abcdef")
- `--str2`: Second string for example (default: "acbcf")

### Examples

Generate new test cases with specific parameters:
```
python3 main.py --generate --min-length 20 --max-length 300 --step 50
```

Skip tests and just create visualizations from existing results:
```
python3 main.py --skip-tests
```

Visualize a specific example with custom strings:
```
python3 main.py --skip-tests --example --str1 "algorithm" --str2 "logarithm"
```

### Interactive DP Visualization

To run the interactive DP table visualizer:

```
# Using the main.py flag (recommended)
python3 main.py --visualizer

# Or directly running the visualizer
python3 src/dp_visualizer_ui.py
```

This will open a web-based interface in your browser where you can enter custom strings and see the dynamic programming table being built step by step.

### Standalone Executable

For the bonus visualization component, a standalone executable can be created:

```
# First install PyInstaller
pip install pyinstaller

# Then create the executable
pyinstaller --onefile --name=LCS_Visualizer lcs_visualizer_executable.py
```

For detailed instructions, see the `EXECUTABLE_INSTRUCTIONS.md` file.

## Algorithms

### Brute Force Approach

The brute force algorithm:
- Generates all possible substrings of the first string
- Checks which ones are present in the second string
- Returns the longest matching substring

**Time Complexity**: O(n²m) where n is the length of the first string and m is the length of the second string.

### Dynamic Programming Approach

The DP algorithm:
- Creates a 2D table of size (m+1) × (n+1)
- When matching characters are found, sets DP[i][j] = DP[i-1][j-1] + 1
- Tracks the maximum value and its position
- Extracts the substring from the original string

**Time Complexity**: O(nm) where n and m are the lengths of the strings.

## Performance Analysis

The project analyzes algorithm performance by:
1. Generating random strings of varying lengths
2. Measuring execution time for both algorithms
3. Creating visualizations to compare:
   - Runtime comparison between algorithms
   - Speedup factor of DP vs brute force
   - Theoretical vs experimental complexity

The results are saved as:
- CSV data in the `data/` directory
- Visualization plots in the `figures/` directory