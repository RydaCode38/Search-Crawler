#!/usr/bin/env python3
"""
Bester einfacher Such-Crawler
Eingabe → Suche → Top Ergebnisse (+ optional Seiten-Inhalt)
"""

from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import textwrap

# ============================================
# Einstellungen
# ============================================
MAX_RESULTS = 10          # Wie viele Suchergebnisse
CRAWL_PAGES = True        # True = gefundene Seiten auch kurz crawlen
MAX_CRAWL = 5             # Maximal so viele Seiten crawlen
REQUEST_DELAY = 1.5       # Sekunden Pause zwischen Requests
TIMEOUT = 10              # Timeout pro Seite


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def search_web(query: str, max_results: int = MAX_RESULTS):
    """Sucht mit DuckDuckGo und gibt saubere Ergebnisse zurück"""
    print(f"\nSuche nach: '{query}' ...\n")
    
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "url": r.get("href"),
                "snippet": r.get("body")
            })
    return results


def extract_text_from_url(url: str) -> str:
    """Crawlt eine Seite und extrahiert den Haupttext"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Unnötige Elemente entfernen
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        
        # Text holen
        text = soup.get_text(separator=" ", strip=True)
        
        # Auf sinnvolle Länge kürzen
        text = " ".join(text.split())
        return text[:2500] + "..." if len(text) > 2500 else text
    
    except Exception as e:
        return f"[Fehler beim Crawlen: {e}]"


def print_results(results: list):
    """Schöne Ausgabe der Suchergebnisse"""
    if not results:
        print("Keine Ergebnisse gefunden.")
        return
    
    for i, r in enumerate(results, 1):
        print("=" * 80)
        print(f"{i}. {r['title']}")
        print(f"   URL: {r['url']}")
        print(f"   Snippet: {r['snippet']}")
        
        if CRAWL_PAGES and i <= MAX_CRAWL:
            print("\n   → Crawle Seite...")
            time.sleep(REQUEST_DELAY)
            content = extract_text_from_url(r['url'])
            print("\n   Extrahierter Inhalt:")
            print(textwrap.fill(content, width=90, initial_indent="   ", subsequent_indent="   "))
        
        print()


def main():
    print("=" * 60)
    print("  BESTER EINFACHER SUCH-CRAWLER")
    print("=" * 60)
    
    while True:
        query = input("\nWas möchtest du suchen? (oder 'exit' zum Beenden): ").strip()
        
        if query.lower() in ["exit", "quit", "q"]:
            print("\nTschüss!")
            break
        
        if not query:
            continue
        
        try:
            results = search_web(query)
            print_results(results)
        except Exception as e:
            print(f"\nFehler bei der Suche: {e}")
            print("Tipp: Internet prüfen oder später nochmal versuchen.")


if __name__ == "__main__":
    main()