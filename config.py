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
    FictionSourceModel(
        name="和图书",
        home="https://www.hetushu.com",
        desc="效果不错，但是网页响应太慢了~",
        cover_xpath='//*[@id="left"]/div[1]/img/@src',
        list_xpath='//*[@id="dir"]/dd/a',
        content_xpath='//*[@id="content"]',
        ext_headers={"Referer": "https://www.hetushu.com"},
        rate_count=5
    ),
    FictionSourceModel(
        name="养鬼为祸",
        home="http://www.xygwh.cc",
        # cover_xpath='/html/body/div[4]/div[2]/div[1]/img/@src',
        list_xpath='//div[@class="listmain"]/dl/dd[position() > 9]/a',
        content_xpath='//*[@id="content"]',
        replace_string_list=["请记住本书首发域名：www.yangguiweihuo.com。笔趣阁手机版阅读网址：m.yangguiweihuo.com",
                             '<div align="center"><a href="javascript:posterror();" style="text-align:center;color:red;">章节错误,点此举报(免注册)我们会尽快处理.</a>举报后请耐心等待,并刷新页面。</div>']
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
