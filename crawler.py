import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import re
import json

def GetParsedHtml(link):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    html_doc = body.decode('iso-8859-1')
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def IsPhoto(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    dt_tags = parsed_html.find_all("dt")
    exp_photo = re.compile(".*photo reference.*", re.IGNORECASE)
    exp_video = re.compile(".*video reference.*", re.IGNORECASE)
    for tag in dt_tags:
        if exp_photo.match(tag.text):
            return True
        if exp_video.match(tag.text):
            return False
    raise Exception("Cannot identify which type of content it is")

def GetAllPhotoLinksOnPage(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    metas = parsed_html.find_all('meta')
    exp = re.compile('https.+id.')
    metas_suitable = []
    for link in metas:
        if exp.match(link.get('content')):
            metas_suitable.append(link.get('content'))
    return metas_suitable


def GetPortfolioItems(page):
    #still not ready!
    # Getting portfolio item id, type of media, id of media, title and description
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page

def GetKeywords(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    tags_found = parsed_html.find_all('div',id='keywords_list')
    text = tags_found[0].text
    keywords_list = json.loads(text)
    return keywords_list

def DescribesResolution(tag):
    return (tag.has_attr('data-tab_group_id') and tag.has_attr('data-tab_panel_id')) \
           and re.match('.*\d.*',tag.text)\
           and (tag['data-tab_group_id']=='tabs_size_unit' and tag['data-tab_panel_id'] == 'pixels')

def GetPhotoResolutions(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    tags_found = parsed_html.find_all(DescribesResolution)
    result = set()
    for tag in tags_found:
        str = tag.text
        pair = [int(s) for s in str.split() if s.isdigit()]
        pair = tuple(pair)
        result.add(pair)
    return result

def TextContainsResolution(tag):
    return re.match('.*\d+.* x .*\d+.*',tag.text)

def GetVideoResolutions(page):
    #still not ready!
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    res = parsed_html.find_all(TextContainsResolution)
    result = set()
    for tag in res:
        str = tag.text
        pair = [int(s) for s in str.split() if s.isdigit()]
        pair = tuple(pair)
        result.add(pair)
    return result


result = GetVideoResolutions('https://us.fotolia.com/id/106881017')
for r in result:
    print(r), print('---------')

