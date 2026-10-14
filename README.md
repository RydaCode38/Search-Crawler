# Best Simple Search Crawler

A clean and effective Python web search crawler.  
Enter any query and it searches the web, returns the best results, and optionally crawls the top pages to extract their main content.

## Features

- Search the web using **DuckDuckGo** (reliable and less aggressive blocking than Google)
- Displays clean results with:
  - Title
  - URL
  - Snippet
- Optional deep crawl of the top results (extracts readable main text)
- Polite crawling behavior (realistic User-Agent + delay between requests)
- No API keys required
- Simple interactive mode – keep searching until you type `exit`

## Requirements

- Python 3.8+
- Packages:
  ```bash
  pip install duckduckgo-search requests beautifulsoup4 lxml
