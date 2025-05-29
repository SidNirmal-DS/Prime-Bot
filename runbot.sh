#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_APP=webapp/app.py
export FLASK_ENV=development
export PYTHONPATH=$(pwd)

# Run the Flask app
flask run