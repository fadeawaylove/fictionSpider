from urllib.parse import urljoinfrom bs4 import BeautifulSoupfrom typing import Listfrom src.models import ChapterContentModel, ChapterListModel, BookInfoModelfrom src.custom_exceptions import SourceNotSupportErrorfrom src.utils import extract_host, replace_invalid_chars, CommonFactory, async_runparser_factory = CommonFactory()def register_parser(url: str):    return parser_factory.deco_register(extract_host(url))def get_html_parser(url: str) -> "BaseHtmlParser":    html_parser = parser_factory.get_stuff(extract_host(url))    if not html_parser:        raise SourceNotSupportError(f"source {url} not support.")    return html_parser(url)class BaseHtmlParser:    """根据配置，解析页面内容，获取需要的数据"""    def __init__(self, source_url: str):        self.source_url = source_url        self.host = extract_host(source_url)    def url_join(self, p: str):        return urljoin(self.source_url, p)    def parse_book_info(self, html_str: str) -> BookInfoModel:        raise NotImplementedError    def parse_chapter_list(self, html_str: str) -> List[ChapterListModel]:        raise NotImplementedError    def parse_chapter_text(self, html_str: str, name: str) -> ChapterContentModel:        raise NotImplementedError    def _get_cha_lst_from_dd(self, dd_lst) -> List[ChapterListModel]:        chapter_list = []        for dd in dd_lst:            cha_name = replace_invalid_chars(dd.get_text())            dd_a = dd.find("a")            if dd_a:                cha_url = self.url_join(dd_a.get("href"))                chapter_list.append(ChapterListModel(cha_name=cha_name, cha_url=cha_url))        return chapter_list@register_parser("https://www.xpiaotian.com/")class PiaoTianHtmlParser(BaseHtmlParser):    def parse_chapter_list(self, html_str: str) -> List[ChapterListModel]:        soup = BeautifulSoup(html_str, "html.parser")        dd_lst = soup.find_all("dd")[12:]        chapter_list = self._get_cha_lst_from_dd(dd_lst)        return chapter_list    def parse_book_info(self, html_str: str) -> BookInfoModel:        soup = BeautifulSoup(html_str, "html.parser")        info_div = soup.find("div", id="info")        book_name = info_div.find("h1").get_text()        book_author = info_div.find("p").get_text().split("：")[-1]        book_intro = soup.find("div", id="intro").get_text(strip=True)        book_cover = self.url_join(soup.find("div", id="fmimg").find("img").get("src"))        return BookInfoModel(name=book_name,                             author=book_author,                             cover=book_cover,                             intro=book_intro,                             cha_list=self.parse_chapter_list(html_str))    def parse_chapter_text(self, html_str: str, name: str) -> ChapterContentModel:        soup = BeautifulSoup(html_str, "html.parser")        content_div = soup.find("div", id="content")        new_content_div = soup.new_tag("div", style="text-indent: 2em;")        title_tag = soup.new_tag("h3")        title_tag.string = name        new_content_div.append(title_tag)        for div_child in content_div.children:            if div_child.name == "br":                continue            if not (child_text := div_child.get_text(strip=True)):                continue            p_tag = soup.new_tag("p")            p_tag.string = child_text            new_content_div.append(p_tag)        return ChapterContentModel(name=name, content=new_content_div.prettify())@register_parser("https://www.bbiquge.net/")class BBiQuGe(BaseHtmlParser):    def parse_chapter_list(self, html_str: str) -> List[ChapterListModel]:        soup = BeautifulSoup(html_str, "html.parser")        dd_lst = soup.find("dl", {"class": "zjlist"}).find_all("dd")        chapter_list = self._get_cha_lst_from_dd(dd_lst)        return chapter_list    def parse_book_info(self, html_str: str) -> BookInfoModel:        soup = BeautifulSoup(html_str, "html.parser")        info_div = soup.find("div", id="info")        author_small = info_div.find("small").extract()        book_author = author_small.find("a").get_text()        book_name = info_div.find("h1").get_text(strip=True)        book_intro = soup.find("div", id="intro").get_text(strip=True)        book_cover = self.url_join(soup.find("div", {"class": "img_in"}).find("img").get("src"))        book_info = BookInfoModel(name=book_name,                                  author=book_author,                                  cover=book_cover,                                  intro=book_intro,                                  cha_list=self.parse_chapter_list(html_str),                                  )        option_list = soup.find_all("option")        all_url_lst = [self.url_join(op.get("value")) for op in option_list]        book_info.url_list = all_url_lst[1:]        return book_info    def parse_chapter_text(self, html_str: str, name: str) -> ChapterContentModel:        soup = BeautifulSoup(html_str, "html.parser")        content_div = soup.find("div", id="content")        new_content_div = soup.new_tag("div", style="text-indent: 2em;")        title_tag = soup.new_tag("h3")        title_tag.string = name        new_content_div.append(title_tag)        br_tags = content_div.find_all('br')        for br_tag in br_tags:            br_tag.unwrap()        for div_child in content_div.children:            if not (child_text := div_child.get_text(strip=True)):                continue            if child_text in ("笔趣阁 www.bbiquge.net，最快更新", "最新章节！"):                continue            p_tag = soup.new_tag("p")            p_tag.string = child_text            new_content_div.append(p_tag)        return ChapterContentModel(name=name, content=new_content_div.prettify())@register_parser("https://www.kuaishuku.net/")class KuaiShuKu(BaseHtmlParser):    def parse_chapter_list(self, html_str: str) -> List[ChapterListModel]:        soup = BeautifulSoup(html_str, "html.parser")        li_lst = soup.find("div", {"class": "panel-body"}).find_all("li")        chapter_list = self._get_cha_lst_from_dd(li_lst)        return chapter_list    def parse_book_info(self, html_str: str) -> BookInfoModel:        soup = BeautifulSoup(html_str, "html.parser")        info_div = soup.find("div", {"class": "bookinfo-info"})        book_author = info_div.find("h3").find("a").get_text(strip=True)        book_name = info_div.find("h1").get_text(strip=True)        book_intro = info_div.find("div", {"class": "intro"}).get_text(strip=True)        book_cover = self.url_join(soup.find("div", {"class": "bookinfo-img"}).find("img").get("src"))        book_info = BookInfoModel(name=book_name,                                  author=book_author,                                  cover=book_cover,                                  intro=book_intro,                                  cha_list=self.parse_chapter_list(html_str)                                  )        return book_info    def parse_chapter_text(self, html_str: str, name: str) -> ChapterContentModel:        soup = BeautifulSoup(html_str, "html.parser")        content_div = soup.find("div", {"class": "book-content"})        new_content_div = soup.new_tag("div", style="text-indent: 2em;")        title_tag = soup.new_tag("h3")        title_tag.string = name        new_content_div.append(title_tag)        br_tags = content_div.find_all('br')        for br_tag in br_tags:            br_tag.unwrap()        for div_child in content_div.children:            if not (child_text := div_child.get_text(strip=True)):                continue            if child_text in ("本站网站:www.kuaishuku.net", "本章未完，请点击下一页继续阅读！"):                continue            p_tag = soup.new_tag("p")            p_tag.string = child_text            new_content_div.append(p_tag)        return ChapterContentModel(name=name, content=new_content_div.prettify())