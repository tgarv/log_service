from flask import Flask, request
import os
from intervaltree import IntervalTree
import json

def create_app(settings_key='dev'):
    app = Flask(__name__)
    app.debug = True
    app.logs = IntervalTree()
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
        request_json['app_id'] = app_id
        app.logs.addi(request_start, request_end, request_json)
        return 'Hello, ' + str(app_id)

    @app.route('/<app_id>', methods=['GET'])
    def get_logs(app_id):
        if not request.args:
            return 'Malformed request', 400
        request_start = request.args.get('start')
        request_end = request.args.get('end')
        logs_in_range = app.logs.search(int(request_start), int(request_end))

        result_logs = []
        for log in logs_in_range:
            if log.data.get('app_id') == app_id:
                data = log.data.copy()
                del(data['app_id'])  # client doesn't care about the app_id because it's their app
                result_logs.append(data)
        return json.dumps({'logs': result_logs})

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Use this for an externally-available app
    # app.run()