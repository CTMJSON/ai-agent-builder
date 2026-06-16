import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from urllib.parse import urljoin, urlparse
from typing import List, Dict

class SmartCrawler:
    def __init__(self):
        self.browser_config = BrowserConfig(
            headless=True,
            verbose=False,
        )
        self.run_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
        )

    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        parsed = urlparse(url)
        if not parsed.scheme.startswith('http'):
            return False
        if parsed.netloc and parsed.netloc != base_domain:
            return False
        return True

    def _extract_key_pages(self, links: List, base_url: str) -> List[str]:
        base_domain = urlparse(base_url).netloc
        keywords = ['about', 'contact', 'faq', 'services', 'products', 'help', 'support']
        
        key_pages = set([base_url])
        
        for link_obj in links:
            link_url = link_obj.get('href', '') if isinstance(link_obj, dict) else str(link_obj)
            if not self._is_valid_url(link_url, base_domain):
                continue
            
            link_lower = link_url.lower()
            for keyword in keywords:
                if keyword in link_lower:
                    key_pages.add(link_url)
                    break
        
        return list(key_pages)[:10]

    async def crawl_site(self, url: str) -> Dict[str, str]:
        results = {}
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            homepage_result = await crawler.arun(url=url, config=self.run_config)
            
            if homepage_result and homepage_result.markdown:
                results[url] = str(homepage_result.markdown)
                
                links = homepage_result.links.get('internal', [])
                key_pages = self._extract_key_pages(links, url)
                
                for page_url in key_pages:
                    if page_url == url:
                        continue
                    
                    try:
                        page_result = await crawler.arun(url=page_url, config=self.run_config)
                        if page_result and page_result.markdown:
                            results[page_url] = str(page_result.markdown)
                    except Exception as e:
                        print(f"Error crawling {page_url}: {e}")
                        continue
        
        return results

def crawl_website(url: str) -> Dict[str, str]:
    crawler = SmartCrawler()
    return asyncio.run(crawler.crawl_site(url))
