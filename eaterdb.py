# For Omelette database stuff

from google.appengine.ext import db
from omletdb import Omlet

def eaters_key(group = 'default'):
    return db.Key.from_path('eaters', group)

class Eater(db.Model):
    omlet_id = db.IntegerProperty(required = True)
    user_id = db.IntegerProperty(required = True)
    latest_bite = db.IntegerProperty(required = True)
    archived = db.BooleanProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return Eater.get_by_id(uid, parent = eaters_key())

    # there should only be one eater associated with a particular omlet+passcode
    @classmethod
    def by_username(cls, omlet_name, username):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to find Bite - Omlet does not exist.')
            return None
        user = User.by_name(user_name)
        if not user:
            print('Tried to find Bite - User does not exist.')
            return None
        eater = Eater.all().filter('omlet_id = ', omlet.key().id()).filter(
            'user_id =', user.key().id()).get()
        return eater

    # returns the bite that was most recently eaten by this eater
    # (ex. if this eater has seen 1-4, returns 4.)
    @classmethod
    def get_latest_bite(cls, omlet_name, username):
        eater = Eater.by_username(omlet_name, username)
        return eater.latest_bite

    # sets the latest_bite to the number given, all previous bites are assumed to be eaten
    # this should be called in conjunction with Bite.set_eaten()
    @classmethod
    def set_latest_bite(cls, omlet_name, username, number):
        eater = Eater.by_username(omlet_name, username)
        eater.latest_bite = number
        eater.put()

    # returns whether this eater/omlet pair has been archived
    @classmethod
    def get_archived(cls, omlet_name, number):
        eater = Eater.by_username(omlet_name, username)
        return eater.archived

    # set this eater/omlet pair as archived or not archived.
    # (nothing in this app is deletable... for now. 8/17/15)
    @classmethod
    def set_archived(cls, omlet_name, number, archive_flag):
        eater = Eater.by_username(omlet_name, username)
        eater.archived = archive_flag
        eater.put()

    # IMPORTANT: does not automatically put bite in database
    # if omlet does not exist, or eater already exists, returns None
    @classmethod
    def create_eater(cls, omlet_name, username, latest_bite = 0, archived = False):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to make Eater - Omlet does not exist.')
            return None
        user = User.by_name(user_name)
        if not user:
            print('Tried to make Eater - User does not exist.')
            return None
        eater = Eater.by_username(omlet_name, username)
        if eater:
            print('Tried to make Eater - Eater already exists.')
            return None

        return Eater(parent = eaters_key(),
                     omlet_id = omlet.key().id(),
                     user_id = user.key().id(),
                     latest_bite = latest_bite,
                     archived = archived)