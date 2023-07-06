import asyncio

from spider import FictionSpider

LOOP = asyncio.get_event_loop()


async def main(url):
    spider = FictionSpider(url)
    await spider.run()


if __name__ == '__main__':
    LOOP.run_until_complete(main(input("请输入小说地址：")))
