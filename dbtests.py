import json

import webapp2
import jinja2

from google.appengine.ext import db
from userdb import User
from omletdb import Omlet
from eaterdb import Eater
from bitedb import Bite

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

def test_function(self):
    test_username = self.user.name
    self.write('<br>username is: ' + test_username)
    user = User.by_name(test_username)
    self.write('<br>user.id() is: ' + str(user.key().id()))

    # # FOR DELETING
    # delete_for_user(self, test_username)

    omlet1 = Omlet.make_omlet(test_username, 'first')
    if omlet1:
        omlet1.put()
    self.write('<br><br>put in omlet called "first" ')
    self.write('<br>list of omlets for this user is ' + string_list_omlet(Omlet.list_username(test_username)))
    self.write('<br>look, the omlet exists: ' + string_omlet(Omlet.by_name('first')))

    self.write('<br><br>this should be empty: ' + string_list_bite(Bite.list_omlet_until_number('first', None)))
    make_bite_noduplicate('first', 'Bite AAAAA')
    make_bite_noduplicate('first', 'This is bite B of omlet1')
    self.write('<br>this should have two bites: ' + string_list_bite(Bite.list_omlet_until_number('first', None)))

    # DEBUGGING CONCURRENCY ISSUES
    list_all_bites_descending(self, 'first')

    # make_bite_noduplicate('first', 'Bite C')
    # # DEBUGGING CONCURRENCY ISSUES
    # list_all_bites_descending(self, 'first')

    # make_bite_noduplicate('first', 'Bite D, yay')
    # make_bite_noduplicate('first', 'Nom, Bite E')
    # self.write('<br> want up to bite C: ' + string_list_bite(Bite.list_omlet_until_number('first', 3)))
    # self.write('<br> want bite D only: ' + string_bite(Bite.by_omlet_number('first', 4)))

    # Bite.set_eaten('first', 2)
    # self.write('has bite B been eaten? should be yes: ' + Bite.by_omlet_number('first', 2))

    # omlet2 = Omlet.make_omlet(test_username, 'second')
    # omlet2.put()
    # omlet3 = Omlet.make_omlet(test_username, 'third')
    # omlet3.put()
    # omlet4 = Omlet.make_omlet(test_username'fourth')
    # omlet4.put()
    # self.write('list of omlets for this user should have 4: ' + Omlet.list_username(test_username))

