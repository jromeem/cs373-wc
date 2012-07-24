import cgi, os, sys
import cgitb; cgitb.enable()
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
template.register_template_library('django.contrib.humanize.templatetags.humanize')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import django.contrib.humanize.templatetags.humanize

class SearchResults(webapp.RequestHandler):
    print "out of post!"
    def post(self):
        print "searched!"

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
