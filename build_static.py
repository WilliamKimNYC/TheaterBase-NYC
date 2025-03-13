from flask import Flask, url_for
from flask_frozen import Freezer
from server import app
import os
import sys
import shutil
import traceback

# Create a new Flask app instance
static_app = Flask(__name__)

# Copy configuration from main app
static_app.config.update(app.config)

# Copy routes from the main app
print("Copying routes from main app...")
for rule in app.url_map.iter_rules():
    print(f"Adding route: {rule.rule}")
    static_app.add_url_rule(rule.rule, view_func=app.view_functions[rule.endpoint])

# Create freezer with custom URL generator
freezer = Freezer(static_app)

# Set the base URL for static files
static_app.config['FREEZER_BASE_URL'] = 'https://wnskim.github.io/TheaterBase-NYC/'
static_app.config['FREEZER_DESTINATION'] = 'static_site'
static_app.config['FREEZER_RELATIVE_URLS'] = True

def ensure_directories():
    """Ensure all necessary directories exist"""
    print("\nEnsuring directories exist...")
    directories = ['static_site', 'static_site/static', 'static_site/Media']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")

def copy_static_files():
    """Copy static files to the build directory"""
    print("\nCopying static files...")
    # Copy static files
    if os.path.exists('static'):
        print("Copying static directory...")
        for item in os.listdir('static'):
            s = os.path.join('static', item)
            d = os.path.join('static_site/static', item)
            try:
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                    print(f"Copied file: {item}")
                elif os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                    print(f"Copied directory: {item}")
            except Exception as e:
                print(f"Error copying {item}: {str(e)}")
    else:
        print("Warning: static directory not found")
    
    # Copy Media files
    if os.path.exists('Media'):
        print("\nCopying Media directory...")
        for item in os.listdir('Media'):
            s = os.path.join('Media', item)
            d = os.path.join('static_site/Media', item)
            try:
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                    print(f"Copied file: {item}")
                elif os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                    print(f"Copied directory: {item}")
            except Exception as e:
                print(f"Error copying {item}: {str(e)}")
    else:
        print("Warning: Media directory not found")
    
    # Copy index.html
    if os.path.exists('index.html'):
        print("\nCopying index.html...")
        try:
            shutil.copy2('index.html', 'static_site/')
            print("Copied index.html successfully")
        except Exception as e:
            print(f"Error copying index.html: {str(e)}")
    else:
        print("Warning: index.html not found")

def update_urls():
    """Update URLs in the theater data to use relative paths"""
    print("\nUpdating URLs...")
    for theater_id, theater_data in app.config['theaters'].items():
        print(f"Processing theater: {theater_id}")
        if theater_data.get('banner'):
            theater_data['banner'] = theater_data['banner'].replace('https://wnskim.github.io/TheaterBase-NYC/', '/')
            print(f"Updated banner URL for {theater_id}")
        if theater_data.get('image'):
            theater_data['image'] = theater_data['image'].replace('https://wnskim.github.io/TheaterBase-NYC/', '/')
            print(f"Updated image URL for {theater_id}")

if __name__ == '__main__':
    try:
        print("Starting static site build...")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        
        # Ensure directories exist
        ensure_directories()
        
        # Update URLs to use relative paths
        update_urls()
        
        # Copy static files first
        copy_static_files()
        
        print("\nBuilding static site...")
        # Build the static site
        freezer.freeze()
        
        print("\nStatic site built successfully!")
        print("\nContents of static_site directory:")
        for root, dirs, files in os.walk('static_site'):
            level = root.replace('static_site', '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")
                
    except Exception as e:
        print(f"\nError building static site: {str(e)}", file=sys.stderr)
        print("\nFull traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1) 