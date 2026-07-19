import feedparser

class NewsFetcher:
    """Handles parsing RSS feeds to grab the latest tech articles."""
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_latest_article(self) -> dict:
        """Fetches the top article from the RSS feed."""
        print(f"Parsing feed: {self.feed_url}...")
        feed = feedparser.parse(self.feed_url)
        
        if not feed.entries:
            raise Exception("No articles found in the provided RSS feed.")
        
        # Extract the most recent entry
        top_entry = feed.entries[0]
        return {
            "title": top_entry.title,
            "link": top_entry.link,
            "summary": getattr(top_entry, "summary", "No description available.")
        }