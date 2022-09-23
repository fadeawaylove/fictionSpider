# 书源地址
from models import FictionSourceModel

SOURCE_LIST = [
    FictionSourceModel(
        name="快书库",
        home="http://www.kuaishuku.net/",
        list_xpath='//*[@id="stylechapter"]/li/a',
        content_xpath='//div[@class="book-content"]'
    ),
    FictionSourceModel(
        name="三七中文",
        home="https://www.777zw.la/",
        list_xpath='//div[@class="section-box"]/ul/li/a',
        content_xpath='//*[@id="content"]',
        cover_xpath='//div[@class="imgbox"]/img/@src',
        replace_string_list=["<p>(三七中文 www.37zw.net)</p>", "<p>〖三七中文 www.37zw.com〗百度搜索“37zw”访问</p>"]

    ),
    FictionSourceModel(
        name="三七中文",
        home="https://www.777zw.net/",
        list_xpath='//div[@class="section-box"]/ul/li/a',
        content_xpath='//*[@id="content"]',
        cover_xpath='//div[@class="imgbox"]/img/@src',
        replace_string_list=["<p>(三七中文 www.37zw.net)</p>", "<p>〖三七中文 www.37zw.com〗百度搜索“37zw”访问</p>"]
    ),
]

#     xpath_map = {
#         "https://mm.abqg5200.com": ['//*[@id="readerlist"]/ul/li/a', '//*[@id="content"]'],
#         "https://www.x9itan.com": ["/html/body/div/div[6]/div[1]/div[2]/ul/li/a", '//*[@id="articlecontent"]'],
#         "https://www.777zw.la": ["/html/body/div[3]/div[2]/div/div/ul/li/a", '//*[@id="content"]'],
#         "https://www.777zw.net": ["/html/body/div[3]/div[2]/div/div/ul/li/a", '//*[@id="content"]'],
#         "http://www.huazhuangsheying.com": ["/html/body/div[3]/div[2]/div/div[2]/ul/li/a", '//*[@id="content"]'],
#         "https://www.3zmmm.net": ['//div[@class="listmain"]/dl/dd[position() > 12]/a', '//div[@id="content"]'],
#         "https://www.86wxw.com": ['//td[@class="ccss"]/a', '//div[@id="content"]'],
#         "http://www.xbiquge5.com": ['//*[@id="list"]/dl/dd[position() > 12]/a', '//div[@id="content"]'],
#         "http://www.xygwh.cc": ['//div[@class="listmain"]/dl/dd[position() > 9]/a', '//div[@id="content"]'],
#         "http://www.kuaishuku.net": ['//*[@id="stylechapter"]/li/a', '//div[@class="book-content"]'],
#     }
