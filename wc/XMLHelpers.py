# Group Import Antigravity
# XMLHelpers.py
# contains the methods to validate, parse, and build XML
# it also contains the code to populate the GAE datastore

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

from DataModels import Link, Person, Organization, Crisis

###############
# XML HELPERS #
###############

# global lists used only for phase 1
#crisis_list = []
#person_list = []
#organization_list = []
#link_list = []

############################
# IMPORT HANDLER FUNCTIONS #
############################
# xml_instance : string
# a string contains the contents of an xml file
#
# xml_schema_filename : string
# the file name of the xml_schema in the project directory
def validXML (xml_instance, xml_schema_filename):
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
            if (l.find('./site') != None):
                new_link.link_site = l.find('./site').text
            if (l.find('./title') != None):
                new_link.title = l.find('./title').text
            if (l.find('./url') != None):
                new_link.link_url = l.find('./url').text
            if (l.find('./description') != None):
                new_link.description = l.find('./description').text
            new_link.link_parent = crisis.attrib['id']

            
            try:
                q = db.GqlQuery("SELECT title FROM Link WHERE link_url='" + (l.find('./url').text) + "'")
                if (not q.count()):
                    new_link.put()
            except:
                new_link.put()
                
    #return link_list

#adds a crisis to the list, where crisis is an element tree
def addCrisis(crisis):
    if (crisis.find('.//info')):
        info = crisis.find('.//info')
        grabLinks(crisis)
        
        c = Crisis(
                   elemid = crisis.attrib['id'],
                   name = crisis.find('.//name').text if crisis.find('.//name').text != None else "",
                   misc = crisis.find('.//misc').text if crisis.find('.//misc').text != None else "",
                   
                   info_history = info.find('.//history').text if info.find('.//history').text != None else "",
                   info_help = info.find('.//help').text if info.find('.//help').text != None else "",
                   info_resources = info.find('.//resources').text if info.find('.//resources').text != None else "",
                   info_type = info.find('.//type').text if info.find('.//type').text != None else "",
                   
                   date_time = info.find('.//time').find('.//time').text if info.find('.//time').find('.//time').text != None else "",
                   date_day = int(info.find('.//time').find('.//day').text),
                   date_month = int(info.find('.//time').find('.//month').text),
                   date_year = int(info.find('.//time').find('.//year').text),
                   date_misc = info.find('.//time').find('.//misc').text if info.find('.//time').find('.//misc').text != None else "",
                   
                   location_city = info.find('.//loc').find('.//city').text if info.find('.//loc').find('.//city').text != None else "",
                   location_region = info.find('.//loc').find('.//region').text if info.find('.//loc').find('.//region').text != None else "",
                   location_country = info.find('.//loc').find('.//country').text if info.find('.//loc').find('.//country').text != None else "",
                   
                   impact_human_deaths = int(info.find('.//impact').find('.//human').find('.//deaths').text),
                   impact_human_displaced = int(info.find('.//impact').find('.//human').find('.//displaced').text),
                   impact_human_injured = int(info.find('.//impact').find('.//human').find('.//injured').text),
                   impact_human_missing = int(info.find('.//impact').find('.//human').find('.//missing').text),
                   impact_human_misc = info.find('.//impact').find('.//human').find('.//misc').text if info.find('.//impact').find('.//human').find('.//misc').text != None else "",
                   
                   impact_economic_amount = int(info.find('.//impact').find('.//economic').find('.//amount').text),
                   impact_economic_currency = info.find('.//impact').find('.//economic').find('.//currency').text,
                   impact_economic_misc = info.find('.//impact').find('.//economic').find('.//misc').text if info.find('.//impact').find('.//economic').find('.//misc').text != None else "",
                   
                   orgrefs = [x.attrib['idref'] for x in crisis.findall('.//org')],
                   personrefs = [x.attrib['idref'] for x in crisis.findall('.//person')]
                   )

        
        try:
            q = db.GqlQuery("SELECT name FROM Crisis WHERE elemid='" + crisis.attrib['id'] + "'")
            if (not q.count()):
                c.put()
        except:
            c.put()

        #return crisis_list
    
#adds a person to the list, where person is an element tree
def addPerson(person):
    if (person.find('.//info')):
        grabLinks(person)
        p = Person(
                   elemid = person.attrib['id'],
                   name = person.find('.//name').text if person.find('.//name').text != None else "",
                   info_type = person.find('.//info').find('.//type').text if person.find('.//info').find('.//type').text != None else "",
                   info_birthdate_time = person.find('.//info').find('.//birthdate').find('.//time').text if person.find('.//info').find('.//birthdate').find('.//time').text != None else "",
                   info_birthdate_day = int(person.find('.//info').find('.//birthdate').find('.//day').text) if person.find('.//info').find('.//birthdate').find('.//day').text != None else "",
                   info_birthdate_month = int(person.find('.//info').find('.//birthdate').find('.//month').text) if person.find('.//info').find('.//birthdate').find('.//month').text != None else "",
                   info_birthdate_year = int(person.find('.//info').find('.//birthdate').find('.//year').text) if person.find('.//info').find('.//birthdate').find('.//year').text != None else "",
                   info_birthdate_misc = person.find('.//info').find('.//birthdate').find('.//misc').text if person.find('.//info').find('.//birthdate').find('.//misc').text != None else "",
                   info_nationality = person.find('.//info').find('.//nationality').text if person.find('.//info').find('.//nationality').text != None else "",
                   info_biography = person.find('.//info').find('.//biography').text if person.find('.//info').find('.//biography').text != None else "",
                   
                   orgrefs = [x.attrib['idref'] for x in person.findall('.//org')],
                   crisisrefs = [x.attrib['idref'] for x in person.findall('.//crisis')]
                   )
            
        try:       
            q = db.GqlQuery("SELECT name FROM Person WHERE elemid='" + person.attrib['id'] + "'")
            if (not q.count()):
                p.put()
        except:
            p.put()
            
        #return person_list
        
#adds an organization to the list, where org is an element tree
def addOrganization(org):
    if org.find('.//info'):
        grabLinks(org)
        info = org.find('.//info')
        contact = info.find('.//contact')
        mail = contact.find('.//mail')
        loc = info.find('.//loc')
        o = Organization(
                         elemid = org.attrib['id'],
                         name = org.find('.//name').text if org.find('.//name').text != None else "",
                         misc = org.find('.//misc').text if org.find('.//misc').text != None else "",
                         
                         info_type = info.find('.//type').text if info.find('.//type').text != None else "",
                         info_history = info.find('.//history').text if info.find('.//history').text != None else "",

                         info_contacts_phone = contact.find('.//phone').text if contact.find('.//phone').text != None else "",
                         info_contacts_email = contact.find('.//email').text if contact.find('.//email').text != None else "",
                         info_contacts_address = mail.find('.//address').text if mail.find('.//address').text != None else "",
                         info_contacts_city = mail.find('.//city').text if mail.find('.//city').text != None else "",
                         info_contacts_state = mail.find('.//state').text if mail.find('.//state').text != None else "",
                         info_contacts_country = mail.find('.//country').text if mail.find('.//country').text != None else "",
                         info_contacts_zip = mail.find('.//zip').text if mail.find('.//zip').text != None else "",

                         info_loc_city = loc.find('.//city').text if loc.find('.//city').text != None else "",
                         info_loc_region = loc.find('.//region').text if loc.find('.//region').text != None else "",
                         info_loc_country = loc.find('.//country').text if loc.find('.//country').text != None else "",
                         
                         personrefs = [x.attrib['idref'] for x in org.findall('.//person')],
                         crisisrefs = [x.attrib['idref'] for x in org.findall('.//crisis')]
                         )
        
        try:
            q = db.GqlQuery("SELECT name FROM Organization WHERE elemid='" + org.attrib['id'] + "'")
            if (not q.count()):
                o.put()
        except:
            o.put()
            
        #return organization_list

#clears the global lists (temporary fix until db integration)
def clearGlobals():
    # to prevent multiple copy uploads
    global crisis_list
    global person_list
    global organization_list
    global link_list
    crisis_list = []
    person_list = []
    organization_list = []
    link_list = []

# in_file : file (XML-validated file)
# parse and store the XML data in the GAE datastore
def parseXML(in_file):
    
    clearGlobals()

    tree = ElementTree.parse(in_file)
        
    crises = tree.findall(".//crisis")
    people = tree.findall(".//person")
    orgs = tree.findall(".//organization")

    #build crisis list
    for crisis in crises:
        addCrisis(crisis)

    #build person list
    for person in people:
        addPerson(person)

    #build organization list
    for org in orgs:
        addOrganization(org)

############################
# EXPORT HANDLER FUNCTIONS #
############################
#gets links for a crisis from the list and adds them to the element tree
def exportLinks(c, ref):
    link_list = db.GqlQuery("SELECT * FROM Link WHERE link_parent='" + c.elemid+"'")
    for l in link_list:
        currRef = ElementTree.SubElement(ref, l.link_type)
        site = ElementTree.SubElement(currRef, "site")
        site.text = l.link_site
        title = ElementTree.SubElement(currRef, "title")
        title.text = l.title
        url = ElementTree.SubElement(currRef, "url")
        url.text = l.link_url
        description = ElementTree.SubElement(currRef, "description")
        description.text = l.description

# fills a crisis subtree, where crisis is the root element, and c is a Crisis object
def buildCrisis(crisis, c):
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

# fills an organization subtree, where organization is the root element, and o is an Organization object
def buildOrganization(organization, o):
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
    
    loc = ElementTree.SubElement(info, "loc")
    city = ElementTree.SubElement(loc, "city")
    city.text = o.info_loc_city
    region = ElementTree.SubElement(loc, "region")
    region.text = o.info_loc_region
    country = ElementTree.SubElement(loc, "country")
    country.text = o.info_loc_country

    ref = ElementTree.SubElement(organization, "ref")
    exportLinks(o, ref)

    misc = ElementTree.SubElement(organization, "misc")
    misc.text = o.misc

    for crisisref in o.crisisrefs:
        crisis = ElementTree.SubElement(organization, "crisis", {"idref" : crisisref})
    for personref in o.personrefs:
        person = ElementTree.SubElement(organization, "person", {"idref" : personref})

# fills a person subtree, where person is the root element, and p is a person object
def buildPerson(person, p):
    name = ElementTree.SubElement(person, "name")
    name.text = p.name
    
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

# main function that builds xml
def buildXML(worldCrises):
    
    #build sub-trees for each crisis
    crisis_list = db.GqlQuery("SELECT * FROM Crisis")
    for c in crisis_list:
        crisis = ElementTree.SubElement(worldCrises, "crisis", {"id" : c.elemid})
        buildCrisis(crisis, c)
        
    #build sub-trees for each organization
    organization_list = db.GqlQuery("SELECT * FROM Organization")
    for o in organization_list:
        organization = ElementTree.SubElement(worldCrises, "organization", {"id" : o.elemid})
        buildOrganization(organization, o)

    #build sub-trees for each person
    person_list = db.GqlQuery("SELECT * FROM Person")
    for p in person_list:
        person = ElementTree.SubElement(worldCrises, "person", {"id" : p.elemid})
        buildPerson(person, p)
            
    tree = ElementTree.ElementTree(worldCrises)
    text = ElementTree.tostring(worldCrises)

    return text
    
