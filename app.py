import click, os, json
from flask import Flask, request, jsonify
from flask.cli import AppGroup
from elasticsearch import Elasticsearch


app = Flask(__name__)
index_cli = AppGroup('index', short_help='Index CLI Commands.')
es = Elasticsearch(os.getenv('ELASTICSEARCH_HOST', 'localhost:9200'))


@app.route('/ingest', methods=['POST'])
def ingest_http():
    """
    Ingest documents.
    """
    index = request.json.get('index', None)
    payload = request.json.get('payload')
    for i in index.split(','):
        res = es.index(index=i.lower(), body=payload)
        print(res)
    
    return jsonify({'index': index, 'payload': payload})


@index_cli.command('status')
def status():
    """Status index"""
    print(es.cluster.health())


@index_cli.command('create')
@click.option('--index', required=True, help='Index name to create, to create multiple index separate by comma.')
def create(index):
    """Create index"""
    for i in index.split(','):
        res = es.indices.create(index=i.lower())
        print(res)


@index_cli.command('ingest')
@click.option('--index', required=True, help='Index name to load data.')
@click.option('--payload', required=True, help='Payload data.')
def ingest_cli(index, payload):
    """Ingest document to index"""
    for i in index.split(','):
        print(payload)
        doc = json.loads(payload)
        res = es.index(index=i.lower(), body=doc)
        print(res)


@index_cli.command('reindex')
@click.option('--source', required=True, help='Source index, could be multiple index.')
@click.option('--dest', required=True, help='Destination index.')
def reindex(source, dest):
    """Reindex indices."""
    body = {
        "source": {
            "index": source
        },
        "dest": {
            "index": dest
        },
        "script": {
            "lang": "painless",
            "source": "ctx._source.last_updated = new Date()"
        }
    }

    res = es.reindex(body=body, wait_for_completion=True)
    print(res)

app.cli.add_command(index_cli)
