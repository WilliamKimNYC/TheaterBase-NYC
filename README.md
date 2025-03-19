# TheaterBase-NYC

A comprehensive guide to independent and art-house theaters in New York City.

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TheaterBase-NYC.git
cd TheaterBase-NYC
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys and secret key
```

5. Run the development server:
```bash
python server.py
```

The site will be available at http://localhost:5001

## Deployment

This project is automatically deployed to GitHub Pages when changes are pushed to the main branch.

### Setting up GitHub Pages

1. Go to your repository settings
2. Navigate to Settings > Pages
3. Under "Source", select "GitHub Actions"

### Environment Variables

The following environment variables need to be set in your GitHub repository:

1. Go to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `GOOGLE_MAPS_API_KEY`: Your Google Maps API key
   - `SECRET_KEY`: A secure random string for Flask

## Features

- Comprehensive list of independent and art-house theaters in NYC
- Detailed theater information including:
  - Ticket prices
  - Student discounts
  - Types of movies shown
  - Nearby theaters
  - Website links
- Search functionality
- Responsive design