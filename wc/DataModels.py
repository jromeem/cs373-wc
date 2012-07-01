# Group Antigravity
# DataModels.py
from google.appengine.ext import db

class Link(db.Model):
    type = db.StringProperty()
    title = db.StringProperty()
    link_url = db.LinkProperty()
    description = db.StringProperty()
    vid_site = db.StringProperty()

class Person(db.Model):
    personid = db.StringProperty()
    
    name_title = db.StringProperty()
    name_first = db.StringProperty()
    name_last = db.StringProperty()
    name_middle = db.StringProperty()
    
    info_type = db.StringProperty()
    info_birthdate_time = db.StringProperty()
    info_birthdate_day = db.IntegerProperty()
    info_birthdate_month = db.IntegerProperty()
    info_birthdate_year = db.IntegerProperty()
    info_birthdate_misc = db.StringProperty()
    info_nat = db.StringProperty()
    into_bio = db.TextProperty()
    
    links = db.ListProperty(db.Key)
    
    orgrefs = db.ListProperty(str)
    crisisrefs = db.ListProperty(str)
    
    misc = db.StringProperty()

            
class Crisis(db.Model):
    crisisid = db.StringProperty()

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
    impact_human_misc = db.StringProperty()
    
    impact_economic_amount = db.IntegerProperty()
    impact_economic_currency = db.StringProperty()
    impact_economic_misc = db.StringProperty()
    
    links = db.ListProperty(db.Key)
    
    orgrefs = db.ListProperty(str)
    personrefs = db.ListProperty(str)
    
class Organization(db.Model):
    orgid = db.StringProperty()
    
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
    
    links = db.ListProperty(db.Key)
    
    crisisrefs = db.ListProperty(str)
    personrefs = db.ListProperty(str)
    
    misc = db.StringProperty()