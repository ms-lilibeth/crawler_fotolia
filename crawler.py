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
def ContainsTitle(tag):
    return
def GetPortfolioItems(page, href=None):
    #still not ready!
    # Getting id of media, title and description
    result = {}
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
        href = page
    else:
        parsed_html = page
        if href == None:
            raise Exception("Pass the link as the second parameter")
    # Finding media id
    search_result = re.search("id/\d+",href)
    if not search_result:
        raise Exception("Cannot find media id in the link")
    tmp_str = href[search_result.regs[0][0]:search_result.regs[0][1]]
    search_result = re.search("\d+",tmp_str)
    media_id =int(tmp_str[search_result.regs[0][0]:search_result.regs[0][1]])
    result['media_id'] = media_id
    #Finding title
    title_tags = parsed_html.find_all('h1', class_='content-title')
    if title_tags.__len__() > 1:
        raise Exception("Finding title: more than 1 title found")
    result['title']=title_tags[0].text
    return result


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


#result = GetPortfolioItems('https://us.fotolia.com/id/106035736') #photo
result = GetPortfolioItems('https://us.fotolia.com/id/106881017') #video
print(result)