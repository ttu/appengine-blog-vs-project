import os
import re

from google.appengine.ext import db
from google.appengine.api import memcache

key = 'users'

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    user_id = db.StringProperty(required = True)
    name = db.StringProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_user_id(cls, user_id):
        user = memcache.get(str(user_id))
        if user is None:
            user = User.gql("WHERE user_id = :1", str(user_id)).get()
        return user

    @classmethod
    def create(cls, profile):
        return User(parent = users_key(),
                    user_id = profile.id,
                    name = profile.name)

    @classmethod
    def try_add_user(cls, user_profile):
        if user_profile:
            if User.by_user_id(user_profile.id) is None:
               u = User.create(user_profile)
               u.put()
               memcache.set(str(user_profile.id), u)