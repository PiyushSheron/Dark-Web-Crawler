import requests
from bs4 import BeautifulSoup
import socks
import socket
import stem.process
from stem.control import Controller
import time
import sqlite3
from urllib.parse import urljoin

# Database setup
def init_db():
    conn = sqlite3.connect("dark_web_index.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indexed_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            depth INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Save crawled site to database
def save_to_db(url, title, depth):
    conn = sqlite3.connect("dark_web_index.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO indexed_sites (url, title, depth) VALUES (?, ?, ?)", (url, title, depth))
    conn.commit()
    conn.close()

# Search indexed sites
def search_indexed_sites(keyword):
    conn = sqlite3.connect("dark_web_index.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, title FROM indexed_sites WHERE title LIKE ? OR url LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print("[+] Search Results:")
        for url, title in results:
            print(f"Title: {title}, URL: {url}")
    else:
        print("[-] No matching results found.")

# Tor Proxy Configuration
def start_tor_proxy():
    """Start a Tor connection and configure it for requests."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")  # Set your Tor password
        controller.signal(stem.Signal.NEWNYM)
        
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

# Function to crawl an .onion site and index links
def crawl_onion_site(url, visited_urls, depth=1, max_depth=2):
    """Recursively crawl and extract links from an .onion site and save to a database."""
    if depth > max_depth or url in visited_urls:
        return
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            print(f"[+] Successfully accessed ({depth}/{max_depth}): {url}")
            print("Page Title:", title)
            
            visited_urls.add(url)
            save_to_db(url, title, depth)
            
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].startswith('http') or a['href'].startswith('/')]
            print(f"[+] Found {len(links)} links.")
            
            for link in links:
                crawl_onion_site(link, visited_urls, depth + 1, max_depth)
                time.sleep(2)  # Delay to prevent overload
        else:
            print(f"[-] Failed to access site {url}. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error accessing site {url}: {e}")

if __name__ == "__main__":
    init_db()
    start_tor_proxy()
    choice = input("Choose mode: 1. Crawl a site, 2. Search indexed sites: ")
    
    if choice == "1":
        onion_url = input("Enter .onion URL to start crawling: ")
        visited_urls = set()
        crawl_onion_site(onion_url, visited_urls)
    elif choice == "2":
        keyword = input("Enter keyword to search: ")
        search_indexed_sites(keyword)
    else:
        print("[-] Invalid option. Exiting.")
