import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
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
            <form action="/import" method="post" enctype="multipart/form-data">
            <div>
            <input id="myfile" name="myfile" type="file">
            <input value="Upload" type="submit">
            </div>
            </form>
            </body>
            </html>""")
            
    def post(self):
        form = cgi.FieldStorage()
        fileitem = form['myfile']
        
        
        # Test if the file was uploaded
        if fileitem.filename:
            fn = os.path.basename(fileitem.filename)
            f = fileitem.file
            message = 'The file "' + fn + '" was uploaded successfully...'
            
            f = f.read()
            
            parser = ElementTree.XMLParser(encoding="utf-8")
            
            tree = ElementTree.fromstring(f, parser)
            

        else:
            message = 'No file was uploaded'
        print message + '<br/><br/><br/>'
         
        crises = tree.findall(".//crisis")
        
        people = tree.findall(".//person")
        
        orgs = tree.findall(".//organization")
        
        for crisis in crises:
            print crisis.items()
            print "</br>"
            
        for person in people:
            print person.items()
            print "</br>"
            
        for org in orgs:
            print org.items()
            print "</br>"   
            
            
            
            
class Organization(db.Model):

    name = db.StringProperty()
    #info = db.ReferenceProperty(Info)
    

application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
