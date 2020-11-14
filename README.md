## Demo ElasticSearch

This is a demo app for ingest and reindex documents on elasticsearch. Built with Flask, click and elasticsearch.
First, install the requirements:

    pip install -r requirements.txt

### Create Index

    flask index create --index [INDEX]

Index name can be more than one, separate by comma.

### Ingest Document

Ingest using CLI

    flask index ingest --index [INDEX] --payload [PAYLOAD]

Index name can be more than one, separate by comma. Payload should be JSON escaped string, e.g.:

    flask index ingest --index project_1 --payload "{\"test\": true}"

Or, ingest can be done via API. First, start the API:

    flask run

Then, POST the document data to endpoint http://localhost:5000/ingest

    curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"index":"project_1","payload": {"test": true}}' \

### Reindex Document

    flask index reindex --source [INDEX] --dest [INDEX]

Source index can use asterisk e.g. `project_*`.