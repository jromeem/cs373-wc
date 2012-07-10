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
        
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))

class CrisisPage(webapp.RequestHandler):
    def get(self, crisis_id):
        crisis_query = "SELECT * FROM Crisis WHERE elemid='" + crisis_id + "'"
        link_query = "SELECT * FROM Link WHERE link_parent='" + crisis_id + "'"
        crisis = db.GqlQuery(crisis_query)
        link = db.GqlQuery(link_query)

        template_values = { 'crisis': crisis,
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
                
        path = os.path.join(os.path.dirname(__file__), "crisis_template.html")
        self.response.out.write(template.render(path, template_values))     

class OrganizationPage(webapp.RequestHandler):
    def get(self, organization_id):
        q = db.GqlQuery("SELECT name FROM Organization WHERE elemid='" + organization_id + "'")
        for x in q:
            self.response.out.write(x.name + "<br />")

class PersonPage(webapp.RequestHandler):
    def get(self, person_id):
        q = db.GqlQuery("SELECT name FROM Person WHERE elemid='" + person_id + "'")
        for x in q:
            self.response.out.write(x.name + "<br />")
        
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
