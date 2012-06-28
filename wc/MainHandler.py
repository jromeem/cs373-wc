import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi, os
import cgitb; cgitb.enable()
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump


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
                    <form action="/handle" method="post" enctype="multipart/form-data">
                        <div>
                            <input id="myfile" name="myfile" type="file">
                            <input value="Upload" type="submit">
                        </div>
                    </form>
                </body>
            </html>""")
            
            
class ImportHandler(webapp.RequestHandler):
    def post(self): 
        form = cgi.FieldStorage()
        fileitem = form['myfile']
        
        
        # Test if the file was uploaded
        if fileitem.filename:
            fn = os.path.basename(fileitem.filename)
            f = fileitem.file
            message = 'The file "' + fn + '" was uploaded successfully...'
            tree = ElementTree.parse(f)
            

        else:
            message = 'No file was uploaded'
        print message + '<br/><br/><br/>'
       
        
       
        for e in tree.iter():
            print("%s - %s<br />" % (e.tag, e.text))
        


application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/import', ImportPage),('/handle', ImportHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
