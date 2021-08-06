import json

from django.db import models


class ScrapModels(models.Model):
    # README :)
    """
    This models is only for testing purpose,
    so when we expecting some response from amazon/ebay
    it will not breaking the test when the data has changed.
    example:
    we expect response like this in the test case
    "title": "Apple iPhone 11, US Version, 128GB, Purple - Unlocked (Renewed)",
    "price": "$572.00",
    "stock": "Available",
    "image": "https://images-na.ssl-images-amazon.com/images/I/61DanysfE8L.__AC_SX300_SY300_QL70_ML2_.jpg"

    but the response from amazon/ebay has changed because seller changed the data.
    so the solution is we have to load data (fixtures) when doing testcase.
    And in the views we have to put some condition if the environment is TESTING:
    get data from database according to url.
    """
    url = models.URLField(unique=True)  # type: str
    response = models.TextField()  # type: str

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if isinstance(self.response, dict):
            self.response = json.dumps(self.response)
        return super(ScrapModels, self).save(*args, **kwargs)

    @property
    def get_response(self):
        return json.loads(self.response)

