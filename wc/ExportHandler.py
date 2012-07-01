import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import cgi, os
import cgitb; cgitb.enable()
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

class ExportPage(webapp.RequestHandler):
    def get(self):
        crises = db.GqlQuery("SELECT * FROM Crisis")
              
        xml_string = '<?xml version="1.0" encoding="UTF-8"?><worldCrises xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"xsi:noNamespaceSchemaLocation="wc.xsd">'
        
        for crisis in crises:
            xml_string += "<crisis id=\"" + crisis.crisisid + "\">"
            xml_string += "<name>" + crisis.name + "</name>"
            xml_string += "<info>"
            xml_string += "<history>" + crisis.info_history + "</history>"
            xml_string += "<help>" + crisis.info_help + "</help>"
            xml_string += "<resources>" + crisis.info_resources + "</resources>"
            xml_string += "<type>" + crisis.info_type + "</type>"
            xml_string += "<time>"
            xml_string += "<time>" + str(crisis.date_time) + "</time>"
            xml_string += "<day>" + str(crisis.date_day) + "</day>"
            xml_string += "<month>" + str(crisis.date_month) + "</month>"
            xml_string += "<year>" + str(crisis.date_year) + "</year>"
            xml_string += "<misc>" + (crisis.date_misc or "") + "</misc>"
            xml_string += "</time>"
            xml_string += "<loc>"
            xml_string += "<city>" + (crisis.location_city or "") + "</city>"
            xml_string += "<region>" + (crisis.location_region or "") + "</region>"
            xml_string += "<country>" + (crisis.location_country or "") + "</country>"
            xml_string += "</loc>"
            xml_string += "<impact>"
            xml_string += "<human>"
            xml_string += "<deaths>" + str(crisis.impact_human_deaths) + "</deaths>"
            xml_string += "<displaced>" + str(crisis.impact_human_displaced) + "</displaced>"
            xml_string += "<injured>" + str(crisis.impact_human_injured) + "</injured>"
            xml_string += "<missing>" + str(crisis.impact_human_missing) + "</missing>"
            xml_string += "<misc>" + str(crisis.impact_human_misc or "") + "</misc>"
            xml_string += "</human>"
            xml_string += "<economic>"
            xml_string += "<amount>" + str(crisis.impact_economic_amount) + "</amount>"
            xml_string += "<currency>" + str(crisis.impact_economic_currency or "") + "</currency>"
            xml_string += "<misc>" + str(crisis.impact_economic_misc or "") + "</misc>"
            xml_string += "</economic>"
            xml_string += "</impact>"
            xml_string += "</info>"
            xml_string += "</crisis>"
        xml_string += "</worldCrises>"
        
        #print xml_string
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        self.response.out.write(xml_string)

application = webapp.WSGIApplication([('/export', ExportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
