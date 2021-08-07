# titip-beliin

### To run the project
- Install python 3.6.5
- Install requirements
`pip install -r requirements.txt`
  
- create database mysql, i'm using mysql. Or you can change database in settings.py
- run `./manage.py migrate`
- run `./manage.py runserver`
- for testing, run `./manage.py test`

## API endpoints
``localhost:8000/api/v1/scrap``

payload: `{"url": "https://www.amazon.com/dp/B085K45C3S"}`

below are the urls that i've been scrapped:
- https://www.ebay.com/itm/294170428836
- https://www.ebay.com/itm/313483072603
- https://www.ebay.com/itm/303924727947
- https://www.amazon.com/dp/B085K45C3S
- https://www.amazon.com/PlayStation-5-DualSense-Wireless-Controller/dp/B08H99BPJN/ref=pd_sbs_3/144-6452510-8483542
- https://www.amazon.com/Xbox-One-S/dp/B08GGDT47N/ref=pd_sbs_5/144-6452510-8483542
