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
        search_results = []
        self.response.out.write('Results for: ' + search_string + '<hr>')
        
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        
        # search in all the crises
        for c in crises.run():
            self.response.out.write('<br>')
            self.response.out.write(repr(c))
            cd = c.__dict__
            
            for k, v in cd.items():
                vv = repr(v)
                if search_string in vv:
                    search_results.append(cd['_elemid'])
                    
            self.response.out.write('<br>')

        self.response.out.write(repr(search_results))
        
        """

        # search in all the orgs
        for o in orgs.run():
            self.response.out.write('<br>')
            self.response.out.write(repr(o))
            od = o.__dict__
            
            for k, v in od.items():
                vv = repr(v)
                if search_string in vv:
                    search_results.append(od['_elemid'])
                    
            print ''

        for p in people.run():
            self.response.out.write('<br>')
            self.response.out.write(repr(p))
            pd = p.__dict__
            
            for k, v in cd.items():
                vv = repr(v)
                if search_string in vv:
                search_results.append(pd['_elemid'])
            
            self.response.out.write('<br>')

        self.response.out.write(repr(search_results))
        """
    

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
