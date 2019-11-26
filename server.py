import os

import elasticsearch

from flask import Flask
from flask_cors import CORS

from apies import apies_blueprint

#BASE = 'http://pipelines/data/{}_in_es/datapackage.json'
BASE = 'http://api.yodaat.org/data/{}_in_es/datapackage.json'
ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = int(os.environ.get('ES_PORT', '9200'))
# INDEX_NAME = os.environ.get('INDEX_NAME', 'migdar')

def rules(field):
    if field.get('es:title') or field.get('es:hebrew'):
        if field.get('es:keyword'):
            return [('exact', '^10')]
        else:
            return [('inexact', '^3'), ('natural', '.hebrew^10')]
    elif field.get('es:boost'):
        if field.get('es:keyword'):
            return [('exact', '^10')]
        else:
            return [('inexact', '^10')]
    elif field.get('es:keyword'):
        return [('exact', '')]
    else:
        return [('inexact', '')]

TYPES = [
    'publications', 'orgs', 'datasets',
]

app = Flask(__name__)
CORS(app)
blueprint = apies_blueprint(app,
    [BASE.format(t) for t in TYPES],
    elasticsearch.Elasticsearch([dict(host=ES_HOST, port=ES_PORT)], timeout=60),
    dict(
        (t, 'migdar__%s' % t)
        for t in TYPES
    ),
    'migdar__docs',
    multi_match_type='best_fields',
    multi_match_operator='and',
    dont_highlight='*',
    text_field_rules=rules,
    debug_queries=True,
)
app.register_blueprint(blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run()
