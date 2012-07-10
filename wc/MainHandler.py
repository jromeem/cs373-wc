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
        query_string = "SELECT * FROM Crisis WHERE elemid='" + crisis_id + "'"
        crisis = db.GqlQuery(query_string)

        for x in crisis:
            self.response.out.write(x.location_city + "<br />")
        
        template_values = { 'crisis': crisis }
        
        path = os.path.join(os.path.dirname(__file__), "crisis_template.html")
        self.response.out.write(template.render(path, template_values))        
        
class OrganizationPage(webapp.RequestHandler):
    def get(self, organization_id):
        q = db.GqlQuery("SELECT name FROM Organization WHERE elemid='" + organization_id + "'")
        for x in q:
            self.response.out.write(x.name + "<br />")
        

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/crisis/(.*)', CrisisPage),
                                      ('/organization/(.*)', OrganizationPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
