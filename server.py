import os

import elasticsearch

from flask import Flask
from flask_cors import CORS

from apies import apies_blueprint

BASE = 'http://pipelines/data/{}_in_es/datapackage.json'
# BASE = 'http://api.yodaat.org/data/{}_in_es/datapackage.json'
ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = int(os.environ.get('ES_PORT', '9200'))
INDEX_NAME = os.environ.get('INDEX_NAME', 'migdar')

app = Flask(__name__)
CORS(app)
blueprint = apies_blueprint(app,
    [
        BASE.format('publications'),
        BASE.format('orgs'),
        BASE.format('datasets'),
    ],
    elasticsearch.Elasticsearch([dict(host=ES_HOST, port=ES_PORT)], timeout=60),
    INDEX_NAME,
    multi_match_type='most_fields',
    multi_match_operator='or'
)
app.register_blueprint(blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run()
