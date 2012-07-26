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
        search_results = {}
        search_results['OR'] = {}
        search_results['AND'] = {}
        
        crises = db.GqlQuery("SELECT * FROM Crisis")
        people = db.GqlQuery("SELECT * FROM Person")
        orgs   = db.GqlQuery("SELECT * FROM Organization")
        
        i = 0

        regexOR = r'(.*)(' + re.escape(search_string) + r')(.*)'
        regexOR_obj = re.compile(regexOR, re.IGNORECASE)
        
        datamodels = [crises.run(), orgs.run(), people.run()]

        index = 0
        for kind in datamodels:
            for entity in kind:
                entity_dict = entity.__dict__
                # take out things you don't want to search in here
                entity_dict.pop('_entity')
                for key, value in entity_dict.items():
                    if type(value) == type(u''):
                        # convert from unicode
                        target_string = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
                        target_string = target_string
                    else:
                        target_string = repr(value)
                    matchedOR = regexOR_obj.match(target_string)
                    
                    elemid = unicodedata.normalize('NFKD', entity_dict['_elemid']).encode('ascii','ignore')
                    title = unicodedata.normalize('NFKD', entity_dict['_name']).encode('ascii','ignore')
                    
                    # AND
                    regexAnd = ''
                    for s in search_list:
                        regexAnd += '(' + s + ')|'
                    regexAnd = regexAnd[:-1]
                    regexAnd_obj = re.compile(regexAnd, re.IGNORECASE)
                    m = regexAnd_obj.match(target_string)
                    for x in range(1, len(search_list)+1):
                        if not m.group(x):
                            break
                    else:
                        for x in range(1, len(search_list)+1):
                            snippet = target_string.replace(m.group(x), '<b>' + m.group(x) + '</b>')
                        snippet = '...' + result_string + '...'
                        link_string = '<a href="/'
                        if index == 0:
                            link_string += 'crises/'
                        elif index == 1:
                            link_string += 'organizations/'
                        else:
                            link_string += 'people/'
                        link_string += elemid + '">' + title + '</a>'
                        
                        snippet = re.sub(r'\.\.\.\[?u.', r'...', snippet)
                        snippet = re.sub(r'\'\.\.\.', r'...', snippet)
                        snippet = re.sub(r'\\u', r'', snippet)
                        
                        result_string = [link_string, '<p>' + snippet + '</p>']
                        search_results['AND'][str(i)] = result_string 
                        i += 1
                        
                    
                    # OR
                    if matchedOr != None:
                        snippet = '...' + matchedOr.group(1) + '<b>' + matchedOr.group(2) + '</b>' + matchedOr.group(3) + '...'
    
                        link_string = '<a href="/'
                        if index == 0:
                            link_string += 'crises/'
                        elif index == 1:
                            link_string += 'organizations/'
                        else:
                            link_string += 'people/'
                        link_string += elemid + '">' + title + '</a>'
                        
                        snippet = re.sub(r'\.\.\.\[?u.', r'...', snippet)
                        snippet = re.sub(r'\'\.\.\.', r'...', snippet)
                        snippet = re.sub(r'\\u', r'', snippet)
                        
                        result_string = [link_string, '<p>' + snippet + '</p>']
                        search_results['OR'][str(i)] = result_string 
                        i += 1
            index += 1

        self.response.out.write(json.dumps(search_results))



application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
