# -*- coding: utf-8 -*-

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-quess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
    ]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')    

# mail server settings
MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'example@com.ua'
MAIL_PASSWORD = 'qwerty'

# administrator list
ADMINS = ['example@com.ua']

# pagination
POSTS_PER_PAGE = 3

WHOOSH_ENABLED = os.environ.get('HEROKU') is None
WHOOSH_BASE = os.path.join(basedir, 'search.db')

MAX_SEARCH_RESULTS = 50

LANGUAGES = {
	'en' : 'English',
	'ru' : 'Русский',
    'uk' : 'Українська'
}

MS_TRANSLATOR_CLIENT_ID = None
MS_TRANSLATOR_CLIENT_SECRET = None