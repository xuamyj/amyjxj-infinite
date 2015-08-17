# For Omelette database stuff

import random
import hashlib
from string import letters

from google.appengine.ext import db

def eaters_key(group = 'default'):
    return db.Key.from_path('eaters', group)

class Eater(db.Model):
    passcode_hash = db.StringProperty(required = True)
    latest_bite = db.IntegerProperty(required = True)