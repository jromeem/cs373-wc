import cgi, os
import cgitb; cgitb.enable()
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person


class MainPage(webapp.RequestHandler):
    def get(self):
        page = self.request.get('page')
        template_values = { 'page': page }
        
        template_values={'page_name': 'World Crises','team_name': 'IMPORT ANTIGRAVITY','team_members': ['Joe Peacock', 'Andy Hsu','Harrison He','Jerome Martinez','Michael Pace','Justin Salazar',]}
        
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))


class OldMainPage(webapp.RequestHandler):
    def get(self):
        page = self.request.get('page')
        template_values = { 'page': page }
        
        path = os.path.join(os.path.dirname(__file__), "oldindex.html")
        self.response.out.write(template.render(path, template_values))


class PersonPage(webapp.RequestHandler):
    def get(self, person_id):
        q = db.GqlQuery("SELECT * FROM Person WHERE elemid='" + person_id + "'")
        for x in q:
            self.response.out.write(x.name + "<br />")

class CrisisPage(webapp.RequestHandler):
    def get(self, crisis_id):
        crisis_query = "SELECT * FROM Crisis WHERE elemid='" + crisis_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + crisis_id + "'"
        crisis = db.GqlQuery(crisis_query)
        link = db.GqlQuery(link_query)

        # find titles in orgrefs/personrefs
        # elemid : title
        dict_orgrefs = {}
        dict_personrefs = {}
        # extract orgrefs list
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
                    
        self.response.out.write(dict_orgrefs)

        template_values = { 'crisis'     : crisis,
                            'link'       : link,
                            'orgrefs'    : dict_orgrefs,
                            'personrefs' : dict_personrefs }

        # categorize and populte links
        images = []
        videos = []
        socials = []
        externals = []
        misc_links = []
        for l in link:
            if l.link_type == 'primaryImage':
                images.append(l)
            elif l.link_type == 'video':
                videos.append(l)
            elif l.link_type == 'social':
                socials.append(l)
            elif l.link_type == 'ext':
                externals.append(l)
            else:
                misc_links.append(l)

        template_values['images'] = images
        template_values['videos'] = videos
        for v in videos:
            if v.link_site == "YouTube":
                template_values['youtube_embed'] = v.link_url[-11:]
        template_values['socials'] = socials
        template_values['externals'] = externals
        template_values['misc_links'] = misc_links
        template_values['isNotEmpty_misc'] = misc_links != []
                
        path = os.path.join(os.path.dirname(__file__), "crisis_template.html")
        self.response.out.write(template.render(path, template_values))     

class OrganizationPage(webapp.RequestHandler):
    def get(self, org_id):
        org_query = "SELECT * FROM Organization WHERE elemid='" + org_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + org_id + "'"
        org = db.GqlQuery(org_query)
        link = db.GqlQuery(link_query)

        template_values = { 'organization': org,
                            'link'  : link    }
                            
        # categorize and populte links
        images = []
        videos = []
        socials = []
        externals = []
        misc_links = []
        for l in link:
            if l.link_type == 'primaryImage':
                images.append(l)
            elif l.link_type == 'video':
                videos.append(l)
            elif l.link_type == 'social':
                socials.append(l)
            elif l.link_type == 'ext':
                externals.append(l)
            else:
                misc_links.append(l)

        template_values['images'] = images
        template_values['videos'] = videos
        for v in videos:
            if v.link_site == "YouTube":
                template_values['youtube_embed'] = v.link_url[-11:]
        template_values['socials'] = socials
        template_values['externals'] = externals
        template_values['misc_links'] = misc_links
        template_values['isNotEmpty_misc'] = misc_links != []
                
        path = os.path.join(os.path.dirname(__file__), "organization_template.html")
        self.response.out.write(template.render(path, template_values))
        
class PersonPage(webapp.RequestHandler):
    def get(self, person_id):
        person_query = "SELECT * FROM Person WHERE elemid='" + person_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + person_id + "'"
        person = db.GqlQuery(person_query)
        link = db.GqlQuery(link_query)

        template_values = { 'person': person,
                            'link'  : link    }

        # categorize and populte links
        images = []
        videos = []
        socials = []
        externals = []
        misc_links = []
        for l in link:
            if l.link_type == 'primaryImage':
                images.append(l)
            elif l.link_type == 'video':
                videos.append(l)
            elif l.link_type == 'social':
                socials.append(l)
            elif l.link_type == 'ext':
                externals.append(l)
            else:
                misc_links.append(l)

        template_values['images'] = images
        template_values['videos'] = videos
        for v in videos:
            if v.link_site == "YouTube":
                template_values['youtube_embed'] = v.link_url[-11:]
        template_values['socials'] = socials
        template_values['externals'] = externals
        template_values['misc_links'] = misc_links
        template_values['isNotEmpty_misc'] = misc_links != []
                
        path = os.path.join(os.path.dirname(__file__), "person_template.html")
        self.response.out.write(template.render(path, template_values))  
        
class CrisisSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Crisis")
        template_values = { 'crises': q }
        
        path = os.path.join(os.path.dirname(__file__), "crises.html")
        self.response.out.write(template.render(path, template_values))

class OrganizationsSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Organization")
        template_values = { 'orgs': q }
        
        path = os.path.join(os.path.dirname(__file__), "organizations.html")
        self.response.out.write(template.render(path, template_values))

class PeopleSplashPage(webapp.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Person")
        template_values = { 'people': q }
        
        path = os.path.join(os.path.dirname(__file__), "people.html")
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([('/', MainPage), 
									  ('/crises', CrisisSplashPage),
									  ('/people', PeopleSplashPage),
									  ('/organizations', OrganizationsSplashPage),
                                      ('/crises/(.*)', CrisisPage),
                                      ('/organizations/(.*)', OrganizationPage),
                                      ('/people/(.*)', PersonPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
