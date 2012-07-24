import cgi, os, sys
import cgitb; cgitb.enable()
"""
sys.path.append('/home/joe/Downloads/google_appengine/google')
sys.path.append('/home/joe/Downloads/google_appengine/google/appengine')
sys.path.append('/home/joe/Downloads/google_appengine/google/appengine/ext')
sys.path.append('/home/joe/Downloads/google_appengine/google/appengine/ext/webapp')
from google import appengine
from google.appengine import ext
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
template.register_template_library('django.contrib.humanize.templatetags.humanize')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import django.contrib.humanize.templatetags.humanize

# mutator for template values
# extracts the values in link and categorizes and stores them in template_values
def link_values(template_values, link):
    images = []
    imageset = set()
    videos = []
    socials = []
    externals = []
    misc_links = []
    for l in link:
        if l.link_type == 'primaryImage' or l.link_type == 'image':
            images.append(l)
            imageset.add(l.link_url)
        elif l.link_type == 'video':
            videos.append(l)
        elif l.link_type == 'social':
            socials.append(l)
        elif l.link_type == 'ext':
            externals.append(l)
        else:
            misc_links.append(l)

    template_values['ImagesSet'] = imageset
    template_values['videos'] = videos
    for v in videos:
        if v.link_site == "YouTube":
            template_values['youtube_embed'] = v.link_url[-11:]
    template_values['socials'] = socials
    template_values['externals'] = externals
    template_values['misc_links'] = misc_links
    template_values['isNotEmpty_misc'] = misc_links != []


class MainPage(webapp.RequestHandler):
    def get(self):
        headerNote = " - Import Antigravity"
        #: test documentation for images
        images = db.GqlQuery("SELECT * FROM Link WHERE link_type='primaryImage' ORDER BY link_url")
        
        template_values={'page_name': 'World Crises','team_name': 'IMPORT ANTIGRAVITY','team_members': ['Joe Peacock', 'Andy Hsu','Harrison He','Jerome Martinez','Michael Pace','Justin Salazar',], 'images' : images, 'headerNote': headerNote}
        
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))


class CrisisPage(webapp.RequestHandler):
    def get(self, crisis_id):
        assert(crisis_id is not None)
    
        crisis_query = "SELECT * FROM Crisis WHERE elemid='" + crisis_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + crisis_id + "'"
        crisis = db.GqlQuery(crisis_query)
        link = db.GqlQuery(link_query)
        headerNote = " - Import Antigravity"
        
        # elemid : title
        dict_orgrefs = {}
        dict_personrefs = {}
        
        # extract refs
        for c in crisis:
            
            # go through orgref list
            for org_elemid in c.orgrefs:
                org_query = "SELECT * FROM Organization WHERE elemid='" + org_elemid + "'"
                org = db.GqlQuery(org_query)
                for o in org:
                    dict_orgrefs[org_elemid] = o.name
                    
            # go through personrefs
            for ppl_elemid in c.personrefs:
                ppl_query = "SELECT * FROM Person WHERE elemid='" + ppl_elemid + "'"
                person = db.GqlQuery(ppl_query)
                for p in person:
                    dict_personrefs[ppl_elemid] = p.name

        template_values = { 'crisis'     : crisis,
                            'link'       : link,                            
                            'headerNote'  : headerNote,
                            'orgrefs'    : dict_orgrefs,
                            'personrefs' : dict_personrefs }
        
        link_values(template_values, link)
        
        path = os.path.join(os.path.dirname(__file__), "crisis_template.html")
        self.response.out.write(template.render(path, template_values))     

class OrganizationPage(webapp.RequestHandler):
    def get(self, org_id):
        assert(org_id is not None)
        
        org_query = "SELECT * FROM Organization WHERE elemid='" + org_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + org_id + "'"
        org = db.GqlQuery(org_query)
        link = db.GqlQuery(link_query)
        headerNote = " - Import Antigravity"

        # find refs
        dict_crisisrefs = {}
        dict_personrefs = {}
        for o in org:    
            # go though crisisrefs
            for crisis_elemid in o.crisisrefs:
                crisis_query = "SELECT * FROM Crisis WHERE elemid='" + crisis_elemid + "'"
                crisis = db.GqlQuery(crisis_query)
                for c in crisis:
                    dict_crisisrefs[crisis_elemid] = c.name
            
            # go through personrefs
            for ppl_elemid in o.personrefs:
                ppl_query = "SELECT * FROM Person WHERE elemid='" + ppl_elemid + "'"
                person = db.GqlQuery(ppl_query)
                for p in person:
                    dict_personrefs[ppl_elemid] = p.name
        
        template_values = { 'organization': org,
                            'link'        : link,
                            'headerNote'  : headerNote,
                            'crisisrefs'  : dict_crisisrefs,
                            'personrefs'  : dict_personrefs }

        link_values(template_values, link)
        
        path = os.path.join(os.path.dirname(__file__), "organization_template.html")
        self.response.out.write(template.render(path, template_values))
        
class PersonPage(webapp.RequestHandler):
    def get(self, person_id):
        assert(person_id is not None)
        
        person_query = "SELECT * FROM Person WHERE elemid='" + person_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + person_id + "'"
        person = db.GqlQuery(person_query)
        link = db.GqlQuery(link_query)
        headerNote = " - Import Antigravity"
        
        org_references = {}
        crisis_references = {}
        for p in person:
            for org_ref in p.orgrefs:
                query = db.GqlQuery("SELECT * FROM Organization WHERE elemid='" + org_ref + "'")
		for org in query:
                    org_references[org_ref] = org.name

            for crisis_ref in p.crisisrefs:
                query2 = db.GqlQuery("SELECT * FROM Crisis WHERE elemid='" + crisis_ref + "'")
		for crisis in query2:
		    crisis_references[crisis_ref] = crisis.name

        template_values = { 'person': person,
                            'link'  : link,
                            'headerNote'  : headerNote,
                            'org_references' : org_references,
                            'crisis_references' : crisis_references }

        link_values(template_values, link)
                
        path = os.path.join(os.path.dirname(__file__), "person_template.html")
        self.response.out.write(template.render(path, template_values))  
        
class CrisisSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Crisis")
        allImages = db.GqlQuery("SELECT * FROM Link WHERE link_type='primaryImage' ORDER BY link_url")
        images = []
        for c in q:
            for i in allImages:
                if c.elemid == i.link_parent:
                    images.append(i)
                    
        headerNote = " - Import Antigravity"
        
        template_values = { 'crises': q, 'images': images, 'headerNote': headerNote }
        
        path = os.path.join(os.path.dirname(__file__), "crises.html")
        self.response.out.write(template.render(path, template_values))

class OrganizationsSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Organization")
        allImages = db.GqlQuery("SELECT * FROM Link WHERE link_type='primaryImage' ORDER BY link_url")
        images = []
        for o in q:
            for i in allImages:
                if o.elemid == i.link_parent:
                    images.append(i)
        
        headerNote = " - Import Antigravity"
        
        template_values = { 'orgs': q, 'images': images, 'headerNote': headerNote }
        
        path = os.path.join(os.path.dirname(__file__), "organizations.html")
        self.response.out.write(template.render(path, template_values))

class PeopleSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Person")
        allImages = db.GqlQuery("SELECT * FROM Link WHERE link_type='primaryImage' ORDER BY link_url")
        images = []
        for p in q:
            for i in allImages:
                if p.elemid == i.link_parent:
                    images.append(i)
                    
        headerNote = " - Import Antigravity"
        
        template_values = { 'people': q, 'images': images, 'headerNote': headerNote }
        
        path = os.path.join(os.path.dirname(__file__), "people.html")
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/crises', CrisisSplashPage),
                                      ('/people', PeopleSplashPage),
                                      ('/organizations', OrganizationsSplashPage),
                                      ('/crises/', CrisisSplashPage),
                                      ('/people/', PeopleSplashPage),
                                      ('/organizations/', OrganizationsSplashPage),
                                      
                                      
                                      ('/crises/(.*)/', CrisisPage),
                                      ('/organizations/(.*)/', OrganizationPage),
                                      ('/people/(.*)/', PersonPage),
                                      ('/crises/(.*)', CrisisPage),
                                      ('/organizations/(.*)', OrganizationPage),
                                      ('/people/(.*)', PersonPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
