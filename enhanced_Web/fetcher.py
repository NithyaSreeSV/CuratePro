import requests
from bs4 import BeautifulSoup

class UniversalWebFetcher:
    """Scrapes content from static HTML sites and JavaScript/React SPAs via SEO metadata."""
    def __init__(self, url: str):
        self.url = url
        # Define modern user headers to prevent websites from blocking requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

    def fetch_web_content(self) -> dict:
        print(f"Scraping web page: {self.url}...")
        response = requests.get(self.url, headers=self.headers, timeout=10)
        
        if response.status_code != 200:
            raise Exception(f"Failed to access site. Status code: {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Grab Title
        title = soup.title.string if soup.title else "Shared Article"
        
        # 2. Extract Data (Works for React apps by targeting metadata fields)
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        tw_desc = soup.find("meta", attrs={"name": "twitter:description"})
        main_paragraphs = soup.find_all("p")
        
        # Priority mapping: OpenGraph -> Twitter -> Raw Paragraph extraction
        if og_desc and og_desc.get("content"):
            context = og_desc["content"]
        elif tw_desc and tw_desc.get("content"):
            context = tw_desc["content"]
        elif main_paragraphs:
            # Combine the first few body text elements for static HTML sites
            context = " ".join([p.text for p in main_paragraphs[:3]])
        else:
            context = "No accessible textual body or metadata found."
            
        return {
            "title": title.strip(),
            "link": self.url,
            "summary": context.strip()
        }
