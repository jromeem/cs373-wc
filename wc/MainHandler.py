import cgi, os
import cgitb; cgitb.enable()
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MainPage(webapp.RequestHandler):
    def get(self):
        page = self.request.get('page')
        template_values = { 'page': page }
        
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))

class TestPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("go page -- hello world!")
        

application = webapp.WSGIApplication([('/', MainPage), ('/go', TestPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
