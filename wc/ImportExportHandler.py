# Group Import Antigravity
# ImportExportHandler.py

import cgi, os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import cgitb; cgitb.enable()
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

# our GAE defined data models
from DataModels import Link, Person, Organization, Crisis

crisis_list = []
person_list = []
organization_list = []
link_list = []

###################
# PARSE AND STORE #
###################
# xml_instance : string
# a string contains the contents of an xml file
#
# xml_schema_filename : string
# the file name of the xml_schema in the project directory
def is_valid_xml (xml_instance, xml_schema_filename):
    try:
        etw = xsv.parseAndValidateXmlInputString(xml_instance, xml_schema_filename,xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        et = etw.getTree()
        root = et.getroot()
        return True
    except:
        return False

# used for creating the list of links for a given crisis/ppl/org
# crisis : Elementtree object
def grabLinks(crisis):
    for ref in crisis.findall('.//ref'):
        for l in ref:
            new_link = Link()
            if (l.tag):
                new_link.link_type = l.tag
            if (l.find('./title') != None):
                new_link.title = l.find('./title').text
            if (l.find('./url') != None):
                new_link.link_url = db.Link(l.find('./url').text)
            if (l.find('./description') != None):
                new_link.description = l.find('./description').text
            if (l.find('./site') != None):
                new_link.vid_site = l.find('./site').text
            new_link.link_parent = crisis.attrib['id']
            #new_link.put()
            link_list.append(new_link)

# in_file : file (XML-validated file)
# parse and store the xml data in the GAE datastore
def parse_store(in_file):

    tree = ElementTree.parse(in_file)
        
    crises = tree.findall(".//crisis")
    people = tree.findall(".//person")
    orgs = tree.findall(".//organization")
    
    for crisis in crises:
        if (crisis.find('.//info')):
            
            info = crisis.find('.//info')
            grabLinks(crisis)
            
            c = Crisis(
                       elemid = crisis.attrib['id'],
                       name = crisis.find('.//name').text,
                       misc = crisis.find('.//misc').text,
                       
                       info_history = info.find('.//history').text,
                       info_help = info.find('.//help').text,
                       info_resources = info.find('.//resources').text,
                       info_type = info.find('.//type').text,
                       
                       date_time = info.find('.//time').find('.//time').text,
                       date_day = int(info.find('.//time').find('.//day').text),
                       date_month = int(info.find('.//time').find('.//month').text),
                       date_year = int(info.find('.//time').find('.//year').text),
                       date_misc = info.find('.//time').find('.//misc').text,
                       
                       location_city = info.find('.//loc').find('.//city').text,
                       location_region = info.find('.//loc').find('.//region').text,
                       location_country = info.find('.//loc').find('.//country').text,
                       
                       impact_human_deaths = int(info.find('.//impact').find('.//human').find('.//deaths').text),
                       impact_human_displaced = int(info.find('.//impact').find('.//human').find('.//displaced').text),
                       impact_human_injured = int(info.find('.//impact').find('.//human').find('.//injured').text),
                       impact_human_missing = int(info.find('.//impact').find('.//human').find('.//missing').text),
                       impact_human_misc = info.find('.//impact').find('.//human').find('.//misc').text,
                       
                       impact_economic_amount = int(info.find('.//impact').find('.//economic').find('.//amount').text),
                       impact_economic_currency = info.find('.//impact').find('.//economic').find('.//currency').text,
                       impact_economic_misc = info.find('.//impact').find('.//economic').find('.//misc').text,
                       
                       orgrefs = [x.attrib['idref'] for x in crisis.findall('.//org')],
                       personrefs = [x.attrib['idref'] for x in crisis.findall('.//person')]
                       )
            crisis_list.append(c)
            #c.put()

    for person in people:
        if (person.find('.//info')):
            grabLinks(person)
            p = Person(
                       elemid = person.attrib['id'],
                       name_title = person.find('.//name').find('.//title').text,
                       name_first = person.find('.//name').find('.//first').text,
                       name_last = person.find('.//name').find('.//last').text,
                       name_middle = person.find('.//name').find('.//middle').text,
                       info_type = person.find('.//info').find('.//type').text,
                       info_birthdate_time = person.find('.//info').find('.//birthdate').find('.//time').text,
                       info_birthdate_day = int(person.find('.//info').find('.//birthdate').find('.//day').text),
                       info_birthdate_month = int(person.find('.//info').find('.//birthdate').find('.//month').text),
                       info_birthdate_year = int(person.find('.//info').find('.//birthdate').find('.//year').text),
                       info_birthdate_misc = person.find('.//info').find('.//birthdate').find('.//misc').text,
                       info_nationality = person.find('.//info').find('.//nationality').text,
                       info_biography = person.find('.//info').find('.//biography').text,
                       
                       orgrefs = [x.attrib['idref'] for x in person.findall('.//org')],
                       crisisrefs = [x.attrib['idref'] for x in person.findall('.//crisis')]
                       )
            person_list.append(p)
            #p.put()

    for org in orgs:
        if org.find('.//info'):
            grabLinks(org)
            info = org.find('.//info')
            contact = info.find('.//contact')
            mail = contact.find('.//mail')
            loc = info.find('.//loc')
            o = Organization(
                             elemid = org.attrib['id'],
                             name = org.find('.//name').text,
                             misc = org.find('.//misc').text,
                             
                             info_type = info.find('.//type').text,
                             info_history = info.find('.//history').text,

                             info_contacts_phone = contact.find('.//phone').text,
                             info_contacts_email = contact.find('.//email').text,
                             info_contacts_address = mail.find('.//address').text,
                             info_contacts_city = mail.find('.//city').text,
                             info_contacts_state = mail.find('.//state').text,
                             info_contacts_country = mail.find('.//country').text,
                             info_contacts_zip = mail.find('.//zip').text,

                             info_loc_city = loc.find('.//city').text,
                             info_loc_region = loc.find('.//region').text,
                             info_loc_country = loc.find('.//country').text,
                             
                             personrefs = [x.attrib['idref'] for x in org.findall('.//person')],
                             crisisrefs = [x.attrib['idref'] for x in org.findall('.//crisis')]
                             )
            organization_list.append(o)
            #o.put()

##################
# EXPORT HANDLER #
##################

#exports current data to an xml string
class ExportPage(webapp.RequestHandler):
    def get(self):
        worldCrises = ElementTree.Element("worldCrisis", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance"})

        #crisis_list = db.GqlQuery("SELECT * FROM Crisis")
        #person_list = db.GqlQuery("SELECT * FROM Person")
        #organization_list = db.GqlQuery("SELECT * FROM Organization")
        
        #convert the crisis list to an xml string and append it
        for c in crisis_list:
            crisis = ElementTree.SubElement(worldCrises, "crisis", {"id" : c.elemid})
            name = ElementTree.SubElement(crisis, "name")
            name.text = c.name
            
            info = ElementTree.SubElement(crisis, "info")
            
            history = ElementTree.SubElement(info, "history")
            history.text = c.info_history
            help = ElementTree.SubElement(info, "help")
            help.text = c.info_help
            resources = ElementTree.SubElement(info, "resources")
            resources.text = c.info_resources
            c_type = ElementTree.SubElement(info, "type")
            c_type.text = c.info_type
            
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
    
		#convert the organization list to an xml string and append it
        for o in organization_list:
            organization = ElementTree.SubElement(worldCrises, "organization", {"id" : o.elemid})
            name = ElementTree.SubElement(organization, "name")
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
            
            ref = ElementTree.SubElement(organization, "ref")
            exportLinks(o, ref)
            
            misc = ElementTree.SubElement(organization, "misc")
            misc.text = o.misc
            
            for crisisref in o.crisisrefs:
                crisis = ElementTree.SubElement(organization, "crisis", {"idref" : crisisref})
            for personref in o.personrefs:
                person = ElementTree.SubElement(organization, "person", {"idref" : personref})
        
        #convert the person list to an xml string and append it
        for p in person_list:
            person = ElementTree.SubElement(worldCrises, "person", {"id" : p.elemid})
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
            
            ref = ElementTree.SubElement(person, "ref")
            exportLinks(p, ref)
            misc = ElementTree.SubElement(person, "misc")
            misc.text = p.misc
            
            for crisisref in p.crisisrefs:
                crisis = ElementTree.SubElement(person, "crisis", {"idref" : crisisref})
            for orgref in p.orgrefs:
                org = ElementTree.SubElement(person, "org", {"idref" : orgref})
            
        tree = ElementTree.ElementTree(worldCrises)
        text = ElementTree.tostring(worldCrises)            
        self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
        self.response.out.write(text)
        
#gets links for a crisis from the list and adds them to the element tree
def exportLinks(c, ref):
    for l in link_list:
        if not l.link_parent == c.elemid:
            continue
        currRef = ElementTree.SubElement(ref, l.link_type)
        title = ElementTree.SubElement(currRef, "title")
        title.text = l.title
        url = ElementTree.SubElement(currRef, "url")
        url.text = l.link_url
        if (l.link_type == "video"):
            site = ElementTree.SubElement(currRef, "site")
            site.text = l.vid_site
        if (l.link_type != "social"):
            description = ElementTree.SubElement(currRef, "description")
            description.text = l.description

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


application = webapp.WSGIApplication([('/import', ImportPage),
                                      ('/export', ExportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
