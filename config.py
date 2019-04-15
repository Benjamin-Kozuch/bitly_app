import os


class Config(object):
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
