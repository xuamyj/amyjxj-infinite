# For Omelette database stuff

from google.appengine.ext import db
from userdb import User

def omlets_key(group = 'default'):
    return db.Key.from_path('omlets', group)

class Omlet(db.Model):
    name = db.StringProperty(required = True)
    user_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return Omlet.get_by_id(uid, parent = omlets_key())

    # there should only be one omlet per name
    @classmethod
    def by_name(cls, name):
        omlet = Omlet.all().filter('name = ', name).get()
        return omlet

    # a single user can have multiple omlets,
    # but there should only be one user per user_name
    @classmethod
    def list_username(cls, user_name):
        user = User.by_name(user_name)
        omlet_query = Omlet.all().filter('user_id =', user.key().id()).run()
        return omlet_query

    # IMPORTANT: does not automatically put omlet in database.
    # if user does not exist, or omlet already exists, returns None
    @classmethod
    def make_omlet(cls, user_name, name):
        user = User.by_name(user_name)
        if not user:
            print('Tried to make Omlet - User does not exist.')
            return None
        omlet = Omlet.by_name(name)
        if omlet:
            print('Tried to make Omlet - Omlet already exists.')
            return None
        return Omlet(name = name,
                     user_id = user.key().id())