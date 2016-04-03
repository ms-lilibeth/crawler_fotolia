import pycurl
from io import BytesIO
from bs4 import BeautifulSoup


buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://us.fotolia.com/p/202938145')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()
body = buffer.getvalue()
html_doc = body.decode('iso-8859-1')
soup = BeautifulSoup(html_doc, 'html.parser')
metas = soup.find_all('meta itemprop=\"url\"')
for link in metas:
    print(link.get('content'))

