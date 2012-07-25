import re, sys, json, unicodedata
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
template.register_template_library('django.contrib.humanize.templatetags.humanize')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import django.contrib.humanize.templatetags.humanize
import google.appengine.api.search

class SearchResults(webapp.RequestHandler):
    def get(self):        
        
        search_string = self.request.get('q')
        search_results = {}
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        i = 0
        
        # search in all the crises
        for c in crises.run():
            cd = c.__dict__
            
            for k, v in cd.items():
                vv = repr(v)
                if search_string in vv:
                    temp = unicodedata.normalize('NFKD', cd['_elemid']).encode('ascii','ignore')
                    search_results[str(i)] = temp 
                    i += 1
        
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            
            for k, v in od.items():
                vv = repr(v)
                if search_string in vv:
                    temp = unicodedata.normalize('NFKD', od['_elemid']).encode('ascii','ignore')
                    search_results[str(i)] = temp
                    i += 1
        
        for p in people.run():
            pd = p.__dict__
            
            for k, v in pd.items():
                vv = repr(v)
                if search_string in vv:
                    temp = unicodedata.normalize('NFKD', pd['_elemid']).encode('ascii','ignore')
                    search_results[str(i)] = temp
                    i += 1

        self.response.out.write(json.dumps(search_results))
        
    

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
