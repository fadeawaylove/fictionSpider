import re

from bs4 import BeautifulSoup


def remove_tags(html_string, tag_list):
    soup = BeautifulSoup(html_string, 'html.parser')
    all_tags = soup.find_all()
    for tag in all_tags:
        if tag.name not in tag_list:
            tag.decompose()
    clean_html = str(soup)
    return clean_html


def remove_links(text):
    pattern = r'https?://\S+'
    return re.sub(pattern, '', text)
