from flask import Flask
from flask_frozen import Freezer
from server import app

# Create a new Flask app instance
static_app = Flask(__name__)

# Copy routes from the main app
for rule in app.url_map.iter_rules():
    static_app.add_url_rule(rule.rule, view_func=app.view_functions[rule.endpoint])

# Create freezer
freezer = Freezer(static_app)

if __name__ == '__main__':
    # Build the static site
    freezer.freeze() 