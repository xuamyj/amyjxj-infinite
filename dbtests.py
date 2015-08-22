import json

import webapp2
import jinja2

from google.appengine.ext import db
from userdb import User
from omletdb import Omlet
from eaterdb import Eater
from bitedb import Bite

import time

def string_list_omlet(omlets):
    if not omlets:
        print('List of omlets does not exist.')
        return ''
    liststring = ''
    for om in omlets:
        liststring += '[' + string_omlet(om) + '], '
    return liststring

def string_omlet(omlet):
    if not omlet:
        return ''
    omstring = omlet.name + ' ' + str(omlet.user_id) + ' ' + str(omlet.key().id())
    return omstring

def string_list_bite(bites):
    if not bites:
        print('List of bites does not exist.')
        return ''
    liststring = ''
    for bi in bites:
        liststring += '[' + string_bite(bi) + '], '
    return liststring

def string_bite(bite):
    if not bite:
        return ''
    if bite.eaten:
        bistring = (str(bite.number) + ' | ' + bite.text + ' | EATEN | ' + str(bite.omlet_id))
    else:
        bistring = (str(bite.number) + ' | ' + bite.text + ' | NOT-EATEN | ' + str(bite.omlet_id))
    return bistring

def delete_for_user(self, test_username):
    # DELETE OMLETS
    delete_list = Omlet.list_username(test_username)
    for om in delete_list:

        # DELETE BITES
        bite_list = Bite.list_omlet_until_number(om.name, None)
        for bi in bite_list:
            bi.delete()
            self.write('<br>deleted a bite')

        om.delete()
        self.write('<br>deleted an omlet')

def make_bite_noduplicate(omlet_name, text):
    new_bite = Bite.by_omlet_text(omlet_name, text)
    if not new_bite:
        new_bite = Bite.make_bite(omlet_name, text)
        new_bite.put()
    else:
        print('make_bite_noduplicate: This bite is a duplicate, will not be re-made')

def list_all_bites_descending(self, omlet_name):
    omlet = Omlet.by_name(omlet_name)
    all_bites_desc = Bite.all().filter('omlet_id = ', omlet.key().id()).order('-number').run()
    self.write('<br><br>this should list all bites descending: ' + string_list_bite(all_bites_desc))

# archived test function
def omlet_bite_test(self):
    test_username = self.user.name
    self.write('<br>username is: ' + test_username)
    user = User.by_name(test_username)
    self.write('<br>user.id() is: ' + str(user.key().id()))

    # # FOR DELETING
    # delete_for_user(self, test_username)

    omlet1 = Omlet.make_omlet(test_username, 'first')
    if omlet1:
        omlet1.put()
    time.sleep(0.5)
    self.write('<br><br>put in omlet called "first" ')
    self.write('<br>list of omlets for this user is ' + string_list_omlet(Omlet.list_username(test_username)))
    self.write('<br>look, the omlet exists: ' + string_omlet(Omlet.by_name('first')))

    self.write('<br><br>this should be empty: ' + string_list_bite(Bite.list_omlet_until_number('first', None)))
    make_bite_noduplicate('first', 'Bite AAAAA')
    time.sleep(0.5)
    make_bite_noduplicate('first', 'This is bite B of omlet1')
    time.sleep(0.5)
    self.write('<br>this should have two bites: ' + string_list_bite(Bite.list_omlet_until_number('first', None)))

    make_bite_noduplicate('first', 'Bite C')
    time.sleep(0.5)
    make_bite_noduplicate('first', 'Bite D, yay')
    time.sleep(0.5)
    make_bite_noduplicate('first', 'Nom, Bite E')
    time.sleep(0.5)
    self.write('<br><br> want up to bite C: ' + string_list_bite(Bite.list_omlet_until_number('first', 3)))
    self.write('<br> want bite D only: ' + string_bite(Bite.by_omlet_number('first', 4)))

    Bite.set_eaten('first', 2)
    time.sleep(0.5)
    self.write('<br>has bite B been eaten? should be yes: ' + string_bite(Bite.by_omlet_number('first', 2)))

    omlet2 = Omlet.make_omlet(test_username, 'second')
    if omlet2:
        omlet2.put()
    time.sleep(0.5)
    omlet3 = Omlet.make_omlet(test_username, 'third')
    if omlet3:
        omlet3.put()
    time.sleep(0.5)
    omlet4 = Omlet.make_omlet(test_username, 'fourth')
    if omlet4:
        omlet4.put()
    time.sleep(0.5)
    self.write('<br><br>list of omlets for this user should have 4: ' + string_list_omlet(Omlet.list_username(test_username)))

def my_txn():
    test_username = self.user.name
    self.write('<br>username is: ' + test_username)
    user = User.by_name(test_username)
    self.write('<br>user.id() is: ' + str(user.key().id()))

    # FOR DELETING
    delete_for_user(self, test_username)

    omlet1 = Omlet.make_omlet(test_username, 'amy1')
    if omlet1:
        omlet1.put()
    self.write('<br><br>put in omlet called "amy1" ')
    self.write('<br>list of omlets for this user is ' + string_list_omlet(Omlet.list_username(test_username)))
    self.write('<br>look, the omlet exists: ' + string_omlet(Omlet.by_name('amy1')))

    self.write('<br><br>this should be empty: ' + string_list_bite(Bite.list_omlet_until_number('amy1', None)))
    make_bite_noduplicate('amy1', 'Bite AAAAA')
    make_bite_noduplicate('amy1', 'This is bite B of omlet1')
    self.write('<br>this should have two bites: ' + string_list_bite(Bite.list_omlet_until_number('amy1', None)))

    make_bite_noduplicate('amy1', 'Bite C')
    make_bite_noduplicate('amy1', 'Bite D, yay')
    make_bite_noduplicate('amy1', 'Nom, Bite E')
    self.write('<br><br> want up to bite C: ' + string_list_bite(Bite.list_omlet_until_number('amy1', 3)))
    self.write('<br> want bite D only: ' + string_bite(Bite.by_omlet_number('amy1', 4)))


def test_function(self):
    xg_on = db.create_transaction_options(xg=True)

    def my_txn():
        test_username = self.user.name
        self.write('<br>username is: ' + test_username)
        print('username is: ' + test_username)
        user = User.by_name(test_username)
        self.write('<br>user.id() is: ' + str(user.key().id()))
        print('user.id() is: ' + str(user.key().id()))

        # FOR DELETING
        delete_for_user(self, test_username)

        omlet1 = Omlet.make_omlet(test_username, 'amy1')
        print('omletparent', omlet1.parent().key().id());
        print('user', user.key().id())
        print('omlet:' + omlet1.name)
        key1 = omlet1.put()
        print('omlet1 newkey:', key1.id())
        omlet2 = Omlet.get_by_id(key1.id(),
            parent = user,
            read_policy = db.STRONG_CONSISTENCY)
        print('omlet2: ' + omlet2.name)
        self.write('<br><br>put in omlet called "amy1" ')
        self.write('<br>list of omlets for this user is ' + string_list_omlet(Omlet.list_username(test_username)))
        self.write('<br>look, the omlet exists: ' + string_omlet(Omlet.by_name('amy1')))

        self.write('<br><br>this should be empty: ' + string_list_bite(Bite.list_omlet_until_number('amy1', None)))
        make_bite_noduplicate('amy1', 'Bite AAAAA')
        make_bite_noduplicate('amy1', 'This is bite B of omlet1')
        self.write('<br>this should have two bites: ' + string_list_bite(Bite.list_omlet_until_number('amy1', None)))

        make_bite_noduplicate('amy1', 'Bite C')
        make_bite_noduplicate('amy1', 'Bite D, yay')
        make_bite_noduplicate('amy1', 'Nom, Bite E')
        self.write('<br><br> want up to bite C: ' + string_list_bite(Bite.list_omlet_until_number('amy1', 3)))
        self.write('<br> want bite D only: ' + string_bite(Bite.by_omlet_number('amy1', 4)))

    db.run_in_transaction_options(xg_on, my_txn)

