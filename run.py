from app import create_app
# from flask import current_app
import os

app = create_app(config_name=os.getenv('FLASK_CONFIG'))


if __name__ == '__main__':
    app.run()