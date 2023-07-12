## 简介

免费的小说采集程序，只需输入小说网址，则自动抓取小说内容，并生成epub文件。

## 使用

```shell
# 安装依赖
pip install -r requirements.txt
# 运行
python main.py
# 然后根据提示输入小说地址
```

## 更新日志

### TODO

- 打包成命令行工具


### 2023.07.13

- 重构项目
- 增加书源[https://www.xpiaotian.com/](https://www.xpiaotian.com/)


### 2023.07.07

- 新增书源
- 新增`all_page_xpath`配置，能够爬取分页的章节列表
- 添加介绍页
- 新增`author_xpath`配置，用于设置小说作者

### 2023.07.06

- 新增书源【和图书】、【养鬼为祸】
- 新增进度条
- 自动添加章节名到每一章节开头