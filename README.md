# Dark Web Crawler

## 📌 Overview
This **Dark Web Crawler** securely connects to the **Tor network** and scrapes **.onion** websites while indexing them into an SQLite database. It supports **recursive crawling**, **search functionality**, and follows ethical guidelines for responsible research.

## 🚀 Features
✔ **Crawls .onion sites securely via Tor**  
✔ **Indexes site titles, URLs, and depth into an SQLite database**  
✔ **Supports recursive crawling up to a specified depth**  
✔ **Allows searching for indexed sites by keywords**  
✔ **Ensures anonymity via Tor's SOCKS5 proxy**  

## 📦 Installation
### **1️⃣ Install Dependencies**
```bash
pip install requests beautifulsoup4 stem pysocks sqlite3
```

### **2️⃣ Install & Start Tor**
- **Linux/macOS**:
  ```bash
  sudo apt install tor  # Ubuntu/Debian
  brew install tor      # macOS (Homebrew)
  sudo service tor start
  ```
- **Windows**:
  - Download & install **Tor Expert Bundle** from [torproject.org](https://www.torproject.org/)
  - Start `tor.exe`

## 🛠 Usage
### **Run the script**
```bash
python dark_web_crawler.py
```

### **Provide Input**
1. **Choose Mode**:
   - `1` → Crawl a .onion site
   - `2` → Search indexed sites
2. **For Crawling**:
   - Enter a `.onion` URL (e.g., `http://example.onion`)
   - The crawler will extract links & store them in `dark_web_index.db`
3. **For Searching**:
   - Enter a keyword (e.g., `market`)
   - Displays matching results from the database

### **Example Output**
```
Choose mode: 1. Crawl a site, 2. Search indexed sites: 1
Enter .onion URL to start crawling: http://example.onion
[+] Successfully accessed: http://example.onion
Page Title: Hidden Market
[+] Found 5 links.
```

## 🛡️ Ethical Guidelines
- **Only crawl sites you have permission to access**.
- **Use this tool responsibly for research & security awareness**.
- **Do NOT engage in illegal activities or data scraping without consent**.

## ⚠️ Disclaimer
This tool is for **educational and ethical cybersecurity research only**. Unauthorized access to systems is **illegal**. Always ensure you have **explicit permission** before using it.

🔒 **Stay ethical and secure!**

