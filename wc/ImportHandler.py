# Group Import Antigravity
# ImportHandler.py

import cgi, os
import cgitb; cgitb.enable()
import urllib2
import tempfile
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
            <head>
                <link rel="stylesheet" type="text/css" href="stylesheets/main.css" />
                <script src="js/jquery-1.7.2.min.js"></script>
                <script src="js/fadeStuff.js"></script>
            </head>
          <body>
            <div id="wrapper"><div id="content"><div id="fadeContent">
            <form action="/import" method="post" enctype="multipart/form-data">
              <div>
                Upload an XML file </br>
                <input id="importfile" name="importfile" type="file"><br /><br />
                
                Or provide a URL</br>
                <input id="inurl" name="inurl" type="text"><br /><br />
                <input value="Import" type="submit" />
              </div>
            </form><br />
            <a href="/">Home</a>
            </div></div></div>
            <script>$(document).ready(function(){$('#fadeContent').fadeIn(400);$('a').click(function(){$('#fadeContent').fadeOut(400);});});</script>
          </body>
        </html>""")
            
    def post(self):        
        form = cgi.FieldStorage()
        file_item = form['importfile']
        url = form['inurl'].value
        

        # check if file was uploaded
        if not file_item.filename and not url:
            message = 'Error: No file was uploaded. Try again?</br>'
            
        elif file_item.filename and url:
            message = 'Error: Please upload only one document.</br>'
        else:
            try:
                if not url:
                    file_name = os.path.basename(file_item.filename)
                    in_file = file_item.file
                    message = 'The file "' + file_name + '" was uploaded successfully, '
                    content = form.getvalue('importfile')
                else:
                    webfile = urllib2.urlopen(url)
                    content = webfile.read()
                    message = 'Content from "' + url + '" was accessed successfully, '
                    in_file = webfile
                    #self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
                    #content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
                    #self.response.out.write(content)
                    #return
                    
                # check if uploaded file is a valid xml_instance
                if not validXML(content, "wc.xsd"):
                    message = "Error: " + message + "but does not validate against our schema.</br>"                
                else:
                    message += "and is a valid XML file!</br>"

                    # call function to parse and store into datastore
                    parseXML(in_file)
            except urllib2.URLError, ue:
                message = 'URLERROR: ' + str(ue)
            except ValueError, ve:
                message = 'VALUEERROR: '+ str(ve)
                
        self.response.out.write("""
        <html>
        <head>
                <link rel="stylesheet" type="text/css" href="stylesheets/main.css" />
                <script src="js/jquery-1.7.2.min.js"></script>
                <script src="js/fadeStuff.js"></script>
            </head>
          <body>
          <div id="wrapper"><div id="content"><div id="fadeContent">
            <form action="/import" method="post" enctype="multipart/form-data">
              <div>
                Upload an XML file </br>
                <input id="importfile" name="importfile" type="file"><br /><br />
                Or provide a URL</br>
                <input id="inurl" name="inurl" type="text"><br /><br />
                <input value="Import" type="submit" />
              </div>
            </form><br />
            <p>%s</p><br />
            <a href="/">Home</a></br>
            </div></div></div>
          </body>
        </html>""" % message)
        
application = webapp.WSGIApplication([('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
