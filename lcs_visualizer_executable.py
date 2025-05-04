#!/usr/bin/env python3
"""
Longest Common Subsequence Visualizer
A standalone executable for visualizing the dynamic programming approach.

This file is designed to be compiled into a standalone executable using PyInstaller.
It contains all necessary code for the visualization and does not depend on the
rest of the project structure.

Run with:
    python lcs_visualizer_executable.py

Create executable with:
    pyinstaller --onefile --name=LCS_Visualizer lcs_visualizer_executable.py

See EXECUTABLE_INSTRUCTIONS.md for more details.
"""

import numpy as np
import webbrowser
import http.server
import socketserver
from urllib.parse import parse_qs, urlparse
import os
import sys
import threading
import time

# Define the LCS algorithm function
def dp_lcs(str1, str2):
    """
    Finds the longest common subsequence between two strings using dynamic programming.
    
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

# HTML template for the visualization
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LCS Visualizer</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .dp-table { border-collapse: collapse; margin: 20px 0; }
        .dp-table td { 
            width: 40px; height: 40px; text-align: center; 
            border: 1px solid #999; font-weight: bold; 
        }
        .dp-table .header { background: #eee; font-style: italic; }
        .dp-table .empty { background: #f8f8f8; }
        .dp-table .current { background: #ff9999; }
        .dp-table .lcs-path { background: #ffff99; }
        .controls { margin: 20px 0; }
        button { padding: 5px 15px; margin: 0 5px; cursor: pointer; }
        .step-info { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 4px; }
        input[type="text"] { padding: 5px; width: 200px; }
        form { margin-bottom: 20px; }
        h1 { color: #333; }
        .footer { margin-top: 40px; font-size: 12px; color: #777; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Longest Common Subsequence Visualizer</h1>
        
        <form method="post" action="/">
            <div>
                <label for="str1">String 1:</label>
                <input type="text" id="str1" name="str1" value="{{str1}}">
            </div>
            <div style="margin-top: 10px;">
                <label for="str2">String 2:</label>
                <input type="text" id="str2" name="str2" value="{{str2}}">
            </div>
            <button type="submit" style="margin-top: 10px;">Visualize</button>
        </form>
        
        {{result}}
        
        <div class="step-info">{{step_info}}</div>
        
        <table class="dp-table">
            {{table}}
        </table>
        
        <div class="controls">
            <a href="/?str1={{str1}}&str2={{str2}}&step={{prev_step}}"><button {{prev_disabled}}>Previous</button></a>
            <span>Step {{current_step}} of {{total_steps}}</span>
            <a href="/?str1={{str1}}&str2={{str2}}&step={{next_step}}"><button {{next_disabled}}>Next</button></a>
        </div>
        
        <div class="footer">
            <p>Created for CMP340 Project - Longest Common Subsequence Visualization</p>
        </div>
    </div>
    <script>
        // Auto-reload if url has reload=true
        if (window.location.href.includes('reload=true')) {
            window.location.href = window.location.href.replace('reload=true', '');
        }
    </script>
</body>
</html>
"""

class DPState:
    """Class to handle DP algorithm state generation and storage"""
    
    def __init__(self, str1, str2):
        self.str1 = str1.upper()
        self.str2 = str2.upper()
        self.steps = self.generate_steps()
        
    def generate_steps(self):
        """Generate all steps of the DP algorithm"""
        steps = []
        m, n = len(self.str1), len(self.str2)
        
        # Initial state (empty table)
        dp = np.zeros((m + 1, n + 1), dtype=int)
        steps.append({
            'dp': dp.copy(),
            'i': None, 'j': None,
            'description': "Initial DP table (all cells set to 0)",
            'max_length': 0,
            'lcs_path': []
        })
        
        # Fill the DP table step by step
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.str1[i-1] == self.str2[j-1]:
                    # Characters match
                    dp[i, j] = dp[i-1, j-1] + 1
                    desc = f"Match: '{self.str1[i-1]}' at DP[{i},{j}] = {dp[i,j]} (diagonal + 1)"
                else:
                    # No match, take max of left or top cell
                    dp[i, j] = max(dp[i-1, j], dp[i, j-1])
                    if dp[i-1, j] >= dp[i, j-1]:
                        desc = f"No match: DP[{i},{j}] = {dp[i,j]} (from top cell)"
                    else:
                        desc = f"No match: DP[{i},{j}] = {dp[i,j]} (from left cell)"
                
                # Save step
                steps.append({
                    'dp': dp.copy(),
                    'i': i, 'j': j,
                    'description': desc,
                    'max_length': dp[m, n],  # The max length is always in the bottom-right
                    'lcs_path': []  # Will be calculated in the final step
                })
        
        # Calculate the LCS path for the final state
        if steps[-1]['max_length'] > 0:
            # Backtrack to find the LCS path
            i, j = m, n
            path_cells = []
            lcs_chars = []
            
            while i > 0 and j > 0:
                if self.str1[i-1] == self.str2[j-1]:
                    path_cells.append((i, j))
                    lcs_chars.append(self.str1[i-1])
                    i -= 1
                    j -= 1
                elif dp[i-1, j] > dp[i, j-1]:
                    i -= 1
                else:
                    j -= 1
            
            # Reverse the path (we built it backwards)
            path_cells.reverse()
            lcs_chars.reverse()
            lcs = ''.join(lcs_chars)
            
            steps[-1]['lcs_path'] = path_cells
            steps[-1]['description'] += f"<br>Final result: '{lcs}' (length: {steps[-1]['max_length']})"
        
        return steps
    
    def get_step(self, step_idx):
        """Get a specific step of the visualization"""
        if step_idx < 0 or step_idx >= len(self.steps):
            step_idx = 0
        return self.steps[step_idx]
    
    def get_total_steps(self):
        """Get the total number of steps"""
        return len(self.steps)


class WebVisualizer(http.server.SimpleHTTPRequestHandler):
    """Simple HTTP handler for DP visualization"""
    
    # Class variable to store current state
    dp_state = None
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        str1 = params.get('str1', ['ABCDE'])[0]
        str2 = params.get('str2', ['CBDA'])[0]
        
        # Create a new state if needed or strings changed
        if (WebVisualizer.dp_state is None or 
            WebVisualizer.dp_state.str1 != str1.upper() or 
            WebVisualizer.dp_state.str2 != str2.upper()):
            WebVisualizer.dp_state = DPState(str1, str2)
        
        # Get step index
        try:
            step_idx = int(params.get('step', ['0'])[0])
        except ValueError:
            step_idx = 0
        
        # Generate HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Show the visualization
        html = self.generate_html(str1, str2, step_idx)
        self.wfile.write(html.encode())
    
    def do_POST(self):
        """Handle POST requests (form submissions)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        # Extract form data
        str1 = params.get('str1', ['ABCDE'])[0]
        str2 = params.get('str2', ['CBDA'])[0]
        
        # Redirect to GET with the new strings
        self.send_response(303)  # See Other
        self.send_header('Location', f'/?str1={str1}&str2={str2}&reload=true')
        self.end_headers()
    
    def generate_html(self, str1, str2, step_idx):
        """Generate HTML for the current state"""
        total_steps = WebVisualizer.dp_state.get_total_steps()
        
        # Ensure step_idx is within range
        if step_idx < 0:
            step_idx = 0
        if step_idx >= total_steps:
            step_idx = total_steps - 1
        
        # Get current step
        step = WebVisualizer.dp_state.get_step(step_idx)
        
        # Run the algorithm for the result
        if step_idx == 0:
            lcs, length = dp_lcs(str1, str2)
            result = f"<div style='margin-top: 15px;'><b>Longest Common Subsequence:</b> '{lcs}' (length: {length})</div>"
        else:
            result = ""
        
        # Generate the table HTML
        table_html = self.generate_table_html(step, str1, str2)
        
        # Generate navigation buttons state
        prev_disabled = "disabled" if step_idx == 0 else ""
        next_disabled = "disabled" if step_idx == total_steps - 1 else ""
        
        # Fill the HTML template
        html = HTML.replace("{{str1}}", str1)
        html = html.replace("{{str2}}", str2)
        html = html.replace("{{result}}", result)
        html = html.replace("{{table}}", table_html)
        html = html.replace("{{step_info}}", step['description'])
        html = html.replace("{{current_step}}", str(step_idx + 1))
        html = html.replace("{{total_steps}}", str(total_steps))
        html = html.replace("{{prev_step}}", str(max(0, step_idx - 1)))
        html = html.replace("{{next_step}}", str(min(total_steps - 1, step_idx + 1)))
        html = html.replace("{{prev_disabled}}", prev_disabled)
        html = html.replace("{{next_disabled}}", next_disabled)
        
        return html
    
    def generate_table_html(self, step, str1, str2):
        """Generate HTML for the DP table"""
        dp = step['dp']
        m, n = len(str1), len(str2)
        i, j = step['i'], step['j']
        
        # Start building the table
        table = []
        
        # Row 1: Empty cells + String 2 characters
        row = ["<tr>"]
        row.append("<td class='empty'></td>")  # Top-left empty cell
        row.append("<td class='empty'></td>")  # Empty cell above indices
        
        # Add String 2 characters
        for j_idx in range(n):
            row.append(f"<td class='header'>{str2[j_idx]}</td>")
        row.append("</tr>")
        table.append("".join(row))
        
        # Row 2: Empty cell + column indices
        row = ["<tr>"]
        row.append("<td class='empty'></td>")  # Empty cell before row indices
        
        # Add column indices
        for j_idx in range(n + 1):
            row.append(f"<td class='header'>{j_idx}</td>")
        row.append("</tr>")
        table.append("".join(row))
        
        # Data rows
        for i_idx in range(m + 1):
            row = ["<tr>"]
            
            # First column: row indices for data rows
            if i_idx == 0:
                row.append("<td class='header'>0</td>")
            else:
                # Add String 1 character + row index
                row.append(f"<td class='header'>{str1[i_idx-1]}{i_idx}</td>")
            
            # Add data cells
            for j_idx in range(n + 1):
                # Determine cell class
                cell_class = ""
                
                # Current cell being filled
                if i_idx == i and j_idx == j:
                    cell_class = "current"
                # Cell in LCS path
                elif (i_idx, j_idx) in step['lcs_path']:
                    cell_class = "lcs-path"
                
                row.append(f"<td class='{cell_class}'>{int(dp[i_idx, j_idx])}</td>")
            
            row.append("</tr>")
            table.append("".join(row))
        
        return "".join(table)


def find_available_port(start_port=8000, max_attempts=100):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            # Try to bind to the port
            with socketserver.TCPServer(("", port), None) as server:
                pass
            return port
        except OSError:
            continue
    # If no ports are available, return a default
    return 8080


def start_server():
    """Start the HTTP server and open browser"""
    # Find an available port
    port = find_available_port()
    
    # Create the server
    handler = WebVisualizer
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"""
=========================================================
   Longest Common Subsequence Visualizer is running!
=========================================================

Server started at http://localhost:{port}/
Opening your web browser...

If the browser doesn't open automatically, please:
1. Open your web browser
2. Go to http://localhost:{port}/

To stop the visualizer, press Ctrl+C in this window.
""")
    
    # Open the browser in a separate thread
    def open_browser():
        time.sleep(1)  # Wait a bit for the server to start
        webbrowser.open(f"http://localhost:{port}/")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run server until interrupted
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Goodbye!")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    start_server()