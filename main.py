import asyncio

from src.flow import GrabFlow

LOOP = asyncio.get_event_loop()


async def main(url):
    await GrabFlow(url).start()


if __name__ == '__main__':
    LOOP.run_until_complete(main(input("请输入小说地址：")))
