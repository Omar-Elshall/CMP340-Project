# Longest Common Substring Visualizer

This is a visualization tool that shows how the dynamic programming algorithm builds the DP table to find the longest common substring between two strings.

## How to Run the Visualizer

1. Double-click the executable file:
   - Windows: `LCS_Visualizer.exe`
   - macOS: `LCS_Visualizer`
   - Linux: `./LCS_Visualizer` (make sure it's executable with `chmod +x LCS_Visualizer`)

2. A command window will appear showing the server has started

3. Your web browser should open automatically to the visualization page
   - If it doesn't, open your browser and go to the URL shown in the command window (usually http://localhost:8000)

4. To stop the visualizer, close the command window or press Ctrl+C in it

## How to Use the Visualizer

1. **Input custom strings**:
   - Enter your strings in the "String 1" and "String 2" input boxes
   - Click "Visualize" to generate the DP table visualization

2. **Navigate through the algorithm steps**:
   - Use the "Previous" and "Next" buttons to step through the algorithm
   - Current position in the table is highlighted in red
   - The longest common substring path is highlighted in yellow

3. **Understand the information**:
   - Each step description is shown above the table
   - The final result shows the longest common substring and its length
   - The table coordinates and indices help you follow the algorithm's progress

## Visualization Features

- **Step-by-step execution**: See exactly how the DP table is filled one cell at a time
- **Current cell highlighting**: The current cell being filled is highlighted in red
- **Path highlighting**: The cells forming the longest common substring are highlighted in yellow
- **Detailed descriptions**: Each step shows which characters are being compared and how the table is updated
- **User input**: Try different string combinations to see how the algorithm works in different scenarios

## Example

Try visualizing with these strings:
- String 1: "ABCDE"
- String 2: "CBDA"

Watch how the algorithm finds the longest common substring by filling in the DP table cell by cell.