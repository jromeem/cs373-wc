import cgi, os
import cgitb; cgitb.enable()
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# module that parses and stores into data models
from ParseStore import is_valid_xml, parse_store
        
##################
# IMPORT HANDLER #
##################

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
            <a href="/">Home</a></br>
          </body>
        </html>""")
            
    def post(self):        
        form = cgi.FieldStorage()
        file_item = form['myfile']
        content = form.getvalue('myfile')

        # check if file was uploaded
        if not file_item.filename:
            message = 'No file was uploaded. Try again? </br>'
        
        else:
            file_name = os.path.basename(file_item.filename)
            in_file = file_item.file
            message = 'The file "' + file_name + '" was uploaded successfully '

            # check if uploaded file is a valid xml_instance
            if not is_valid_xml(content, "wc.xsd"):
                message += "but file does not validate against schema! </br>"
                
            else:
                message += "and XML file validates against schema! </br>"

                # call function to parse and store into datastore
                parse_store(in_file)
        
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
