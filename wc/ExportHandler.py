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
        worldCrises = ElementTree.Element("worldCrisis", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance"})
        
        query = db.GqlQuery("SELECT * FROM Crisis")
        crisis_list = query.fetch()
        
        query = db.GqlQuery("SELECT * FROM Person")
        person_list = cquery.fetch()
        
        query = db.GqlQuery("SELECT * FROM Organization")
        organization_list = cquery.fetch()
        
        for c in crisis_list:
            crisis = ElementTree.SubElement(worldCrises, "crisis", {"id" : c.crisisid})
            name = ElementTree.SubElement(crisis, "name")
            name.text = c.name
            
            info = ElementTree.SubElement(crisis, "info")
            
            history = ElementTree.SubElement(info, "history")
            history.text = c.info_history
            help = ElementTree.SubElement(info, "help")
            help.text = c.info_help
            resources = ElementTree.SubElement(info, "resources")
            resources.text = c.info_resources
            type = ElementTree.SubElement(info, "type")
            type.text = c.info_type
            
            time = ElementTree.SubElement(info, "time")
            time_time = ElementTree.SubElement(time, "time")
            time_time.text = str(c.date_time)
            day = ElementTree.SubElement(time, "day")
            day.text = str(c.date_day)
            month = ElementTree.SubElement(time, "month")
            month.text = str(c.date_month)
            year = ElementTree.SubElement(time, "year")
            year.text = str(c.date_year)
            time_misc = ElementTree.SubElement(time, "misc")
            time_misc.text = str(c.date_misc)
            
            loc = ElementTree.SubElement(info, "loc")
            city = ElementTree.SubElement(loc, "city")
            city.text = c.location_city
            region = ElementTree.SubElement(loc, "region")
            region.text = c.location_region
            country = ElementTree.SubElement(loc, "country")
            country.text = c.location_country
            
            impact = ElementTree.SubElement(info, "impact")
            
            human = ElementTree.SubElement(impact, "human")
            deaths = ElementTree.SubElement(human, "deaths")
            deaths.text = str(c.impact_human_deaths)
            displaced = ElementTree.SubElement(human, "displaced")
            displaced.text = str(c.impact_human_displaced)
            injured = ElementTree.SubElement(human, "injured")
            injured.text = str(c.impact_human_injured)
            missing = ElementTree.SubElement(human, "missing")
            missing.text = str(c.impact_human_missing)
            human_misc = ElementTree.SubElement(human, "misc")
            human_misc.text = c.impact_human_misc
            
            economic = ElementTree.SubElement(impact, "economic")
            amount = ElementTree.SubElement(economic, "amount")
            amount.text = str(c.impact_economic_amount)
            currency = ElementTree.SubElement(economic, "currency")
            currency.text = str(c.impact_economic_currency)
            economic_misc = ElementTree.SubElement(economic, "misc")
            economic_misc.text = c.impact_economic_misc
            
            ref = ElementTree.SubElement(crisis, "ref")
            exportLinks(c, ref)
            
            misc = ElementTree.SubElement(crisis, "misc")
            misc.text = c.misc
            
            for orgref in c.orgrefs:
                org = ElementTree.SubElement(crisis, "org", {"idref" : orgref})
            for personref in c.personrefs:
                person = ElementTree.SubElement(crisis, "person", {"idref" : personref})
    
    
        for o in organization_list:
            organization = ElementTree.SubElement(worldCrises, "organization", {"id" : o.orgid})
            name.text = o.name
            
            info = ElementTree.SubElement(organization, "info")
            orgtype = ElementTree.SubElement(info, "type")
            orgtype.text = o.info_type
            history = ElementTree.SubElement(info, "history")
            history.text = o.info_history
            
            contact = ElementTree.SubElement(info, "contact")
            phone = ElementTree.SubElement(contact, "phone")
            phone.text = o.info_contacts_phone
            email = ElementTree.SubElement(contact, "email")
            email.text = o.info_contacts_email
            
            mail = ElementTree.SubElement(contact, "mail")
            address = ElementTree.SubElement(mail, "address")
            address.text = o.info_contacts_address
            city = ElementTree.SubElement(mail, "city")
            city.text = o.info_contacts_city
            state = ElementTree.SubElement(mail, "state")
            state.text = o.info_contacts_state
            country = ElementTree.SubElement(mail, "country")
            country.text = o.info_contacts_country
            orgzip = ElementTree.SubElement(mail, "zip")
            orgzip.text = o.info_contacts_zip
            
            misc = ElementTree.SubElement(organization, "misc")
            misc.text = o.misc
        

        for p in person_list:
            person = ElementTree.SubElement(worldCrises, "person", {"id" : p.personid})
            name = ElementTree.SubElement(person, "name")
            title = ElementTree.SubElement(name, "title")
            title.text = p.name_title
            first = ElementTree.SubElement(name, "first")
            first.text = p.name_first
            last = ElementTree.SubElement(name, "last")
            last.text = p.name_last
            middle = ElementTree.SubElement(name, "middle")
            middle.text = p.name_middle
            info = ElementTree.SubElement(person, "info")
            info_type = ElementTree.SubElement(info, "type")
            info_type.text = p.info_type
            info_birthdate = ElementTree.SubElement(info, "birthdate")
            info_birthdate_time = ElementTree.SubElement(info_birthdate, "time")
            info_birthdate_time.text = p.info_birthdate_time
            info_birthdate_day = ElementTree.SubElement(info_birthdate, "day")
            info_birthdate_day.text = str(p.info_birthdate_day)
            info_birthdate_month = ElementTree.SubElement(info_birthdate, "month")
            info_birthdate_month.text = str(p.info_birthdate_month)
            info_birthdate_year = ElementTree.SubElement(info_birthdate, "year")
            info_birthdate_year.text = str(p.info_birthdate_year)
            info_birthdate_misc = ElementTree.SubElement(info_birthdate, "misc")
            info_birthdate_misc.text = p.info_birthdate_misc
            info_nat = ElementTree.SubElement(info, "nationality")
            info_nat.text = p.info_nationality
            info_bio = ElementTree.SubElement(info, "biography")
            info_bio.text = p.info_biography

            
        tree = ElementTree.ElementTree(worldCrises)
        text = ElementTree.tostring(worldCrises)            
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        self.response.out.write(text)
        
        
def exportLinks(c, ref):
    for l in link_list:
        if not l.link_parent == c.crisisid:
            continue
        currRef = ElementTree.SubElement(ref, l.type)
        title = ElementTree.SubElement(currRef, "title")
        title.text = l.title
        url = ElementTree.SubElement(currRef, "url")
        url.text = l.link_url
        if (l.type == "video"):
            site = ElementTree.SubElement(currRef, "site")
            site.text = l.vid_site
        if (l.type != "social"):
            description = ElementTree.SubElement(currRef, "description")
            description.text = l.description

application = webapp.WSGIApplication([('/export', ExportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
