from pydantic import BaseModel


class FictionSourceModel(BaseModel):
    name: str
    home: str
    title_xpath: str = "//h1 | //h2 | //h3 | //h4"
    cover_xpath: str = "//img[1]/@src"
    list_xpath: str
    content_xpath: str
    ext_headers: dict = {}
    replace_string_list: list = []
