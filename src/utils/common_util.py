import asyncio
import re
import os
import datetime
from urllib.parse import urlparse


def extract_host(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    return host


def replace_invalid_chars(filename: str):
    filename = filename.strip()
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        filename = re.sub(re.escape(char), '', filename)
    return filename


async def batch_run_tasks(task_list, batch_size: int = 20):
    for i in range(0, len(task_list), batch_size):
        temp_task_list = task_list[i:i + batch_size]
        temp_res_list = await asyncio.gather(*temp_task_list)
        yield temp_res_list


def get_formatted_time(format_str="%Y-%m-%d %H:%M:%S"):
    now = datetime.datetime.now()
    formatted_time = now.strftime(format_str)
    return formatted_time


def get_unique_file_path(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    counter = 1
    numbered_file_path = file_path
    while os.path.exists(numbered_file_path):
        numbered_file_path = f"{file_name}_{counter:02d}{file_extension}"
        counter += 1
    return numbered_file_path


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


path_join = os.path.join

os_makedirs = os.makedirs

async_run = asyncio.get_event_loop().run_until_complete
