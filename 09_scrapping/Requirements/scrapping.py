#!/usr/bin/env python3
import requests
import re
from typing import Optional
from urllib.parse import urljoin
import time

class URLCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.found: Optional[str] = None
        self.total = 18279
        self.current = 0
        self.session = requests.Session()
        self.session.timeout = 2  # Reduced timeout

    def check_for_flag(self, content: str) -> Optional[str]:
        """Check for flag in the specific format we know exists."""
        match = re.search(r'flag : ([a-f0-9]{64})', content)
        if match:
            return match.group(1)
        return None

    def search_flag(self, url: str, check_flag: bool = False) -> None:
        """
        Recursively search through URL structure for a flag.
        """
        if self.found:
            return

        try:
            response = self.session.get(url)
            content = response.text

            if check_flag:
                flag = self.check_for_flag(content)
                if flag:
                    self.found = flag
                    return
                self.current += 1
                progress = (self.current * 100) // self.total
                print(f"Current progress : {progress}%", end='\r', flush=True)
                return

            links = re.findall(r'href="([^"./][^"]*)"', content)

            for link in links:
                if link == "README":
                    next_url = urljoin(url, link)
                    self.search_flag(next_url, True)
                else:
                    next_url = urljoin(url, link + '/')
                    self.search_flag(next_url)

        except requests.RequestException:
            # Silently retry after a short delay
            time.sleep(0.1)
            try:
                self.search_flag(url, check_flag)
            except:
                pass

def main():
    base_url = "http://192.168.56.102/.hidden/"
    crawler = URLCrawler(base_url)

    try:
        crawler.search_flag(base_url)
        print("\nTHE FLAG IS :", crawler.found if crawler.found else "Not found")
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user")

if __name__ == "__main__":
    main()