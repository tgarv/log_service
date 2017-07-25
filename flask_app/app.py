from flask import Flask, request
import os
from intervaltree import IntervalTree
import json

def create_app(settings_key='dev'):
    app = Flask(__name__)
    app.debug = True
    app.logs = {}
    # app.config.from_object('config')

    @app.route('/')
    def main():
        return 'Hello, World!'

    @app.route('/<app_id>', methods=['POST'])
    def create_log(app_id):
        request_json = request.get_json()
        if not request_json:
            # Make sure a JSON object was provided with the request
            return 'Malformed request', 400

        request_start = request_json.get('start', -1)
        request_end = request_json.get('end', -1)
        if not request_start and not request_end:
            # Make sure start and end are set. We could do additional validation,
            # but those are the only fields that are strictly required.
            return 'Malformed request -- please provide a "start" and "end"', 400

        if app_id not in app.logs:
            # We don't have a tree yet for this app ID, so create one
            app.logs[app_id] = IntervalTree()
        app.logs[app_id].addi(request_start, request_end, request_json)

        return '', 200


    @app.route('/<app_id>', methods=['GET'])
    def get_logs(app_id):
        required_parameters = set(['start', 'end'])
        if set(request.args.viewkeys()) < required_parameters:
            # A quick way to check that all the required arguments have been provided
            # (via https://stackoverflow.com/a/1285926)
            return 'Malformed request -- please provide a "start" and "end"', 400

        logs_for_app = app.logs.get(app_id, [])
        logs_in_range = []
        if logs_for_app:
            logs_in_range = logs_for_app.search(int(request.args.get('start')), int(request.args.get('end')))
            logs_in_range = [log.data for log in logs_in_range]

        return json.dumps(logs_in_range)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Use this for an externally-available app
    # app.run()