import unittest
from google.appengine.ext import testbed

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from DataModels import Person, Organization, Crisis, Link
from MainHandler import link_values

class ExportLinks(unittest.TestCase):

    # test class mutator for extracting links
    def test_crisisLink(dictionary, link):
        
        link_query = "SELECT * FROM Link WHERE link_parent='haiti'"
        link = db.GqlQuery(link_query)

        dictionary = {}
        self.assert_(len(dictionary) == 0)
        link_values(dictionary, link)
        self.assert_(len(dictionary) != 0)

    def test_orgsLinks(dictionary, link):
        
        link_query = "SELECT * FROM Link WHERE link_parent='wfp'"
        link = db.GqlQuery(link_query)

        dictionary = {}
        self.assert_(len(dictionary) == 0)
        link_values(dictionary, link)
        self.assert_(len(dictionary) != 0)

    def trst_personLinks(dictionary, link):
        
        link_query = "SELECT * FROM Link WHERE link_parent='aroche'"
        link = db.GqlQuery(link_query)

        dictionary = {}
        self.assert_(len(dictionary) == 0)
        link_values(dictionary, link)
        self.assert_(len(dictionary) != 0)
        
        
