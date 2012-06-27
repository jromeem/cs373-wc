import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        page = self.request.get('page')
        template_values = {
            'page': page,
        }

        #path = os.path.join(os.path.dirname(__file__), page + ".html")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))
        
        
        
class ImportPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
            <html>
                <body>
                    <form action="form-handler.php" method="post" enctype="multipart/form-data">
                        <div>
                            <input id="myfile" name="myfile" type="file">
                            <input value="Upload" type="submit">
                        </div>
                    </form>
                </body>
            </html>""")



application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
