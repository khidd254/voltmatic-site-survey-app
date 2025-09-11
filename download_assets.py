"""
Download assets from Voltmatic Energy Solutions website
"""
import os
import requests
from urllib.parse import urlparse

def download_image(url, filename):
    """Download image from URL and save to assets folder"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    """Download all company assets"""
    
    # Company logo and branding
    assets = {
        'logo.png': 'https://voltmaticenergysolutions.co.ke/wp-content/uploads/2022/01/VES-Logo-Variation-Transparent.png',
        'logo_small.png': 'https://voltmaticenergysolutions.co.ke/wp-content/uploads/2022/01/VES-Logo-Variation-Transparent-300x113.png'
    }
    
    # Download assets
    for filename, url in assets.items():
        filepath = os.path.join('assets', 'images', filename)
        download_image(url, filepath)
    
    print("Asset download completed!")

if __name__ == '__main__':
    main()
