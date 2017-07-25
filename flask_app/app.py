from flask import Flask
import os

def create_app(settings_key='dev'):
    app = Flask(__name__)
    app.debug = True
    # app.config.from_object('config')

    @app.route('/')
    def main():
        return 'Hello, World!'

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)