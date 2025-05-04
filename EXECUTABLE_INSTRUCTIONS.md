# Creating an Executable for the LCS Visualizer

This document explains how to create a standalone executable for the Longest Common Subsequence Visualizer, which can be distributed and run without requiring Python installation.

> **Note:** The project now has fixed parameters for testing:
>
> - min_length = 10
> - max_length = 30 for brute force, 1000 for DP
> - step = 1
>
> When running tests, please be aware that brute force tests take approximately 2 hours to complete with these parameters.

## Prerequisites

1. You need Python installed on your system to create the executable
2. You need PyInstaller package to bundle the application

## Steps to Create the Executable

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Create the Executable

Navigate to the project directory and run:

```bash
# For Windows
pyinstaller --onefile --name=LCS_Visualizer lcs_visualizer_executable.py

# For macOS
pyinstaller --onefile --windowed --name=LCS_Visualizer lcs_visualizer_executable.py

# For Linux
pyinstaller --onefile --name=LCS_Visualizer lcs_visualizer_executable.py
```

### 3. Find the Executable

The executable will be created in the `dist` folder:

- Windows: `dist/LCS_Visualizer.exe`
- macOS: `dist/LCS_Visualizer`
- Linux: `dist/LCS_Visualizer`

## Running the Executable

### For users on Windows:

1. Double-click the `LCS_Visualizer.exe` file
2. A command prompt window will open showing the server status
3. Your web browser should open automatically to the visualization
4. To stop the program, close the command prompt window or press Ctrl+C

### For users on macOS:

1. Double-click the `LCS_Visualizer` application
2. Your web browser should open automatically to the visualization
3. To stop the program, quit the application or press Ctrl+C in Terminal if you launched it from there

### For users on Linux:

1. Run the `LCS_Visualizer` file (`./LCS_Visualizer` from a terminal)
2. Your web browser should open automatically to the visualization
3. To stop the program, press Ctrl+C in the terminal

## Troubleshooting

1. If the browser doesn't open automatically, manually go to `http://localhost:8000` or check the console output for the correct URL
2. If you see an error about the port being in use, the program will automatically try to find an available port
3. Make sure you have permission to execute the file (chmod +x on Linux/macOS if needed)
