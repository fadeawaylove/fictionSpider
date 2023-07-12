from typing import AsyncIterable

from tqdm import tqdm

from src.models import ChapterContentModel, ChapterListModel, BookInfoModel
from src.parser import get_html_parser
from src.settings import SAVE_PATH
from src.utils import http_client, EpubHelper, batch_run_tasks, get_formatted_time, path_join, \
    get_unique_file_path, os_makedirs, run_parallel_with_sem


class GrabFlow:

    def __init__(self, url: str, is_test=False):
        self.url = url
        self.parser = get_html_parser(url)
        self.is_test = is_test
        self.book = EpubHelper()
        self.cover_path = "cover.jpg"

    async def _get_chapter_content_next_page(self, cm):
        content = await http_client.get(cm.next_page)
        content_model = self.parser.parse_chapter_text(content, cm.name, add_title=False)
        return content_model

    async def _get_chapter_content(self, list_model: ChapterListModel) -> ChapterContentModel:
        content = await http_client.get(list_model.cha_url)
        content_model = self.parser.parse_chapter_text(content, list_model.cha_name)

        next_page = content_model.next_page
        while next_page:
            next_content_model = await self._get_chapter_content_next_page(content_model)
            content_model.content += next_content_model.content
            next_page = next_content_model.next_page

        return content_model

    async def _get_chapter_list(self, book_info: BookInfoModel) -> AsyncIterable[ChapterContentModel]:
        cha_content_task = [self._get_chapter_content(cha) for cha in book_info.cha_list]
        async for content_model_list in batch_run_tasks(cha_content_task):
            for content_model in content_model_list:
                yield content_model

    async def _get_book_info(self, page_url=None) -> BookInfoModel:
        page_content = await http_client.get(page_url or self.url)
        return self.parser.parse_book_info(page_content)

    @staticmethod
    def _get_save_path(name):
        p = path_join(SAVE_PATH, get_formatted_time("%Y-%m-%d"))
        os_makedirs(p, exist_ok=True)
        return get_unique_file_path(path_join(p, name + ".epub"))

    def _format_book_intro(self, book_info: BookInfoModel):
        return f"""
        <div style="text-indent: 2em;">
        <img src="{self.cover_path}" style="width: 80%; display: block; margin: 0 auto;">
        <p>{book_info.intro}</p>
        <a href="{self.url}">{self.url}</a>
        </div>
        """

    async def start(self):
        book_info = await self._get_book_info()
        if self.is_test:
            print(book_info)

        if book_info.url_list and not self.is_test:
            tasks = [http_client.get(u) for u in book_info.url_list]
            res = await run_parallel_with_sem(tasks)
            for r in res:
                ch_lst = self.parser.parse_chapter_list(r)
                book_info.cha_list.extend(ch_lst)

        if self.is_test:
            book_info.cha_list = book_info.cha_list[:5]

        self.book.set_title(book_info.name)
        self.book.add_author(book_info.author)
        cover_content = await http_client.get(book_info.cover)
        self.book.set_cover(self.cover_path, content=cover_content)
        self.book.add_chapter("简介", self._format_book_intro(book_info))

        pbar = tqdm(total=len(book_info.cha_list), postfix=f"开始采集《{book_info.name}》", unit="章",
                    desc=f"采集《{book_info.name}》")

        async for cha_model in self._get_chapter_list(book_info):
            self.book.add_chapter(cha_model.name, cha_model.content)
            pbar.set_postfix_str(f"写入【{cha_model.name}】，字数{len(cha_model.content)}")
            pbar.update(1)

        out_name = self._get_save_path(book_info.name)
        pbar.set_postfix_str(f"合成文件：{out_name}")
        self.book.save(out_name)
