from src.loop import LOOP
from src.flow import GrabFlow


async def main(url):
    await GrabFlow(url).start()


if __name__ == '__main__':
    LOOP.run_until_complete(main(input("请输入小说地址：")))
