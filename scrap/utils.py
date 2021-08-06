from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}


class Scrapper:

    def __init__(self, url):
        self.url = url

    def scrap(self):
        is_amazon = urlparse(self.url).netloc == 'www.amazon.com'
        if is_amazon:
            return self.amazon_scrap()
        return self.ebay_scrap()

    def amazon_scrap(self):

        page = requests.get(self.url, headers=HEADERS)

        soup = BeautifulSoup(page.content, features="html.parser")

        title = soup.find(id='productTitle').get_text().strip()

        try:
            price = soup.find(id='priceblock_ourprice').get_text()
        except AttributeError:
            price = ''

        try:
            soup.select('#availability .a-color-state')[0].get_text().strip()
            stock = 'Out of Stock'
        except IndexError:
            stock = 'Available'

        images = []
        images_container = soup.find(id='altImages')
        for li in images_container.select('li.item'):
            images.append(li.find('img').attrs.get('src'))

        return {
            "title": title,
            "price": price,
            "stock": stock,
            "images": images
        }

    def ebay_scrap(self):
        page = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="html.parser")

        try:
            title = [i for i in soup.find(id='itemTitle').children][-1]
        except (AttributeError, IndexError):
            title = ''

        prices_tag = ['prcIsum', 'mm-saleDscPrc']
        price = ''
        for i in prices_tag:
            if soup.find(id=i):
                price = soup.find(id=i).get_text()

        stock = 'Out of Stock'
        if soup.find(id='binBtn_btn'):
            stock = 'Available'

        images_selector = soup.select('#vi_main_img_fs ul li')
        images = []
        for li in images_selector:
            image = li.find('img').attrs.get('src')
            images.append(image)
        return {
            "title": title,
            "price": price,
            "stock": stock,
            "images": images
        }
