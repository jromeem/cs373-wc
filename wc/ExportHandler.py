# Group Import Antigravity
# ExportHandler.py

import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from xml.etree import ElementTree
from XMLHelpers import buildXML

##################
# EXPORT HANDLER #
##################
#exports current data to an xml string
class ExportPage(webapp.RequestHandler):
    def get(self):
        worldCrises = ElementTree.Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})

        xml_out = buildXML(worldCrises)
        
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        self.response.out.write('<?xml version="1.0" encoding="UTF-8"?>' + xml_out)

application = webapp.WSGIApplication([('/export', ExportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
