import os
import shutil
import sys
from jinja2 import Environment, FileSystemLoader
from server import app, theaters

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
        shutil.copytree('static', 'static_site/static', dirs_exist_ok=True)
    
    # Copy Media files
    if os.path.exists('Media'):
        print("Copying Media files...")
        shutil.copytree('Media', 'static_site/Media', dirs_exist_ok=True)
    
    # Copy index.html
    if os.path.exists('index.html'):
        print("Copying index.html...")
        shutil.copy2('index.html', 'static_site/')

def generate_static_site():
    """Generate static HTML files from templates"""
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=True
    )
    
    # Add config and url_for to templates
    env.globals['config'] = app.config
    env.globals['url_for'] = lambda endpoint, **kwargs: f"/{endpoint}.html" if endpoint != 'static' else f"/static/{kwargs.get('filename', '')}"
    
    # Generate home page
    print("Generating home page...")
    home_template = env.get_template('home.html')
    featured_ids = ["Metrograph", "Film-Forum", "IFC-Center"]
    popular_theaters = [theaters[t_id] for t_id in featured_ids]
    with open('static_site/home.html', 'w') as f:
        f.write(home_template.render(popular_theaters=popular_theaters))
    
    # Generate theater pages
    print("Generating theater pages...")
    view_template = env.get_template('view.html')
    for theater_id, theater_data in theaters.items():
        print(f"Generating page for {theater_id}...")
        # Get nearby theaters' full data
        nearby_theaters = []
        for nearby_id in theater_data["nearby theater ids"]:
            if nearby_id in theaters:
                nearby_theaters.append(theaters[nearby_id])
        
        # Create directory for theater if it doesn't exist
        theater_dir = os.path.join('static_site', theater_id)
        if not os.path.exists(theater_dir):
            os.makedirs(theater_dir)
        
        # Generate the page
        with open(os.path.join(theater_dir, 'index.html'), 'w') as f:
            f.write(view_template.render(
                theater=theater_data,
                nearby_theaters=nearby_theaters
            ))
    
    # Generate search page
    print("Generating search page...")
    search_template = env.get_template('search.html')
    with open('static_site/search.html', 'w') as f:
        f.write(search_template.render(query="", results=[]))

if __name__ == '__main__':
    try:
        print("Starting static site build...")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        
        # Ensure directories exist
        ensure_directories()
        
        # Copy static files
        copy_static_files()
        
        # Generate static site
        generate_static_site()
        
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
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1) 