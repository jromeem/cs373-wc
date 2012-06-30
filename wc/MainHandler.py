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


class MainPage(webapp.RequestHandler):
    def get(self):
        page = self.request.get('page')
        template_values = {
            'page': page,
        }

        #path = os.path.join(os.path.dirname(__file__), page + ".html")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))
        
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
            </body>
            </html>""")
            
    def post(self):
        form = cgi.FieldStorage()
        fileitem = form['myfile']
        
        
        # Test if the file was uploaded
        if fileitem.filename:
            fn = os.path.basename(fileitem.filename)
            f = fileitem.file
            message = 'The file "' + fn + '" was uploaded successfully.  Upload another? </br>'
            
            #f = f.read()
            
            #parser = ElementTree.XMLParser()
            
            tree = ElementTree.parse(f)
            
            try:
                etw = xsv.parseAndValidateXmlInput(fn,'wc.xsd',xmlIfClass=xsv.XMLIF_ELEMENTTREE)
                et = etw.getTree()
                root = et.getroot()
                print "XML Validates!"
                
                crises = tree.findall(".//crisis")
                people = tree.findall(".//person")
                orgs = tree.findall(".//organization")
                for crisis in crises:
                    print crisis.items()
                    print "</br>"
                for person in people:
                    print person.items()
                    print "</br>"
                for org in orgs:
                    print org.items()
                    print "</br>"
                
            except xsv.XsvalError,errstr:
                print errstr
                print "XML Does not Validate"
                

            
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
                               info_birthdate_day = person.find('.//info').find('.//birthdate').find('.//day').text,
                               info_birthdate_month = person.find('.//info').find('.//birthdate').find('.//month').text,
                               info_birthdate_year = person.find('.//info').find('.//birthdate').find('.//year').text,
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
                                     info_loc_country = loc.find('.//country').text)
                    o.put()

        else:
            message = 'No file was uploaded. Try again? </br>'
        
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
           
        # print message


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
    info_birthdate_time = db.IntegerProperty()
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
    


application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/import', ImportPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
