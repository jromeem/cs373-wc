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
from google.appengine.api.labs import taskqueue

##################
# IMPORT HANDLER #
##################
f = open('wc.xsd', 'rb')
schema = f.read()
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
                <input type="hidden" name="check" value="0" />
                <input type="checkbox" name="check" value="1" /> Check if image URLs are valid<br /><br />
                <input name="merge" value="Import Merge" type="submit" />
                <input name="overwrite" value="Import Overwrite" type="submit" />
              </div>
            </form><br />

            <form method="link" action="http://xkcd.com/353/"><input type="submit" value="Import Antigravity"></form><br />
            
            <a href="/">Home</a>
            </div></div></div>
            <script>$(document).ready(function(){$('#fadeContent').fadeIn(400);$('a').click(function(){$('#fadeContent').fadeOut(400);});});</script>
          </body>
        </html>""")
            
    def post(self): 
        import logging        
        form = cgi.FieldStorage()
        file_item = form['importfile']

        url = form['inurl'].value
        merge = False
        update = False

        ### ### ###
        antigravity = False
        if "antigravity" in form:
            pass
        ### ### ###
        
        logging.info("POSTING TO IMPORT...")
        if "merge" in form:
            logging.info("with merge=TRUE")
            merge = True

        check = 0
        try:
            check = form['check'].value
        except AttributeError:
            check = 1

        
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
                
                if not validXML(content, schema):
                    message = "Error: " + message + "but does not validate against our schema.</br>"                

                else:
                    message += "and is a valid XML file!</br>"

                    # call function to parse and store into datastore
                    flags = {'check': check, 'merge' : merge}
                    parseXML(in_file, flags)
                
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
                <input type="hidden" name="check" value="0" />
                <input type="checkbox" name="check" value="1" /> Check if image URLs are valid<br /><br />
                <input name="merge" value="Import Merge" type="submit" />
                <input name="overwrite" value="Import Overwrite" type="submit" />
              </div>
            </form><br />

            <form method="link" action="http://xkcd.com/353/"><input type="submit" value="Import Antigravity"></form>
            
            <p>%s</p><br />
            <a href="/">Home</a>
            </div></div></div>
            <script>$(document).ready(function(){$('#fadeContent').fadeIn(400);$('a').click(function(){$('#fadeContent').fadeOut(400);});});</script>
          </body>
        </html>""" % message)
        
application = webapp.WSGIApplication([('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
