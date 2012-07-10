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
        query_string = "SELECT * FROM Crisis WHERE elemid='" + crisis_id + "'"
        query = db.GqlQuery(query_string)
        output = ""
        self.response.out.write(x.name + "<br />")
        
class OrganizationPage(webapp.RequestHandler):
    def get(self, organization_id):
        q = db.GqlQuery("SELECT * FROM Organization WHERE elemid='" + organization_id + "'")
        for x in q:
            self.response.out.write(x.name + "<br />")
        

application = webapp.WSGIApplication([('/', MainPage),('/om', OldMainPage),
                                      ('/crisis/(.*)', CrisisPage),
                                      ('/organization/(.*)', OrganizationPage),
                                      ('/person/(.*)', PersonPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
