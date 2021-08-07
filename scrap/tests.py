from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ScrapperAPITestCases(APITestCase):
    fixtures = ['fixtures/data.json']

    def test_scrap_ebay(self):
        url = reverse('scrap')
        scrap_url = 'https://www.ebay.com/itm/294170428836'
        response = self.client.post(url, data={
            'url': scrap_url
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'title': 'Xbox Wireless Controller Electric Volt - Wireless And Bluetooth Connectivity',
            'price': 'US $55.99',
            'stock': 'Available',
            'images': [
                'https://i.ebayimg.com/images/g/R7UAAOSwp0dg6SoB/s-l64.jpg',
                'https://i.ebayimg.com/images/g/TjsAAOSwAW9gyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/0vYAAOSwWZtgyDSn/s-l64.jpg',
                'https://i.ebayimg.com/images/g/4jIAAOSwrsBgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/5UAAAOSw5clgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/jJkAAOSwc1FgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/roYAAOSwDyBgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/b6IAAOSwEZRgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/tqEAAOSwoD5gyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/Mj4AAOSwdqxgyDSm/s-l64.jpg',
                'https://i.ebayimg.com/images/g/QgsAAOSwbntgyDSm/s-l64.jpg'
            ]
        })

    def test_scrap_amazon(self):
        url = reverse('scrap')
        scrap_url = 'https://www.amazon.com/dp/B085K45C3S'
        response = self.client.post(url, data={
            'url': scrap_url
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'title': 'All-new Echo Dot (4th generation) International Version | Smart speaker with Alexa | Charcoal',
            'price': '$49.99',
            'stock': 'Available',
            'images': [
                'https://m.media-amazon.com/images/I/41fYTXmURgL._AC_US40_.jpg',
                'https://m.media-amazon.com/images/I/51ydNSj0AiL._AC_US40_.jpg',
                'https://m.media-amazon.com/images/I/51kEJiB04FL._AC_US40_.jpg',
                'https://m.media-amazon.com/images/I/51H3XYM0hsL._AC_US40_.jpg',
                'https://m.media-amazon.com/images/I/51YVl+rdMxL._AC_US40_.jpg'
            ]
        })

    def test_scrap_from_other(self):
        url = reverse('scrap')
        scrap_url = 'https://www.tokopedia.com/jabra/jabra-elite-85h-over-ear-headphones-with-anc-and-smartsound-tech' \
                    '-black '
        response = self.client.post(url, data={
            'url': scrap_url
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "url": [
                "only supported scrapping for amazon & ebay"
            ]
        })

    def test_scrap_not_detail_product_url(self):
        url = reverse('scrap')
        scrap_urls = [
            'https://www.ebay.com/',
            'https://www.ebay.com/p/18045962259',
            'https://www.ebay.com/b/Video-Game-Accessories/54968/bn_1642249',
            'https://www.amazon.com/',
            'https://www.amazon.com/s?k=oculus&i=electronics-intl-ship',
            'https://www.amazon.com/s?k=gaming+headsets'
        ]
        for scrap_url in scrap_urls:
            response = self.client.post(url, data={
                'url': scrap_url
            })
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, {
                "url": [
                    f"{scrap_url} is not valid detail product."
                ]
            })
