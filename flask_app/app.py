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
            return 'Malformed request', 400
        request_start = request_json.get('start')
        request_end = request_json.get('end')
        if app_id not in app.logs:
            app.logs[app_id] = IntervalTree()
        app.logs[app_id].addi(request_start, request_end, request_json)
        return 'Hello, ' + str(app_id)

    @app.route('/<app_id>', methods=['GET'])
    def get_logs(app_id):
        if not request.args:
            return 'Malformed request', 400
        logs_for_app = app.logs.get(app_id, [])
        if logs_for_app:
            request_start = request.args.get('start')
            request_end = request.args.get('end')
            logs_in_range = logs_for_app.search(int(request_start), int(request_end))
            logs_in_range = [log.data for log in logs_in_range]
        else:
            logs_in_range = []

        return json.dumps({'logs': logs_in_range})

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Use this for an externally-available app
    # app.run()