import json

import tornado.httpclient


def get_forex(currencies, date='latest'):
    url = 'https://api.exchangeratesapi.io/%s?symbols=%s' % (
            date, ','.join(currencies))
    http_client = tornado.httpclient.HTTPClient()
    response = http_client.fetch(url)
    return json.loads(response.body)
