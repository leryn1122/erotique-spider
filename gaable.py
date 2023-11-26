from typing import Iterable
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.chrome.webdriver import WebDriver
from lxml import etree
import json

def is_soup_tag(e):
    return isinstance(e, Tag)


def is_soup_string(e):
    if not isinstance(e, NavigableString):
        return False
    else:
        return len(e.strip()) > 0


def extract_records(html: BeautifulSoup):
    divs = html.find('div', id="list_videos_common_videos_list") \
        .find('div', class_="row gutter-20")
    records = []

    #
    for div in filter(is_soup_tag, divs):
        record = dict()
        record['id'] = div.find('a').get('href').split('/')[4].upper()
        record['title'] = div.find('h6', class_="title")\
            .find('a').text.replace(' ', '').replace('\n', '')

        counter = 0
        for e in filter(is_soup_string, div.find('p', class_="sub-title")):
            # First value might be `watch`
            if counter == 0:
                record['watch'] = int(e.replace(' ', ''))
            # Second value might be `star`
            elif counter > 0:
                record['star'] = int(e.replace(' ', ''))
            counter += 1
        records.append(record)

    return records


def extract_records_v2(content: str):
    document = etree.HTML(content, etree.HTMLParser())
    records = []
    with open('conf/rules.json', 'r') as f:
        rules = json.load(f)['gaable']
    items = document.xpath(rules['xpath'])
    for i in range(1, len(items)):
        record = dict()
        record['id'] = document.xpath(rules['fields']['id']['xpath'] % i)[0].split('/')[-2].upper()
        record['title'] = document.xpath(rules['fields']['title']['xpath'] % i)[0]
        record['watch'] = int(document.xpath(rules['fields']['watch']['xpath'] % i)[0].replace(' ', ''))
        record['stars'] = int(document.xpath(rules['fields']['stars']['xpath'] % i)[0].replace(' ', ''))
        records.append(record)
    return records


if __name__ == '__main__':
    with open('resources/test.html') as f:
        content = f.read()
    # for result in extract_records(BeautifulSoup(content, 'html.parser')):
    #     print(result)

    for result in extract_records_v2(content):
        print(result)
