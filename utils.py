import asyncio
import re
from lxml import html as HTML
from bs4 import BeautifulSoup


def remove_tags(html_string, tag_list):
    soup = BeautifulSoup(html_string, 'html.parser')
    all_tags = soup.find_all()
    for tag in all_tags:
        if tag.name not in tag_list:
            tag.decompose()
    clean_html = str(soup)
    return clean_html


def trans_element_to_string(ele) -> str:
    result = HTML.tostring(ele, encoding="unicode", method="html")
    return result


def extract_text_from_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text.strip()


def extract_text_from_ele(ele):
    soup = BeautifulSoup(trans_element_to_string(ele), 'html.parser')
    text = soup.get_text()
    return text.strip()


def remove_links(text):
    pattern = r'https?://\S+'
    return re.sub(pattern, '', text)


async def run_parallel_with_sem(async_func_list: list = None, sem_count=5, rate: float = None):
    """
    同时运行异步方法，并且限制并发数，例如sem_count=3，rate=1，表示一秒钟三个任务并发运行
    Args:
        sem_count: 并发的数量
        async_func_list: 异步方法列表
        rate: 速率，单位为秒（s）

    Returns: 结果list，与传入的coroutine顺序一致

    """
    if not async_func_list:
        return []
    sem = asyncio.Semaphore(sem_count)
    tasks = []
    for af in async_func_list:
        tasks.append(asyncio.ensure_future(_run_parallel(af, sem, rate)))
    return await asyncio.gather(*tasks)


async def _run_parallel(cro_func, sem, rate):
    async with sem:
        if rate is not None:
            nxt = asyncio.sleep(rate)
            res = await cro_func
            await nxt
            return res
        return await cro_func
