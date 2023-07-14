import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url, domain):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and parsed.netloc == domain

def is_telephone_link(url):
    return url.startswith("tel:")

def is_email_link(url):
    return url.startswith("mailto:")

def scan_website(url, domain):
    visited = set()
    broken_links = set()

    def process_page(url):
        if url in visited:
            print("Already visited:", url)
            return
        visited.add(url)
        print("Scanning:", url)

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            broken_links.add(url)
            return

        if response.status_code != 200:
            print("Broken link:", url)
            broken_links.add(url)
            return

        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                absolute_url = urljoin(url, href)
                if is_valid_url(absolute_url, domain) and not is_telephone_link(absolute_url) and not is_email_link(absolute_url):
                    process_page(absolute_url)

    process_page(url)

    return broken_links

# Usage example
website_url = "https://www.my100bank.com/"
target_domain = "my100bank.com"
broken_links = scan_website(website_url, target_domain)
print("Broken links:", len(broken_links))
for link in broken_links:
    print(link)

