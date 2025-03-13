from flask import Flask, url_for
from flask_frozen import Freezer
from server import app
import os
import sys
import shutil

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

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = ['static_site', 'static_site/static', 'static_site/Media']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def copy_static_files():
    """Copy static files to the build directory"""
    # Copy static files
    if os.path.exists('static'):
        print("Copying static files...")
        for item in os.listdir('static'):
            s = os.path.join('static', item)
            d = os.path.join('static_site/static', item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d)
    
    # Copy Media files
    if os.path.exists('Media'):
        print("Copying Media files...")
        for item in os.listdir('Media'):
            s = os.path.join('Media', item)
            d = os.path.join('static_site/Media', item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d)

if __name__ == '__main__':
    try:
        print("Starting static site build...")
        
        # Ensure directories exist
        ensure_directories()
        
        # Copy static files first
        copy_static_files()
        
        print("Building static site...")
        # Build the static site
        freezer.freeze()
        
        print("Static site built successfully!")
        print("\nContents of static_site directory:")
        for root, dirs, files in os.walk('static_site'):
            level = root.replace('static_site', '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")
                
    except Exception as e:
        print(f"Error building static site: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1) 