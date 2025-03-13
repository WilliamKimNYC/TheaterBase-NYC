from flask import Flask
from flask_frozen import Freezer
from server import app
import os
import sys

# Create a new Flask app instance
static_app = Flask(__name__)

# Copy routes from the main app
for rule in app.url_map.iter_rules():
    static_app.add_url_rule(rule.rule, view_func=app.view_functions[rule.endpoint])

# Create freezer with custom URL generator
freezer = Freezer(static_app)

# Set the base URL for static files
static_app.config['FREEZER_BASE_URL'] = 'https://wnskim.github.io/TheaterBase-NYC/'
static_app.config['FREEZER_DESTINATION'] = 'static_site'

# Ensure static files are copied
@freezer.register_generator
def static_files():
    for root, dirs, files in os.walk('static'):
        for file in files:
            yield {'path': os.path.join(root, file)}

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = ['static_site', 'static_site/static', 'static_site/Media']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

if __name__ == '__main__':
    try:
        # Ensure directories exist
        ensure_directories()
        
        # Build the static site
        freezer.freeze()
        
        # Copy static files
        if os.path.exists('static'):
            os.system('cp -r static/* static_site/static/')
        if os.path.exists('Media'):
            os.system('cp -r Media/* static_site/Media/')
            
        print("Static site built successfully!")
    except Exception as e:
        print(f"Error building static site: {str(e)}", file=sys.stderr)
        sys.exit(1) 