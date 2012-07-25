import re, sys, json, unicodedata
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import google.appengine.api.search

class SearchResults(webapp.RequestHandler):
    def get(self):
        search_string = self.request.get('q')
        search_list = search_string.split()
        and_results = {}
        or_results = {}
        
        search_results = {}
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        i = 0
        
        # search in all the crises
        for c in crises.run():
            cd = c.__dict__
            # take out things you don't want to search in here
            cd.pop('_entity')
            
            for k, v in cd.items():
                
                vv = repr(v)[2:-1]
                regex = r'(.{0,50})(' + re.escape(search_string) + r')(.{0,50})'
                matched = re.search(regex, vv)
                
                if matched != None:
                    snippet = '...' + matched.group(1) + '<b>' + matched.group(2) + '</b>' + matched.group(3) + '...'
                    u_elemid = unicodedata.normalize('NFKD', cd['_elemid']).encode('ascii','ignore')
                    u_title = unicodedata.normalize('NFKD', cd['_name']).encode('ascii','ignore')
                    
                    result_string = ['<a href="/crises/' + u_elemid + '">' + u_title + '</a>', '<p>' + snippet + '</p>']
                    search_results[str(i)] = result_string 
                    i += 1
        
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            # take out things you don't want to search in here
            od.pop('_entity')
            
            for k, v in od.items():
                
                vv = repr(v)[2:-1]
                regex = r'(.{0,50})(' + re.escape(search_string) + r')(.{0,50})'
                matched = re.search(regex, vv)
                
                if matched != None:
                    snippet = '...' + matched.group(1) + '<b>' + matched.group(2) + '</b>' + matched.group(3) + '...'
                    u_elemid = unicodedata.normalize('NFKD', od['_elemid']).encode('ascii','ignore')
                    u_title = unicodedata.normalize('NFKD', od['_name']).encode('ascii','ignore')
                    
                    result_string = ['<a href="/organizations/' + u_elemid + '">' + u_title + '</a>', '<p>' + snippet + '</p>']
                    search_results[str(i)] = result_string 
                    i += 1
        
        for p in people.run():
            pd = p.__dict__
            # take out things you don't want to search in here
            pd.pop('_entity')
            
            for k, v in pd.items():
                
                vv = repr(v)[2:-1]
                regex = r'(.{0,50})(' + re.escape(search_string) + r')(.{0,50})'
                matched = re.search(regex, vv)
                
                if matched != None:
                    snippet = '...' + matched.group(1) + '<b>' + matched.group(2) + '</b>' + matched.group(3) + '...'
                    u_elemid = unicodedata.normalize('NFKD', pd['_elemid']).encode('ascii','ignore')
                    u_title = unicodedata.normalize('NFKD', pd['_name']).encode('ascii','ignore')

                    result_string = '<a href="/people/' + u_elemid + '">' + u_title + '</a>', '<p>' + snippet + '</p>'
                    search_results[str(i)] = result_string 
                    i += 1

        self.response.out.write(json.dumps(search_results))


application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
