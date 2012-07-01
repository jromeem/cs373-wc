# Group Import Antigravity
# ParseStore.py
# contains the methods to validate, parse, and store
# the data from an xml document.

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

# our GAE defined data models
from DataModels import Link, Person, Organization, Crisis

# validates a xml instance against a schema
# 
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
    list_of_links = []
    for ref in crisis.findall('.//ref'):
        for l in ref:
            new_link = Link()
            if (l.tag):
                new_link.type = l.tag
            if (l.find('./title') != None):
                new_link.title = l.find('./title').text
            if (l.find('./url') != None):
                new_link.link_url = db.Link(l.find('./url').text)
            if (l.find('./description') != None):
                new_link.description = l.find('./description').text
            if (l.find('./site') != None):
                new_link.vid_site = l.find('./site').text
            new_link.put()
            list_of_links.append(new_link.key())
            
    return list_of_links

# in_file
# parse and store the xml data

def parse_store(in_file):

    tree = ElementTree.parse(in_file)
        
    crises = tree.findall(".//crisis")
    people = tree.findall(".//person")
    orgs = tree.findall(".//organization")
    
    for crisis in crises:
        if (crisis.find('.//info')):
            
            list_of_links = grabLinks(crisis)
            
            info = crisis.find('.//info')
            c = Crisis(
                       crisisid = crisis.attrib['id'],
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
                       impact_human_misc = info.find('.//impact').find('.//human').find('.//deaths').text,
                       
                       impact_economic_amount = int(info.find('.//impact').find('.//economic').find('.//amount').text),
                       impact_economic_currency = info.find('.//impact').find('.//economic').find('.//currency').text,
                       impact_economic_misc = info.find('.//impact').find('.//economic').find('.//misc').text,
                       
                       links = list_of_links,
                       orgrefs = [x for x in crisis.find('.//org').attrib['idref']],
                       personrefs = [x for x in crisis.find('.//person').attrib['idref']]
                       )
            c.put()

    for person in people:
        if (person.find('.//info')):
            list_of_links = grabLinks(person)
            p = Person(
                       personid = person.attrib['id'],
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
                       
                       links = list_of_links,
                       orgrefs = [x for x in person.find('.//org').attrib['idref']],
                       crisisrefs = [x for x in person.find('.//crisis').attrib['idref']]
                       )
            p.put()

    for org in orgs:
        if org.find('.//info'):
            info = org.find('.//info')
            contact = info.find('.//contact')
            mail = contact.find('.//mail')
            loc = info.find('.//loc')
            o = Organization(orgid = org.attrib['id'],
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
                             
                             links = list_of_links,
                             personrefs = [x for x in org.find('.//person').attrib['idref']],
                             crisisrefs = [x for x in org.find('.//crisis').attrib['idref']]
                             )
            o.put()
