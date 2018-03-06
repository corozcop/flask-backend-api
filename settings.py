import os

# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:toor@192.168.33.10/boletaje"
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'mysecretkeydontsharethis'
FLASK_DEBUG = True
FLASK_SERVER_NAME = 'localhost:5000'
