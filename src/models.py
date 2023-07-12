from pydantic import BaseModel
from typing import List


class ChapterListModel(BaseModel):
    cha_name: str
    cha_url: str


class ChapterContentModel(BaseModel):
    name: str
    content: str


class BookInfoModel(BaseModel):
    name: str
    author: str
    cover: str
    intro: str
    cha_list: List[ChapterListModel] = []
    url_list: List = []
