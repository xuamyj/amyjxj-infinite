# For Omelette database stuff

from google.appengine.ext import db
from omletdb import Omlet

def eaters_key(group = 'default'):
    return db.Key.from_path('eaters', group)

class Eater(db.Model):
    passcode = db.StringProperty(required = True)
    latest_bite = db.IntegerProperty(required = True)
    omlet_id = db.IntegerProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return Eater.get_by_id(uid, parent = eaters_key())

    # there should only be one eater associated with a particular omlet+passcode
    @classmethod
    def by_passcode(cls, omlet_name, passcode):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to find Bite - Omlet does not exist.')
            return None
        eater = Eater.all().filter('omlet_id = ', omlet.key().id()).filter(
            'passcode =', passcode).get()
        return eater

    # returns the bite that was most recently eaten by this eater
    # (ex. if this eater has seen 1-4, returns 4.)
    @classmethod
    def get_latest_bite(cls, omlet_name, passcode):
        eater = Eater.by_passcode(omlet_name, passcode)
        return eater.latest_bite

    # sets the latest_bite to the number given, all previous bites are assumed to be eaten
    # this should be called in conjunction with Bite.set_eaten()
    @classmethod
    def set_latest_bite(cls, omlet_name, passcode, number):
        eater = Eater.by_passcode(omlet_name, passcode)
        eater.latest_bite = number
        eater.put()

    # IMPORTANT: does not automatically put bite in database
    # if omlet does not exist, or eater already exists, returns None
    @classmethod
    def create_eater(cls, omlet_name, passcode, latest_bite = 0, email = None):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to make Eater - Omlet does not exist.')
            return None
        eater = Eater.by_passcode(passcode)
        if eater:
            print('Tried to make Eater - Eater already exists.')
            return None

        return Eater(parent = eaters_key(),
                     passcode = passcode,
                     latest_bite = latest_bite,
                     omlet_id = omlet.key().id(),
                     email = email)