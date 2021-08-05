from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


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

        # to prevent script from crashing when there isn't a price for the product
        try:
            price = soup.find(id='priceblock_ourprice').get_text()
        except Exception as e:
            price = ''

        # checking if there is "Out of stock" and if not, it means the product is available
        try:
            soup.select('#availability .a-color-state')[0].get_text().strip()
            stock = 'Out of Stock'
        except IndexError:
            stock = 'Available'

        try:
            images = soup.select('#imgTagWrapperId > img')[0].attrs.get('src')
        except IndexError:
            images = ''

        return {
            "title": title,
            "price": price,
            "stock": stock,
            "images": images
        }

    def ebay_scrap(self):

        # fetch the url
        page = requests.get(self.url, headers=HEADERS)

        # create the object that will contain all the info in the url
        soup = BeautifulSoup(page.content, features="html.parser")

        # product title
        title = soup.find(id='itemTitle').get_text().strip()

        # to prevent script from crashing when there isn't a price for the product
        try:
            price = soup.find(id='prcIsum').get_text()
        except Exception as e:
            price = ''

        images_selector = soup.select('#vi_main_img_fs ul li')
        images = []
        for li in images_selector:
            image = li.find('img').attrs.get('src')
            images.append(image)
        return {
            "title": title,
            "price": price,
            "images": images
        }
