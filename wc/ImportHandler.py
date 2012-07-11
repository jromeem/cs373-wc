# Group Import Antigravity
# ImportHandler.py

import cgi, os
import cgitb; cgitb.enable()
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from XMLHelpers import validXML, parseXML
        
##################
# IMPORT HANDLER #
##################

class ImportPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
        <html>
            <head><link rel="stylesheet" type="text/css" href="stylesheets/main.css" /></head>
          <body>
            <div id="wrapper"><div id="content">
            <form action="/import" method="post" enctype="multipart/form-data">
              <div>
                <input id="myfile" name="myfile" type="file"><br /><br />
                <input value="Upload" type="submit">
              </div>
            </form>
            <a href="/">Home</a>
            </div></div>
          </body>
        </html>""")
            
    def post(self):        
        form = cgi.FieldStorage()
        file_item = form['myfile']
        content = form.getvalue('myfile')

        # check if file was uploaded
        if not file_item.filename:
            message = 'Error: No file was uploaded. Try again? </br>'
        
        else:
            file_name = os.path.basename(file_item.filename)
            in_file = file_item.file
            message = 'The file "' + file_name + '" was uploaded successfully '

            # check if uploaded file is a valid xml_instance
            if not validXML(content, "wc.xsd"):
                message = "Error: " + message + "but the file does not validate against our schema.</br>"                
            else:
                message += "and is a valid XML file!</br>"

                # call function to parse and store into datastore
                parseXML(in_file)
        
        self.response.out.write("""
        <html>
          <body>
            <form action="/import" method="post" enctype="multipart/form-data">
              <div>
                <input id="myfile" name="myfile" type="file">
                <input value="Upload" type="submit">
              </div>
            </form>
            <p>%s</p>
            <a href="/">Home</a></br>
          </body>
        </html>""" % message)
        
application = webapp.WSGIApplication([('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
