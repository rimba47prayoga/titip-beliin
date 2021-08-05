from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ScrapperAPITestCases(APITestCase):

    def test_scrap_amazon(self):
        url = reverse('scrap')
        scrap_url = 'https://www.amazon.com/Apple-iPhone-11-128GB-Purple/dp/B07ZPJWGKZ/ref=sr_1_1?dchild=1&keywords' \
                    '=iphone&qid=1628171349&sr=8-1 '
        response = self.client.post(url, data={
            'url': scrap_url
        })
        self.assertEqual(response.data, {
            "title": "Apple iPhone 11, US Version, 128GB, Purple - Unlocked (Renewed)",
            "price": "$572.00",
            "stock": "Available",
            "image": "https://images-na.ssl-images-amazon.com/images/I/61DanysfE8L.__AC_SX300_SY300_QL70_ML2_.jpg"
        })
