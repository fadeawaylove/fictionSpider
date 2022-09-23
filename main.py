import asyncio

from spider import FictionSpider

LOOP = asyncio.get_event_loop()


async def main(url):
    spider = FictionSpider(url)
    await spider.run()


if __name__ == '__main__':
    LOOP.run_until_complete(main("https://www.777zw.net/0/230/"))
