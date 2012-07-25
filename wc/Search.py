import re, sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
template.register_template_library('django.contrib.humanize.templatetags.humanize')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import django.contrib.humanize.templatetags.humanize

import google.appengine.api.search

class SearchResults(webapp.RequestHandler):
    def post(self):        
        
        search_string = self.request.get('q')
        search_results = set([])
        self.response.out.write('Results for: ' + search_string + '<hr>')
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        # search in all the crises
        for c in crises.run():
            cd = c.__dict__
            
            for k, v in cd.items():
                vv = repr(v)
                if search_string in vv:
                    search_results.add(cd['_elemid'])
        
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            
            for k, v in od.items():
                vv = repr(v)
                if search_string in vv:
                    search_results.add(od['_elemid'])
        
        for p in people.run():
            pd = p.__dict__
            
            for k, v in pd.items():
                vv = repr(v)
                if search_string in vv:
                    search_results.add(pd['_elemid'])

        self.response.out.write(repr(search_results))
        for s in search_results:
            self.response.out.write(s)
            self.response.out.write('<br>')
        
    

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
