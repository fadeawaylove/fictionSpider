import asyncio
import datetime
import os
import re
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup
from ebooklib import epub
from lxml import etree, html as HTML
from tqdm import tqdm

from config import SOURCE_LIST
from http_client import HttpClient
from utils import remove_tags, remove_links, run_parallel_with_sem, extract_text_from_html, trans_element_to_string, \
    extract_text_from_ele

LOOP = asyncio.get_event_loop()


def get_formatted_time(format_str="%Y-%m-%d %H:%M:%S"):
    now = datetime.datetime.now()
    formatted_time = now.strftime(format_str)
    return formatted_time


async def batch_run_tasks(task_list, call_back=None, batch_size: int = 20):
    for i in range(0, len(task_list), batch_size):
        temp_task_list = task_list[i:i + batch_size]
        temp_res_list = await asyncio.gather(*temp_task_list)
        if call_back:
            for res in temp_res_list:
                call_back(res)


def replace_invalid_chars(filename: str):
    # 定义要替换的字符列表
    filename = filename.strip()
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    # 循环遍历要替换的字符列表，并替换文件名中的每个字符
    for char in invalid_chars:
        filename = re.sub(re.escape(char), ' ', filename)

    # 返回替换后的文件名
    return filename


def get_source_model(url: str):
    for m in SOURCE_LIST:
        if url.startswith(m.home):
            return m


class FictionSpider:

    def __init__(self, base_url: str, output_name="", is_test=False, test_cnt=5):

        self.source_model = get_source_model(base_url)
        if not self.source_model:
            raise Exception("无法解析此书源，请添先添加配置规则！")

        parsed_url = urlsplit(base_url)
        self.pbar = None
        self.base_url = base_url
        self.host = parsed_url.scheme + "://" + parsed_url.netloc
        self.sem_count = self.source_model.rate_count
        self.name = output_name
        self.is_test = is_test
        self.test_cnt = test_cnt
        self.epub_book = epub.EpubBook()
        self.chapter_name_set = set()
        self.cover_img_path = "cover.jpg"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
            **self.source_model.ext_headers
        }

    def set_title(self, html):
        """尝试获取小说名（标题）"""
        if self.name:
            return
        title = html.xpath(self.source_model.title_xpath)
        for t in title:
            if t.text:
                self.name = t.text.strip()
                self.epub_book.set_title(self.name)
                break
        if not self.name:
            raise Exception("获取小说名失败")

    async def set_cover(self, html):
        """尝试获取封面"""
        cover_url = html.xpath(self.source_model.cover_xpath)
        if not cover_url:
            raise Exception("获取封面失败")
        cover_url = cover_url[0]
        if not cover_url.startswith("http"):
            cover_url = urljoin(self.base_url, cover_url)

        # 设置封面
        cover_content = await HttpClient.get(cover_url, headers=self.headers, return_type="raw")
        self.epub_book.set_cover(self.cover_img_path, cover_content)

    def add_chapter(self, chapter_name, chapter_content):
        xhtml_name = f'{chapter_name}.xhtml'
        chapter = epub.EpubHtml(title=chapter_name, file_name=xhtml_name, lang='en')
        chapter.content = chapter_content
        self.epub_book.add_item(chapter)
        self.epub_book.spine.append(chapter)
        self.epub_book.toc.append(epub.Link(xhtml_name, chapter_name, chapter_name))

    def set_intro(self, html):
        """设置介绍页"""
        intro_img_str = f'''
        <div style="text-align: center;">
            <img src="{self.cover_img_path}" style="display: inline-block;"/>
        </div>
        '''
        intro_text = ""
        intro_source_str = f'''
        <div style="text-align: center;">
            <a href="{self.base_url}" style="display: inline-block;">来源：{self.base_url}</a>
        </div>
        '''
        intro_xpath = self.source_model.intro_xpath
        if intro_xpath:
            intro_ele = html.xpath(intro_xpath)
            if intro_ele:
                intro_ele = intro_ele[0]
                intro_text = trans_element_to_string(intro_ele)

        intro_str = intro_img_str + intro_text + intro_source_str
        self.add_chapter("简介", intro_str)

    def set_author(self, html):
        if not (author_xpath := self.source_model.author_xpath):
            return
        if not (author := html.xpath(author_xpath)):
            return
        author_ele = author[0]
        if author_text := extract_text_from_ele(author_ele):
            author_text = author_text.split("：")[-1]
            self.epub_book.add_author(author_text)

    async def get_chapter_list_html(self, url=None):
        u = url or self.base_url
        if not u.startswith("http"):
            u = urljoin(self.base_url, u)
        content = await HttpClient.get(u, headers=self.headers, return_type="raw")
        return HTML.fromstring(content)

    async def get_chapter_list(self, first_html):
        html_list = [first_html]
        if self.source_model.all_page_xpath:
            all_page_url_list = first_html.xpath(self.source_model.all_page_xpath)
            tasks = [self.get_chapter_list_html(x) for x in all_page_url_list]
            temp_list = await run_parallel_with_sem(tasks, sem_count=self.sem_count)
            html_list += temp_list

        result = []
        for html in html_list:
            chapter_xpath = self.source_model.list_xpath
            if not chapter_xpath:
                print(f"不支持：{self.host}")
                return False
            chapter_list = html.xpath(chapter_xpath)
            chapter_list = [(chapter.text.strip(), urljoin(self.base_url, chapter.get("href")))
                            for chapter in chapter_list]
            result += chapter_list
        return result

    async def get_chapter_content(self, chapter_url: str) -> str:
        """获取章节的页面内容"""
        resp_content = await HttpClient.get(chapter_url, headers=self.headers, return_type="raw")
        html = etree.HTML(resp_content)
        content_ele = html.xpath(self.source_model.content_xpath)[0]
        content_str = trans_element_to_string(content_ele)
        content_str = self._process_replace_string(content_str)
        content_str = self._process_include_tags(content_str)
        content_str = self._process_include_links(content_str)
        return content_str

    def _process_replace_string(self, content_str: str):
        for replace_string in self.source_model.replace_string_list:
            content_str = content_str.replace(replace_string, "")
        return content_str

    def _process_include_tags(self, content_str: str):
        return remove_tags(content_str, self.source_model.include_tag_list)

    @staticmethod
    def _process_include_links(content_str: str):
        return remove_links(content_str)

    @staticmethod
    def get_unique_file_path(file_path):
        file_name, file_extension = os.path.splitext(file_path)
        counter = 1
        numbered_file_path = file_path
        while os.path.exists(numbered_file_path):
            numbered_file_path = f"{file_name}_{counter:02d}{file_extension}"
            counter += 1
        return numbered_file_path

    async def get_one_chapter_info(self, chapter_name, chapter_url):
        if chapter_name in self.chapter_name_set:
            return False, chapter_name, "重复章节"
        self.chapter_name_set.add(chapter_name)
        chapter_content = await self.get_chapter_content(chapter_url)
        if self.source_model.begin_title:
            chapter_content = f"<h2>{chapter_name}</h2>" + chapter_content
        return True, chapter_name, chapter_content

    def add_chapter_to_book(self, args):
        flag, chapter_name, chapter_content = args
        if not flag:
            self.pbar.set_postfix_str(f"跳过【{chapter_name}】，原因{chapter_content}")
            self.pbar.update(1)
            return

        self.add_chapter(chapter_name, chapter_content)
        self.pbar.set_postfix_str(f"写入【{chapter_name}】，长度{len(chapter_content)}")
        self.pbar.update(1)

    async def run(self):
        html = await self.get_chapter_list_html()

        await self.set_cover(html)
        self.set_title(html)
        self.set_intro(html)
        self.set_author(html)

        chapter_list = await self.get_chapter_list(html)
        if not chapter_list:
            print("未获取到任何章节！")
            return
        file_name = self.name
        if self.is_test:
            file_name += f"_测试"
            chapter_list = chapter_list[:self.test_cnt]
        chapter_cnt = len(chapter_list)

        self.pbar = tqdm(total=chapter_cnt, postfix=f"开始采集《{file_name}》", unit="章", desc=f"采集《{file_name}》")

        chapter_tasks = [self.get_one_chapter_info(*chapter) for chapter in chapter_list]
        await batch_run_tasks(chapter_tasks, call_back=self.add_chapter_to_book, batch_size=self.sem_count)

        self.epub_book.add_item(epub.EpubNcx())
        self.epub_book.add_item(epub.EpubNav())

        dir_name = os.path.join("epubs", get_formatted_time("%Y-%m-%d"))
        os.makedirs(dir_name, exist_ok=True)
        file_name = file_name + f"_{self.source_model.name}" + ".epub"
        out_name = self.get_unique_file_path(os.path.join(dir_name, file_name))
        self.pbar.set_postfix_str(f"合成文件：{out_name}")
        epub.write_epub(out_name, self.epub_book, {})
