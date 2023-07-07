from pydantic import BaseModel


class FictionSourceModel(BaseModel):
    name: str  # 站点名称
    home: str  # 站点地址
    desc: str = ""
    title_xpath: str = "//h1 | //h2 | //h3 | //h4"  # 提取小说标题的xpath
    cover_xpath: str = "//img[1]/@src"  # 提取小说封面的xpath
    list_xpath: str  # 提取小说章节列表的xpath
    content_xpath: str  # 提取小说内容的xpath
    ext_headers: dict = {}  # 发起请求时额外的请求头
    replace_string_list: list = []  # 内容中需要替换为空的字符串
    include_tag_list: list = ["div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "br"]  # 内容包含的标签列表，不在此列表中的标签会被移除
    rate_count: int = 20  # 采集速率，每批次采集多少章
    begin_title: bool = True  # 在章节内容开始加上一个章节名
    all_page_xpath: str = ""  # 所有章节列表的xpath
    intro_xpath: str = ""  # 小说简介
    author_xpath: str = ""  # 作者名
