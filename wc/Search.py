from pprint import pprint
import re, sys, unicodedata
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person

class SearchResults(webapp.RequestHandler):
    def get(self):
        search_string = self.request.get('q')
        search_list = search_string.split()
        search_results = {}
        search_results['OR'] = {}
        search_results['AND'] = {}
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        datamodels = [crises.run(), orgs.run(), people.run()]

        AND = lambda x,y : x and y
        OR  = lambda x,y : x or y
        
        i = 0
        index = 0
        
        for kind in datamodels:
            for entity in kind:
                entity_dict = entity.__dict__
                entity_dict.pop('_entity')
                
                for key, value in entity_dict.items():
                    
                    if type(value) == type(u''):
                        target_string = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
                        target_string = target_string
                    else:
                        target_string = repr(value)
                    
                    inAll  = reduce(AND, [(s.lower() in target_string.lower()) for s in search_list], True)
                    inSome = reduce(OR,  [(s.lower() in target_string.lower()) for s in search_list], False)

                    elemid = unicodedata.normalize('NFKD', entity_dict['_elemid']).encode('ascii','ignore')
                    title = unicodedata.normalize('NFKD', entity_dict['_name']).encode('ascii','ignore')
                    
                    link_string = '<a href="/'
                    if index == 0:
                        link_string += 'crises/'
                    elif index == 1:
                        link_string += 'organizations/'
                    else:
                        link_string += 'people/'
                    link_string += elemid + '">' + title + '</a>'
                    for s in search_list :
                        target_string = target_string.replace(s, '<b><FONT style="BACKGROUND-COLOR: yellow">'+s+'</FONT></b>')
                    snippet = '...' + target_string + '...'
                    
                    snippet = snippet.replace('\.\.\...', '...')
                    snippet = snippet.replace('.\.\.\.', '...')
                    snippet = snippet.replace('\\u', '')
                    snippet = snippet.replace('\\n', '')
                    snippet = snippet.replace('\\t', '')

                    result = [link_string, '<p>' + snippet + '</p>']
                    if inAll:
                        search_results['AND'][str(i)] = result
                    if inSome:
                        search_results['OR'][str(i)] = result
                    i+=1
                    
            index+=1
        
        self.response.out.write(simplejson.dumps(search_results))

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
