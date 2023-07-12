from ebooklib import epub


class EpubHelper(epub.EpubBook):

    def add_chapter(self, name: str, content: str):
        """添加章节"""
        xhtml_name = f'{name}.xhtml'
        chapter = epub.EpubHtml(title=name, file_name=xhtml_name, lang='en')
        chapter.content = content
        self.add_item(chapter)
        self.spine.append(chapter)
        self.toc.append(epub.Link(xhtml_name, name, name))

    def save(self, file_path: str):
        """保存"""
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        epub.write_epub(file_path, self, {})

        # dir_name = os.path.join("epubs", get_formatted_time("%Y-%m-%d"))
        # os.makedirs(dir_name, exist_ok=True)
        # file_name = file_name + f"_{self.source_model.name}" + ".epub"
        # out_name = self.get_unique_file_path(os.path.join(dir_name, file_name))
        # self.pbar.set_postfix_str(f"合成文件：{out_name}")
