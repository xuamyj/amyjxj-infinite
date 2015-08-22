# For Omelette database stuff

from google.appengine.ext import db
from omletdb import Omlet

def bites_key(group = 'default'):
    return db.Key.from_path('bites', group)

class Bite(db.Model):
    number = db.IntegerProperty(required = True)
    text = db.StringProperty(required = True)
    eaten = db.BooleanProperty(required = True)
    omlet_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return Bite.get_by_id(uid, parent = bites_key())

    # this function used for testing
    @classmethod
    def by_omlet_text(cls, omlet_name, text):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to find Bite - Omlet does not exist.')
            return None
        bite = Bite.all().filter('omlet_id = ', omlet.key().id()).filter(
            'text =', text).get()
        return bite

    # there should be only one bite associated with a particular omlet+number
    @classmethod
    def by_omlet_number(cls, omlet_name, number):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to find Bite - Omlet does not exist.')
            return None
        bite = Bite.all().filter('omlet_id = ', omlet.key().id()).filter(
            'number =', number).get()
        return bite

    # returns list of all the bites from 1 to max_number from a particular omlet
    # if None is passed into max_number, returns list of all the bites form this omlet
    @classmethod
    def list_omlet_until_number(cls, omlet_name, max_number):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to find Bite - Omlet does not exist.')
            return None
        bite_query = Bite.all().filter('omlet_id = ', omlet.key().id()).order('number')
        if not max_number:
            return bite_query.run()
        else:
            return bite_query.run(limit = max_number)
        return bite_query

    # set this omlet bite as eaten. once eaten, cannot be uneaten
    # (nothing in this app is deletable... for now. 8/17/15)
    # this should be called in conjunction with Eater.set_latest_bite()
    @classmethod
    def set_eaten(cls, omlet_name, number):
        bite = Bite.by_omlet_number(omlet_name, number)
        bite.eaten = True
        bite.put()

    # by default, bites are numbered in the order they are added.
    # IMPORTANT: does not automatically put bite in database
    # if omlet does not exist, returns None
    @classmethod
    def make_bite(cls, omlet_name, text):
        omlet = Omlet.by_name(omlet_name)
        if not omlet:
            print('Tried to make Bite - Omlet does not exist.')
            return None

        latest_bite = Bite.all().filter('omlet_id = ', omlet.key().id()).order('-number').get()
        next_number = 1
        if latest_bite:
            next_number = latest_bite.number + 1;

        return Bite(parent = bites_key(),
                    number = next_number,
                    text = text,
                    eaten = False,
                    omlet_id = omlet.key().id())





