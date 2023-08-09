import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
SECRET = os.environ.get("SECRET")
