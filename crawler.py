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


print (GetKeywords('https://us.fotolia.com/id/106035423'))

