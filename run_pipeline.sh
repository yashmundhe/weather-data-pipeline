#!/bin/bash

# Navigate to project directory
cd /Users/yashmundhe/Documents/DE_Projects/Weather\ Pipeline

# Activate virtual environment
source venv/bin/activate

# Run the pipeline
python3 src/extract.py

# Log completion time
echo "Pipeline completed at $(date)" >> logs/cron.log