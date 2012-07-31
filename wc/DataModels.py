# Group Antigravity
# DataModels.py
from google.appengine.ext import db
from google.appengine.api import memcache
import logging
class Link(db.Model):
    """Link Model Class"""

    link_parent = db.StringProperty()
    link_type = db.StringProperty()
    title = db.StringProperty()
    link_url = db.StringProperty()
    description = db.StringProperty()
    link_site = db.StringProperty()
    def __eq__(self,other):
        if self.link_url == other.link_url and self.link_type == other.link_type:
            return True
        return False

class Person(db.Model):
    """Person Model Class"""
    elemid = db.StringProperty()
    
    name = db.StringProperty()
   
    info_type = db.StringProperty()
    info_birthdate_time = db.StringProperty()
    info_birthdate_day = db.IntegerProperty()
    info_birthdate_month = db.IntegerProperty()
    info_birthdate_year = db.IntegerProperty()
    info_birthdate_misc = db.StringProperty()
    info_nationality = db.StringProperty()
    info_biography = db.TextProperty()
    
    links = db.ListProperty(db.Key)
    
    orgrefs = db.ListProperty(str)
    crisisrefs = db.ListProperty(str)
    
    misc = db.StringProperty()
    
    def attrs(self):
      for attr, value in self.__dict__.iteritems():
        yield attr, value
            
class Crisis(db.Model):
    """Crisis Model Class"""
    elemid = db.StringProperty()

    name = db.StringProperty()
    misc = db.StringProperty()
    
    info_history = db.TextProperty()
    info_help = db.StringProperty()
    info_resources = db.StringProperty()
    info_type = db.StringProperty()
    
    date_time = db.StringProperty()
    date_day = db.IntegerProperty()
    date_month = db.IntegerProperty()
    date_year = db.IntegerProperty()
    date_misc = db.StringProperty()
    
    location_city = db.StringProperty()
    location_region = db.StringProperty()
    location_country = db.StringProperty()
    
    impact_human_deaths = db.IntegerProperty()
    impact_human_displaced = db.IntegerProperty()
    impact_human_injured = db.IntegerProperty()
    impact_human_missing = db.IntegerProperty()
    impact_human_misc = db.TextProperty()
    
    impact_economic_amount = db.IntegerProperty()
    impact_economic_currency = db.StringProperty()
    impact_economic_misc = db.StringProperty()
    
    links = db.ListProperty(db.Key)
    
    orgrefs = db.ListProperty(str)
    personrefs = db.ListProperty(str)
    
    def attrs(self):
      for attr, value in self.__dict__.iteritems():
        yield attr, value
    
class Organization(db.Model):
    """Organization Model Class"""
    elemid = db.StringProperty()
    
    name = db.StringProperty()
    
    info_type = db.StringProperty()
    info_history = db.TextProperty()
    info_contacts_phone = db.StringProperty()
    info_contacts_email = db.StringProperty()
    info_contacts_address = db.StringProperty()
    info_contacts_city = db.StringProperty()
    info_contacts_state = db.StringProperty()
    info_contacts_country = db.StringProperty()
    info_contacts_zip = db.StringProperty()
    
    info_loc_city = db.StringProperty()
    info_loc_region = db.StringProperty()
    info_loc_country = db.StringProperty()
    
    links = db.ListProperty(db.Key)
    
    crisisrefs = db.ListProperty(str)
    personrefs = db.ListProperty(str)
    
    misc = db.StringProperty()

    def attrs(self):
      for attr, value in self.__dict__.iteritems():
        yield attr, value

def getPeople(args = {}, limit = 0):
    """Returns a list of all Person objects matching the key:value pairs supplied in args"""
    plist = [] 
    people = memcache.get("people")
    if people is  None:
        logging.info("CACHE MISS!")
        people = db.GqlQuery("SELECT * FROM Person").run(batch_size=1000)
        memcache.add("people",people)
    for person in people:
        for key in args:
            if person.__dict__[key] != args[key]:
                break
        else:
            plist.append(person)
    if limit !=0:
        plist = plist[:limit]
    return plist

def getCrises(args = {}, limit = 0):
    """Returns a list of all Crisis objects matching the key:value pairs supplied in args"""
    logging.info("CALLED getCrisis!")
    clist = []
    crises = memcache.get("crises")
    if crises is None:
        logging.info("CACHE MISS!")
        crises = db.GqlQuery("SELECT * FROM Crisis").run(batch_size=1000)
        memcache.add("crises",crises)
    logging.info("FETCH TYPE:" + str(type(crises)))
    for crisis in crises:
        for key in args:
            if crisis.__dict__[key] != args[key]:
                break
        else:
            clist.append(crisis)
    if limit !=0:
        clist = clist[:limit]
    return clist

def getOrgs(args = {}, limit = 0):
    """Returns a list of all Organization objects matching the key:value pairs supplied in args"""
    olist = []
    orgs = memcache.get("orgs")
    if orgs is None:
        logging.info("CACHE MISS!")
        orgs = db.GqlQuery("SELECT * FROM Organization").run(batch_size=1000)
        memcache.add("orgs",orgs)
    for org in orgs:
        for key in args:
            if org.__dict__[key] != args[key]:
                break
        else:
            olist.append(org)
    if limit !=0:
        olist = olist[:limit]
    return olist