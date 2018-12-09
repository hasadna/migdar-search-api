import os

import elasticsearch

from flask import Flask
from flask_cors import CORS

from apies import apies_blueprint

DATAPACKAGE_BASE = 'http://pipelines/datapackages/{}/datapackage.json'
ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = int(os.environ.get('ES_PORT', '9200'))
INDEX_NAME = os.environ.get('INDEX_NAME', 'migdar')

app = Flask(__name__)
CORS(app)
blueprint = apies_blueprint(app,
    [
        'http://pipelines/data/publications_for_es/datapackage.json'
    ],
    elasticsearch.Elasticsearch([dict(host=ES_HOST, port=ES_PORT)], timeout=60),
    INDEX_NAME,
    # dont_highlight={
    #     'kind',
    #     'kind_he',
    #     'budget_code',
    #     'entity_kind',
    #     'entity_id',
    #     'code',
    # },
)
app.register_blueprint(blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run()
