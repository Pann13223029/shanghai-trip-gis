#!/bin/bash
# Start a local web server for development
# Open http://localhost:8000/web/index.html in your browser
echo "Starting local server..."
echo "Open: http://localhost:8000/web/index.html"
echo "Press Ctrl+C to stop"
python3 -m http.server 8000
