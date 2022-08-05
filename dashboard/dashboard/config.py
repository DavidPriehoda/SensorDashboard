import urllib.parse
from os import environ, path
from dotenv import load_dotenv

db_params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=team25.database.windows.net;DATABASE=Sensor Dashboard;UID=Admin1@team25.database.windows.net;PWD=pA5LMzymirrHZQ3')

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = '96348e9c6d35c63a170f87a2967803911b39dba8e8c0bf47bf35890ed19b0d00'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % db_params
WTF_CSRF_CHECK_DEFAULT = True