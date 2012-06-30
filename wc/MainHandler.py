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
                    c = Crisis(
                               crisisid = crisis.attrib['id'],
                               name = crisis.find('.//name').text,
                               misc = crisis.find('.//misc').text,
                               info_history = crisis.find('.//info').find('.//history').text
                               )
                    c.put()
            
            """
            crisisid = db.StringProperty()

            name = db.StringProperty()
            misc = db.StringProperty()
            
            info_history = db.TextProperty()
            info_help = db.StringProperty()
            info_resources = db.StringProperty()
            info_type = db.StringProperty()
            info_loc = db.ReferenceProperty()
            
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
            """
            

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
    title = db.StringProperty()
    url = db.StringProperty()
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
    info_loc = db.ReferenceProperty()
    
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
