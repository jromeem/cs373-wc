import re, sys, json, unicodedata
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
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
                    # hacked way of converting unicode -> ascii
                    elemid = repr(cd['_elemid'])[2:-1]
                    title = repr(cd['_name'])[2:-1]
                    result_string = '<a href="/crises/' + elemid + '">' + title + '</a>'
                    
                    search_results[str(i)] = result_string 
                    i += 1
        
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            
            for k, v in od.items():
                vv = repr(v)
                if search_string in vv:
                    # hacked way of converting unicode -> ascii
                    elemid = repr(od['_elemid'])[2:-1]
                    title = repr(od['_name'])[2:-1]
                    result_string = '<a href="/organizations/' + elemid + '">' + title + '</a>'
                    
                    search_results[str(i)] = result_string
                    i += 1
        
        for p in people.run():
            pd = p.__dict__
            
            for k, v in pd.items():
                vv = repr(v)
                if search_string in vv:
                    # hacked way of converting unicode -> ascii
                    elemid = repr(pd['_elemid'])[2:-1]
                    title = repr(pd['_name'])[2:-1]
                    result_string = '<a href="/people/' + elemid + '">' + title + '</a>'
                    
                    search_results[str(i)] = result_string
                    i += 1

        self.response.out.write(json.dumps(search_results))

        '''
        search_string = self.request.get('q')
        search_results = []
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        # search in all the crises
        for c in crises.run():
            cd = c.__dict__
            
            for k, v in cd.items():
                vv = repr(v)
                if search_string in vv:
                    #fields = ('crises', repr(cd['_elemid'])[2:-1], repr(cd['_name'])[2:-1])
                    search_results.append(cd['_elemid'])
        
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            
            for k, v in od.items():
                vv = repr(v)
                if search_string in vv:
                    #fields = ('organizations', repr(cd['_elemid'])[2:-1], repr(cd['_name'])[2:-1])
                    search_results.append(cd['_elemid'])

        # search in all crises
        for p in people.run():
            pd = p.__dict__
            
            for k, v in pd.items():
                vv = repr(v)
                if search_string in vv:
                    #fields = ('people', repr(cd['_elemid'])[2:-1], repr(cd['_name'])[2:-1])
                    search_results.append(cd['_elemid'])

        for x in search_results:
            self.response.out.write(x)
            
        #self.response.out.write(json.dumps(search_results))
        '''

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()