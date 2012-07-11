import cgi, os
from pprint import pprint
import cgitb; cgitb.enable()
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person

class Page(webapp.RequestHandler):
    def get(self):
        query = "SELECT * FROM Crisis"
        crises = db.GqlQuery(query)

        crisis_properties = None
        for c in crises:
            crisis_properties = crisis.properties()

        pprint(crisis_properties)
