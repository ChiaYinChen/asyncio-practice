"""Sync spider."""
from pprint import pprint
from typing import Dict, List

import requests
from pyquery import PyQuery

from utils import timer


class Spider:
    """Sync spider."""

    def make_request(self, url: str) -> PyQuery:
        """Sync make a request and make http DOM."""
        response = requests.get(url)
        dom = PyQuery(response.text)
        return dom

    def get_links(self, url: str) -> List[str]:
        """Sync get links."""
        links = []
        dom = self.make_request(url)
        items = dom('.category-content [class="item clearfix"] .item-text a').items()  # noqa: E501
        for item in items:
            link = f'https://stars.udn.com{item.attr("href")}'
            links.append(link)
        return links

    def parse_article(self, url: str) -> Dict[str, str]:
        """Sync parse article."""
        dom = self.make_request(url)
        article_title = dom('#story_art_title').text()
        article_time = dom('.shareBar__info--author span').text()
        return {
            'title': article_title,
            'time': article_time,
            'url': url
        }

    def run(self, n: int = 3) -> None:
        """Sync execute task."""
        pagination_url = 'https://stars.udn.com/star/cate/10088/{page}'
        urls = [pagination_url.format(page=page+1) for page in range(n)]
        for url in urls:
            print(f'pagination url: {url}')
            article_links = self.get_links(url)
            for article_link in article_links:
                json_item = self.parse_article(article_link)
                pprint(json_item)


@timer
def main():
    """Execute."""
    spider = Spider()
    spider.run(n=10)


if __name__ == '__main__':
    main()
