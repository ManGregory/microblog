from app import db
from app import app
from hashlib import md5
from config import WHOOSH_ENABLED
import re

ROLE_USER = 0
ROLE_ADMIN = 1

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))	
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	lang_id = db.Column(db.Integer, db.ForeignKey('language.id'))
	followed = db.relationship('User',
		secondary = followers,
		primaryjoin = (followers.c.follower_id == id),
		secondaryjoin = (followers.c.followed_id == id),
		backref = db.backref('followers', lazy = 'dynamic'),
		lazy = 'dynamic')

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname = nickname).first() == None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname = new_nickname).first() == None:
				break
			version += 1
		return new_nickname

	@staticmethod
	def make_valid_nickname(nickname):
		return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

	def is_authenticated(self):
		return True;

	def is_active(self):
		return True;

	def is_anonymous(self):
		return False;

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def __repr__(self):
		return '<User %r>' % (self.nickname)	

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

class Post(db.Model):
	__searchable__ = ['body']

	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	langauge = db.Column(db.String(5))

	def __repr__(self):
		return '<Post %r>' % (self.body)

class Language(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	short_name = db.Column(db.String(5))
	long_name = db.Column(db.String(15))		
	users = db.relationship('User', backref = 'lang', lazy = 'dynamic')

	def __repr__(self):
		return '<Language %s - %s>' % (self.short_name, self.long_name)
		
if WHOOSH_ENABLED:
	import flask.ext.whooshalchemy as whooshalchemy
	whooshalchemy.whoosh_index(app, Post)