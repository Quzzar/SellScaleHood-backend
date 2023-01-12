import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

FIREBASE_CONFIG = {
  'apiKey': os.environ.get("FIREBASE_API_KEY"),
  'authDomain': os.environ.get("FIREBASE_AUTH_DOMAIN"),
  'databaseURL': os.environ.get("FIREBASE_DB_URL"),
  'storageBucket': os.environ.get("FIREBASE_STORAGE_BUCKET"),
}

BASE_URL = os.environ.get("BASE_URL")