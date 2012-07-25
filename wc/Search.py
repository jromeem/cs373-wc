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

        regex = r'(.{0,50})(' + re.escape(search_string) + r')(.{0,50})'
        regex_obj = re.compile(regex, re.IGNORECASE)
        
        datamodels = [crises.run(), orgs.run(), people.run()]

        index = 0
        for kind in datamodels:
            
            for entity in kind:    
                entity_dict = entity.__dict__
                # take out things you don't want to search in here
                entity_dict.pop('_entity')
                
                for key, value in entity_dict.items():
                    # only parse normalized strings and unicode strings
                    if type(value) == type(1L) or value == None:
                        break
                    
                    # convert to unicode
                    target_string = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
                    matched = regex_obj.match(target_string)
                    
                    if matched != None:
                        snippet = '...' + matched.group(1) + '<b>' + matched.group(2) + '</b>' + matched.group(3) + '...'
                        elemid = unicodedata.normalize('NFKD', entity_dict['_elemid']).encode('ascii','ignore')
                        title = unicodedata.normalize('NFKD', entity_dict['_name']).encode('ascii','ignore')

                        link_string = '<a href="/'
                        if index == 0:
                            link_string += 'crisis'
                        elif index == 1:
                            link_string += 'organizations'
                        else:
                            link_string += 'people'
                        link_string += elemid + '">' + title + '</a>'

                        print link_string
                        
                        result_string = [link_string, '<p>' + snippet + '</p>']
                        search_results[str(i)] = result_string 
                        i += 1

        '''
        # search in all the orgs
        for o in orgs.run():
            od = o.__dict__
            # take out things you don't want to search in here
            od.pop('_entity')
            
            for k, v in od.items():
                # only parse normalized strings and unicode strings
                if type(v) == type(1L) or v == None:
                    break
                
                # convert to unicode
                vv = unicodedata.normalize('NFKD', v).encode('ascii','ignore')
                
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
                # only parse normalized strings and unicode strings
                if type(v) == type(1L) or v == None:
                    break
                
                # convert to unicode
                vv = unicodedata.normalize('NFKD', v).encode('ascii','ignore')
                
                regex = r'(.{0,50})(' + re.escape(search_string) + r')(.{0,50})'
                matched = re.search(regex, vv)
                
                if matched != None:
                    snippet = '...' + matched.group(1) + '<b>' + matched.group(2) + '</b>' + matched.group(3) + '...'
                    u_elemid = unicodedata.normalize('NFKD', pd['_elemid']).encode('ascii','ignore')
                    u_title = unicodedata.normalize('NFKD', pd['_name']).encode('ascii','ignore')

                    result_string = '<a href="/people/' + u_elemid + '">' + u_title + '</a>', '<p>' + snippet + '</p>'
                    search_results[str(i)] = result_string 
                    i += 1
        '''

        self.response.out.write(json.dumps(search_results))


application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
