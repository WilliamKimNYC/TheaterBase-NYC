from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from flask_frozen import Freezer
from dotenv import load_dotenv
import os
import json
import sys
import pathlib

# Add the parent directory to Python path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

# Import the Flask app from server.py
from server import app

# Load environment variables - only in development
if os.path.exists('.env'):
    load_dotenv()

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('GOOGLE_MAPS_API_KEY', '')

# This is required for Vercel
app.config['TEMPLATES_AUTO_RELOAD'] = True 