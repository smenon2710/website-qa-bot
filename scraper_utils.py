# scraper_utils.py
import subprocess
import os

def scrape_url_with_playwright(url: str, output_file: str) -> str:
    print(f"🕷️ Crawling with Playwright: {url}")
    
    # Run the Node script with the URL
    result = subprocess.run(
        ["node", "run_playwright.js", url, output_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"❌ Scraper failed:\n{result.stderr}")
    
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"❌ Expected markdown not found at: {output_file}")
    
    with open(output_file, "r") as f:
        return f.read()