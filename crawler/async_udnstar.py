"""Async spider."""
from pprint import pprint
from typing import Dict, List

import asyncio
from aiohttp import ClientSession
from pyquery import PyQuery

from utils import timer


class Spider:
    """Async spider."""

    async def make_request(self, url: str, session: ClientSession) -> PyQuery:
        """Async make a request and make http DOM."""
        async with session.get(url) as response:
            html_body = await response.text()
            dom = PyQuery(html_body)
            return dom

    async def get_links(self, url: str, session: ClientSession) -> List[str]:
        """Async get links."""
        dom = await self.make_request(url, session)
        links = []
        items = dom('.category-content [class="item clearfix"] .item-text a').items()  # noqa: E501
        for item in items:
            link = f'https://stars.udn.com{item.attr("href")}'
            links.append(link)
        return links

    async def parse_article(self, url: str,
                            session: ClientSession) -> Dict[str, str]:
        """Async parse article."""
        dom = await self.make_request(url, session)
        article_title = dom('#story_art_title').text()
        article_time = dom('.shareBar__info--author span').text()
        return {
            'title': article_title,
            'time': article_time,
            'url': url
        }

    async def do(self, page: int, session: ClientSession) -> None:
        """Async execute task."""
        pagination_url = 'https://stars.udn.com/star/cate/10088/{page}'
        url = pagination_url.format(page=page+1)
        print(f'pagination url: {url}')
        article_links = await self.get_links(
            url=url,
            session=session
        )
        for article_link in article_links:
            json_item = await self.parse_article(article_link, session)
            pprint(json_item)

    async def run(self, n: int = 3) -> None:
        """Execute the following steps:

        1. Create task list.
        2. Use asyncio.gather to run multiple coroutines concurrently.
        """
        async with ClientSession() as session:
            tasks = [asyncio.create_task(self.do(page, session)) for page in range(n)]  # noqa: E501
            await asyncio.gather(*tasks)


@timer
def main():
    """Execute."""
    spider = Spider()
    asyncio.run(spider.run(n=10))


if __name__ == '__main__':
    main()
