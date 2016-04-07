import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import re
import json
import pymysql
import time

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

def GetAllMediaLinksOnPage(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    metas = parsed_html.find_all('meta')
    exp = re.compile('https://us\.fotolia\.com/id.')
    metas_suitable = []
    for link in metas:
        if exp.match(link.get('content')):
            metas_suitable.append(link.get('content'))
    return metas_suitable
def GetAuthorId(link):
    search_result = re.search("p/\d+", link)
    if not search_result:
        raise Exception("Cannot find author id in the link")
    tmp_str = link[search_result.regs[0][0]:search_result.regs[0][1]]
    search_result = re.search("\d+", tmp_str)
    author_id = int(tmp_str[search_result.regs[0][0]:search_result.regs[0][1]])
    return author_id
def GetPortfolioItems(page, href=None):
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
    tags_found = parsed_html.find_all('h1', class_='content-title')
    if tags_found.__len__() > 1:
        raise Exception("Finding title: more than 1 title found")
    result['title']=tags_found[0].text
    #Finding description
    tags_found = parsed_html.find_all('div',attrs={'data-tab_group_id':"tabs_content_details",
                                             'data-tab_panel_id':"description"})
    desc_str = ""
    for string in tags_found[0].strings:
        desc_str += string
    desc_str = desc_str[2:-2]
    result['description']=desc_str
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

#returns set
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

#returns set
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
def ContainsPhotoCategory(tag):
    return tag.name=='a' \
        and re.match('.*category.*',tag['href'],re.IGNORECASE)
def GetPhotoCategories(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    tags_found = parsed_html.find_all(ContainsPhotoCategory)
    result = set()
    for tag in tags_found:
        result.add(tag.text)
    return result
def GetVideoDuration(page):
    if not type(page) is BeautifulSoup:
        parsed_html = GetParsedHtml(page)
    else:
        parsed_html = page
    tags_found = parsed_html.find_all('span',class_="thumb-video-duration")
    result = {}
    for tag in tags_found:
        media_id = tag.parent.parent['href'][4:]
        duration= tag.text.split(':')
        min = int(duration[0])
        sec = int(duration[1])
        duration = min*60 + sec
        result[int(media_id)] = duration
    return result
def GetNextPortfolioPage(current_page):
    if not type(current_page) is BeautifulSoup:
        parsed_html = GetParsedHtml(current_page)
    else:
        parsed_html = current_page
    tags_found = parsed_html.find_all('a', class_='button')
    for tag in tags_found:
        if re.match('.*next page.*',tag.text,re.IGNORECASE):
            return tag['href']
    return None
def WriteToDatabase(info):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='mlstudent4',
                                 password='59a7752be0',
                                 db='scraping',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
                        # Selecting pi_id
            sql = "SELECT `pi_id` FROM `portfolio_items` WHERE `author_id`=%s AND `media_type`=%s AND `media_id`=%s"
            cursor.execute(sql, (info['author_id'],info['media_type'], info['media_id']))
            pi_id = cursor.fetchone()['pi_id']

            # Inserting portfolio items
            sql = "DELETE FROM `portfolio_items` WHERE `author_id`=%s AND `media_type`=%s AND `media_id`=%s "
            cursor.execute(sql, (info['author_id'], info['media_type'], info['media_id']))

            sql = "INSERT INTO `portfolio_items` (`author_id`,`media_type`, `media_id`, `title`, `description`)" \
                  " VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (
            info['author_id'], info['media_type'], info['media_id'], info['title'], info['description']))
            #inserting keywords
            sql = "DELETE FROM `items_keywords` WHERE `pi_id`=%s"
            cursor.execute(sql, (pi_id))

            for kw in info['keywords']:
                sql = "INSERT INTO `items_keywords` (`pi_id`,`keyword`)" \
                  " VALUES (%s, %s)"
                cursor.execute(sql, (pi_id,kw))

            #inserting resolutions
            sql = "DELETE FROM `items_resolutions` WHERE `pi_id`=%s"
            cursor.execute(sql, (pi_id))

            for r in info['resolutions']:
                str_to_insert = str(r[0]) + " x " + str(r[1])
                sql = "INSERT INTO `items_resolutions` (`pi_id`,`resolution_size`)" \
                      " VALUES (%s, %s)"
                cursor.execute(sql, (pi_id, str_to_insert))

            #inserting video duration and photo categories
            if info['media_type']:
                sql = "DELETE FROM `video_duration` WHERE `pi_id`=%s"
                cursor.execute(sql, (pi_id))
                sql = "INSERT INTO `video_duration` (`pi_id`,`duration`) VALUES (%s,%s)"
                cursor.execute(sql,(pi_id,info['video_duration']))
            else:
                sql = "DELETE FROM `photos_categories` WHERE `pi_id`=%s"
                cursor.execute(sql, (pi_id))

                for cat in info['photo_categories']:
                    sql = "INSERT INTO `photos_categories` (`pi_id`,`category_name`)" \
                          " VALUES (%s, %s)"
                    cursor.execute(sql, (pi_id, cat))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()

domain = 'https://us.fotolia.com'
portfolio_page = 'https://us.fotolia.com/p/202938145'

author_id = GetAuthorId(portfolio_page)
videos_duration = GetVideoDuration(portfolio_page)
media_pages_links = GetAllMediaLinksOnPage(portfolio_page)
while portfolio_page != None:
    inc_tmp=1;
    for media_link in media_pages_links:
        with open("links_parsed","a") as f:
            f.write(media_link)
            f.write("\n")
        inc_tmp+=1
        media_page = GetParsedHtml(media_link) #for not to parse every time
        info = GetPortfolioItems(media_page,media_link)
        info['keywords'] = GetKeywords(media_page)
        info['author_id'] = author_id
        if IsPhoto(media_page):
            info['media_type'] = 0
            info['resolutions'] = GetPhotoResolutions(media_page)
            info['photo_categories'] = GetPhotoCategories(media_page)
        else:
            info['media_type'] = 1
            info['resolutions'] = GetVideoResolutions(media_page)
            media_id = info['media_id']
            info['video_duration'] = videos_duration[media_id]
        WriteToDatabase(info)
        time.sleep(1)
    next_page = GetNextPortfolioPage(portfolio_page)
    if next_page != None:
        portfolio_page = domain + next_page
    else:
        portfolio_page = None
