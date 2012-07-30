# Group Import Antigravity
# XMLHelpers.py
# contains the methods to validate, parse, and build XML
# it also contains the code to populate the GAE datastore
import logging
from google.appengine.api.labs import taskqueue 

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

from DataModels import Link, Person, Organization, Crisis

from google.appengine.api.urlfetch import DownloadError 
import httplib
import urlparse
import urllib
import cPickle
import zlib

###############
# XML HELPERS #
###############

# global lists used only for phase 1
#crisis_list = []
#person_list = []
#organization_list = []
#link_list = []
check = 0
merge = 0

############################
# IMPORT HANDLER FUNCTIONS #
############################
# xml_instance : string
# a string contains the contents of an xml file
#
# xml_schema_filename : string
# the file name of the xml_schema in the project directory
def validXML (xml_instance, xml_schema_filename):
    assert(xml_instance is not None)
    assert(xml_schema_filename is not None)
    
    try:
        etw = xsv.parseAndValidateXmlInputString(xml_instance, xml_schema_filename,xmlIfClass=xsv.XMLIF_ELEMENTTREE)
        et = etw.getTree()
        root = et.getroot()
        return True
    except:
        pass
        return False

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """

    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
        
# Uses HTTP request to see if the url given is valid
# url : url
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND]
    return get_server_status_code(url) in good_codes

def mergeLinks(newmodel, oldmodel, newlinks):
    oldlinks = db.GqlQuery("SELECT * FROM Link WHERE link_parent='" + oldmodel.elemid + "'")
    for link in newlinks:
        if not link in oldlinks:
            link.link_parent = oldmodel.elemid
            link.put() 

def mergeModels(newmodel, oldmodel):
    logging.info("MERGEMODELS CALLED!")
    #try:
    logging.info("TRYING")
    logging.info("OLDMODEL TYPE: " + str(type(oldmodel)))
    olddict = oldmodel.__dict__
    logging.info("OLD DICT KEYS: ")
    for k in olddict:
        logging.info("     " + str(k))
    logging.info("ENTERING FOR LOOP...")
    for k,v in newmodel.__dict__.iteritems():
        logging.info("---------KV PAIR: "+ str(k) + " " + str(v) )
        
        if (k in olddict) and (v != False and v != "" and v != None):
            if olddict[k] == False or olddict[k] == "":
                logging.info("key " + str(k) + " not found; replacing with new value: " + str(v))
                setattr(oldmodel,k,v)
    #except StopIteration:
    logging.info("STOPITER")
    return oldmodel

# used for creating the list of links for a given crisis/ppl/org
# crisis : Elementtree object
def grabLinks(crisis):
    assert(crisis is not None)
    links = []
    imgvid_tags = ["primaryImage","image"]
    for ref in crisis.findall('.//ref'):
        for l in ref:
            new_link = Link()
            if (l.tag):
                new_link.link_type = l.tag
            if (l.find('./site') != None):
                new_link.link_site = l.find('./site').text
            if (l.find('./title') != None):
                new_link.title = l.find('./title').text
            try:
                if (l.find('./url') != None):
                    
                    if (l.tag in imgvid_tags and check == 1):
                        
                        if (check_url(l.find('./url').text)):
                            new_link.link_url = l.find('./url').text
                        else:
                            new_link.link_url = None
                    else:
                        new_link.link_url = l.find('./url').text            
            except DownloadError:
                new_link.link_url = None
            except AttributeError:
                new_link.link_url = None
            if (l.find('./description') != None):
                new_link.description = l.find('./description').text
            new_link.link_parent = crisis.attrib['id']



            try:
                if new_link.link_url != None:
                    q = db.GqlQuery("SELECT * FROM Link WHERE link_parent='" + crisis.attrib['id'] + "' AND link_url='" + new_link.link_url + "' AND link_type='" + new_link.link_type + "'")

                    if (not q.count()):
                        #new_link.put()
                        links.append(new_link)
                    
            except db.BadQueryError, e:
                logging.info("Error Caught: "+ str(e))
                #new_link.put()
                links.append(new_link)
    return links
    
#adds a crisis to the list, where crisis is an element tree
def addCrisis(crisis):

    
    assert(crisis is not None)
    if (crisis.find('.//info') is not None):
        info = crisis.find('.//info')
        links = grabLinks(crisis)
        
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
            q = db.GqlQuery("SELECT * FROM Crisis WHERE elemid='" + crisis.attrib['id'] + "'")
            if (not q.count()) and merge:
                q = db.GqlQuery("SELECT * FROM Crisis WHERE name='" + c.name + "'")
            if (not q.count()):
                c.put()
                for link in links:
                    link.put()
            elif merge:
                mergeModels(c,q[0]).put()
                mergeLinks(c,q[0],links)
        except db.BadQueryError, e:
            logging.info("Error Caught: "+ str(e))
            c.put()
            for link in links:
                link.put()
        
    
#adds a person to the list, where person is an element tree
def addPerson(person):
    assert(person is not None)
    
    if (person.find('.//info') is not None):
        links = grabLinks(person)
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
            q = db.GqlQuery("SELECT * FROM Person WHERE elemid='" + person.attrib['id'] + "'")
            if (not q.count()) and merge:
                q = db.GqlQuery("SELECT * FROM Person WHERE name='" + p.name + "'")
            if (not q.count()):
                p.put()
                for link in links:
                    link.put()
            elif merge:
                mergeModels(p,q[0]).put()
                mergeLinks(p,q[0],links)
        except db.BadQueryError, e:
            logging.info("Error Caught: "+ str(e))
            p.put()
            for link in links:
                link.put()
        
        
#adds an organization to the list, where org is an element tree
def addOrganization(org):
    assert (org is not None)    
    
    if org.find('.//info') is not None:
        links = grabLinks(org)
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
            q = db.GqlQuery("SELECT * FROM Organization WHERE elemid='" + org.attrib['id'] + "'")
            if (not q.count()) and merge:
                q = db.GqlQuery("SELECT * FROM Organization WHERE name='" + o.name + "'")
            if (not q.count()):
                o.put()
                for link in links:
                    link.put()
            elif merge:
                mergeModels(o,q[0]).put()
                mergeLinks(o,q[0],links)
        except db.BadQueryError, e:
            logging.info("Error Caught: "+ str(e))
            o.put()
            for link in links:
                link.put()

def zdumps(obj):
  return zlib.compress(cPickle.dumps(obj,cPickle.HIGHEST_PROTOCOL),9)
  
# in_file : file (XML-validated file)
# parse and store the XML data in the GAE datastore
def parseXML(in_file, flags):
    assert(in_file is not None)
    assert(flags is not None)
    global check
    global merge
    check = flags['check']
    merge = flags['merge']

    if not merge:
        db.delete(db.Query())

    tree = ElementTree.parse(in_file)
        
    crises = tree.findall(".//crisis")
    people = tree.findall(".//person")
    orgs = tree.findall(".//organization")
   
    #logging.info('***** LEN CRISIS' + str(len(crises)))   
    #logging.info('***** LEN CRISIS' + str(len(people)))  
    #logging.info('***** LEN CRISIS' + str(len(orgs)))  
	
    for crisis in crises:
        if (crisis.find('.//info') is not None):
            carr = ['crisis',crisis]
            pCrisis = zdumps(carr)
            task = taskqueue.Task(url='/importtask', payload=pCrisis).add(queue_name='importtask')
            #logging.info('***** adding CRISIS task NAME: ' + str(crisis))
		
    for person in people:
        if (person.find('.//info') is not None):
            parr = ['person',person]
            pPerson = zdumps(parr)
            task = taskqueue.Task(url='/importtask', payload=pPerson).add(queue_name='importtask')
            #logging.info('***** adding PERSON task NAME: ' + str(person))
		
    for org in orgs:
        if (org.find('.//info') is not None):
            oarr = ['org',org]
            pOrg = zdumps(oarr)
            task = taskqueue.Task(url='/importtask', payload=pOrg).add(queue_name='importtask')
            #logging.info('***** adding ORG task')    
    
    check = 0
    merge = 0
	
############################
# EXPORT HANDLER FUNCTIONS #
############################
#gets links for a crisis from the list and adds them to the element tree
def exportLinks(c, ref):
    assert(c is not None)
    assert(ref is not None)

    link_list = db.GqlQuery("SELECT * FROM Link WHERE link_parent='" + c.elemid+"'")

    for t in ['primaryImage', 'image', 'video', 'social', 'ext']:
        for l in link_list:
            if l.link_type == t:
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
    assert(crisis is not None)
    assert(c is not None)

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
    assert(organization is not None)
    assert(o is not None)    
    
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
    assert(person is not None)
    assert(p is not None)
    
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
    assert(worldCrises is not None)
    
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
    
