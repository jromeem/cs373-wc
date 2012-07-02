import unittest
import XMLHelpers
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
from DataModels import Link, Person, Organization, Crisis
from google.appengine.ext import db

class ExportTests(unittest.TestCase):
    
    def test_buildperson1(self):
        tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        person1 = Person(elemid = "bobs",
                   name = "Bob",
                   info_type = "Salamander",
                   info_birthdate_time = "12:00PM",
                   info_birthdate_day = 12,
                   info_birthdate_month = 12,
                   info_birthdate_year = 1900,
                   info_birthdate_misc = "born under the full moon...",
                   info_nationality = "Swedish",
                   info_biography = "Bob swam a lot, as salamanders do...",
                   
                   orgrefs = ["salamanders united", "salamander liberation front"],
                   crisisrefs = ["swamp famine", "west swamp drought"])
        ptree = SubElement(tree, "person", {"id" : "bobs"})     
        XMLHelpers.buildPerson(ptree, person1)
        
        elemid = ptree.attrib['id'],
        name = ptree.find('.//name').text
        info_type = ptree.find('.//info').find('.//type').text
        info_birthdate_time = ptree.find('.//info').find('.//birthdate').find('.//time').text
        info_birthdate_day = int(ptree.find('.//info').find('.//birthdate').find('.//day').text)
        info_birthdate_month = int(ptree.find('.//info').find('.//birthdate').find('.//month').text)
        info_birthdate_year = int(ptree.find('.//info').find('.//birthdate').find('.//year').text)
        info_birthdate_misc = ptree.find('.//info').find('.//birthdate').find('.//misc').text
        info_nationality = ptree.find('.//info').find('.//nationality').text
        info_biography = ptree.find('.//info').find('.//biography').text

        orgrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]
        
       
        self.assertEqual(elemid[0], person1.elemid)

        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography == person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
        
	def test_buildperson2(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        person1 = Person(elemid = "sally",
                   name = "Sally",
                   info_type = "seahorse",
                   info_birthdate_time = "0:00PM",
                   info_birthdate_day = 1124,
                   info_birthdate_month = 1132,
                   info_birthdate_year = 19000,
                   info_birthdate_misc = "born in a clamshell...",
                   info_nationality = "French",
                   info_biography = "Sally was boring...",
                   
                   orgrefs = ["seahorse united", "seahorse liberation front"],
                   crisisrefs = ["swamp famine", "west swamp drought"])
        ptree = SubElement(tree, "person", {"id" : "sally"})  
        XMLHelpers.buildPerson(ptree, person1)
        
        elemid = ptree.attrib['id'],
        name = ptree.find('.//name').text
        info_type = ptree.find('.//info').find('.//type').text
        info_birthdate_time = ptree.find('.//info').find('.//birthdate').find('.//time').text
        info_birthdate_day = int(ptree.find('.//info').find('.//birthdate').find('.//day').text)
        info_birthdate_month = int(ptree.find('.//info').find('.//birthdate').find('.//month').text)
        info_birthdate_year = int(ptree.find('.//info').find('.//birthdate').find('.//year').text)
        info_birthdate_misc = ptree.find('.//info').find('.//birthdate').find('.//misc').text
        info_nationality = ptree.find('.//info').find('.//nationality').text
        info_biography = ptree.find('.//info').find('.//biography').text

        orgrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]
        
       

        self.assertEqual(elemid[0], person1.elemid)

        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography == person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
        
	def test_buildperson3(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        person1 = Person(elemid = "null",
                   name = "",
                   info_type = "",
                   info_birthdate_time = "",
                   info_birthdate_day = 0,
                   info_birthdate_month = 0,
                   info_birthdate_year = 0,
                   info_birthdate_misc = "",
                   info_nationality = "",
                   info_biography = "",
                   
                   orgrefs = [],
                   crisisrefs = [])
        ptree = SubElement(tree, "person", {"id" : "null"})     
        XMLHelpers.buildPerson(ptree, person1)
        
        
        elemid = ptree.attrib['id']
        name = ptree.find('.//name').text
        info_type = ptree.find('.//info').find('.//type').text
        info_birthdate_time = ptree.find('.//info').find('.//birthdate').find('.//time').text
        info_birthdate_day = int(ptree.find('.//info').find('.//birthdate').find('.//day').text)
        info_birthdate_month = int(ptree.find('.//info').find('.//birthdate').find('.//month').text)
        info_birthdate_year = int(ptree.find('.//info').find('.//birthdate').find('.//year').text)
        info_birthdate_misc = ptree.find('.//info').find('.//birthdate').find('.//misc').text
        info_nationality = ptree.find('.//info').find('.//nationality').text
        info_biography = ptree.find('.//info').find('.//biography').text

        orgrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]

        
        self.assertEqual(elemid, person1.elemid)

        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography == person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
		
	def test_buildorg1(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        organization1 = Organization(elemid = "Franch",
    
                                    name = "French pride",
    
                                    info_type = "non-existant",
                                    info_history = "white flags",
                                    info_contacts_phone = "1234567890",
                                    info_contacts_email = "omuledu@fromage.com",
                                    info_contacts_address = "French",
                                    info_contacts_city = "Paris",
                                    info_contacts_state = "Canada",
                                    info_contacts_country = "USA",
                                    info_contacts_zip = "7890",
    
                                    info_loc_city = "Alaska",
                                    info_loc_region = "Ukraine",
                                    info_loc_country = "Antarctica",
    
                                    personrefs = ["baquettes", "crumpets"],
                                    crisisrefs = ["war", "nazis"],
    
                                    misc = "")

        otree = SubElement(tree, "organization", {"id" : "Franch"})     
        XMLHelpers.buildPerson(ptree, organization1)
	    
        elemid = otree.attrib['id'],
        name = otree.find('.//name').text
        info_type = otree.find('.//info').find('.//type').text
        info_history = otree.find('.//info').find('.//history').text
        info_contacts_phone = otree.find('.//info').find('.//contact').find('.//phone').text
        info_contacts_email = otree.find('.//info').find('.//contact').find('.//email').text
        info_contacts_address = otree.find('.//info').find('.//contact').find('.//mail').find('.//address').text
        info_contacts_city = otree.find('.//info').find('.//contact').find('.//mail').find('.//city').text
        info_contacts_state = otree.find('.//info').find('.//contact').find('.//mail').find('.//state').text
        info_contacts_country = otree.find('.//info').find('.//contact').find('.//mail').find('.//country').text
        info_contacts_zip = otree.find('.//info').find('.//contact').find('.//mail').find('.//zip').text
        info_loc_city = otree.find('.//info').find('.//loc').find('.//city').text
        info_loc_region = otree.find('.//info').find('.//loc').find('.//region').text
        info_loc_country = otree.find('.//info').find('.//loc').find('.//country').text

        personrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]
        misc = otree.find('.//misc').text
        
        self.assert_(elemid == organization1.elemid)
        self.assert_(name == organization1.name)
        self.assert_(info_type == organization1.info_type)
        self.assert_(info_history == organization1.info_history)
        self.assert_(info_contacts_phone == organization1.info_contacts_phone)
        self.assert_(info_contacts_email == organization1.info_contacts_email)
        self.assert_(info_contacts_address == organization1.info_contacts_address)
        self.assert_(info_contacts_city == organization1.info_contacts_city)
        self.assert_(info_contacts_state == organization1.info_contacts_state)
        self.assert_(info_contacts_country == organization1_info_contacts_country)
        self.assert_(info_contacts_zip == organization1.info_contacts_zip)
        self.assert_(info_loc_city == organization1.info_loc_city)
        self.assert_(info_loc_region = organization1.info_loc_region)
        self.assert_(info_loc_country = organization1.info_loc_country)
        self.assert_(misc == organization1.misc)
        self.assert_(personrefs == organization1.personrefs)
        self.assert_(crisisrefs == organization1.crisisrefs)
	    
	def test_buildorg2(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        organization2 = Organization(elemid = "crap",
    
                                    name = "crap",
    
                                    info_type = "",
                                    info_history = "",
                                    info_contacts_phone = "",
                                    info_contacts_email = "",
                                    info_contacts_address = "",
                                    info_contacts_city = "",
                                    info_contacts_state = "",
                                    info_contacts_country = "",
                                    info_contacts_zip = "",
    
                                    info_loc_city = "",
                                    info_loc_region = "",
                                    info_loc_country = "",
    
                                    personrefs = [],
                                    crisisrefs = [],
    
                                    misc = "")

        otree = SubElement(tree, "organization", {"id" : "crap"})     
        XMLHelpers.buildPerson(ptree, organization2)
	    
        elemid = otree.attrib['id'],
        name = otree.find('.//name').text
        info_type = otree.find('.//info').find('.//type').text
        info_history = otree.find('.//info').find('.//history').text
        info_contacts_phone = otree.find('.//info').find('.//contact').find('.//phone').text
        info_contacts_email = otree.find('.//info').find('.//contact').find('.//email').text
        info_contacts_address = otree.find('.//info').find('.//contact').find('.//mail').find('.//address').text
        info_contacts_city = otree.find('.//info').find('.//contact').find('.//mail').find('.//city').text
        info_contacts_state = otree.find('.//info').find('.//contact').find('.//mail').find('.//state').text
        info_contacts_country = otree.find('.//info').find('.//contact').find('.//mail').find('.//country').text
        info_contacts_zip = otree.find('.//info').find('.//contact').find('.//mail').find('.//zip').text
        info_loc_city = otree.find('.//info').find('.//loc').find('.//city').text
        info_loc_region = otree.find('.//info').find('.//loc').find('.//region').text
        info_loc_country = otree.find('.//info').find('.//loc').find('.//country').text

        personrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]
        misc = otree.find('.//misc').text
	    
        self.assert_(elemid == organization2.elemid)
        self.assert_(name == organization2.name)
        self.assert_(info_type == organization2.info_type)
        self.assert_(info_history == organization2.info_history)
        self.assert_(info_contacts_phone == organization2.info_contacts_phone)
        self.assert_(info_contacts_email == organization2.info_contacts_email)
        self.assert_(info_contacts_address == organization2.info_contacts_address)
        self.assert_(info_contacts_city == organization2.info_contacts_city)
        self.assert_(info_contacts_state == organization2.info_contacts_state)
        self.assert_(info_contacts_country == organization2_info_contacts_country)
        self.assert_(info_contacts_zip == organization2.info_contacts_zip)
        self.assert_(info_loc_city == organization2.info_loc_city)
        self.assert_(info_loc_region = organization2.info_loc_region)
        self.assert_(info_loc_country = organization2.info_loc_country)
        self.assert_(misc == organization2.misc)
        self.assert_(personrefs == organization2.personrefs)
        self.assert_(crisisrefs == organization2.crisisrefs)
	    
	def test_buildorg3(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        organization3 = Organization(elemid = "new1",
    
                                    name = "n2123",
    
                                    info_type = "stant",
                                    info_history = "sadvass",
                                    info_contacts_phone = "sdfasdc2345",
                                    info_contacts_email = "asdjhkch234",
                                    info_contacts_address = "Japan",
                                    info_contacts_city = "hates",
                                    info_contacts_state = "baka",
                                    info_contacts_country = "gaijins",
                                    info_contacts_zip = "who",
    
                                    info_loc_city = "act",
                                    info_loc_region = "like",
                                    info_loc_country = "weaboos",
    
                                    personrefs = ["sushi", "fish"],
                                    crisisrefs = ["perl harbor", "atom bombs"],
    
                                    misc = "")

        otree = SubElement(tree, "organization", {"id" : "new1"})     
        XMLHelpers.buildPerson(ptree, organization3)
	    
        elemid = otree.attrib['id'],
        name = otree.find('.//name').text
        info_type = otree.find('.//info').find('.//type').text
        info_history = otree.find('.//info').find('.//history').text
        info_contacts_phone = otree.find('.//info').find('.//contact').find('.//phone').text
        info_contacts_email = otree.find('.//info').find('.//contact').find('.//email').text
        info_contacts_address = otree.find('.//info').find('.//contact').find('.//mail').find('.//address').text
        info_contacts_city = otree.find('.//info').find('.//contact').find('.//mail').find('.//city').text
        info_contacts_state = otree.find('.//info').find('.//contact').find('.//mail').find('.//state').text
        info_contacts_country = otree.find('.//info').find('.//contact').find('.//mail').find('.//country').text
        info_contacts_zip = otree.find('.//info').find('.//contact').find('.//mail').find('.//zip').text
        info_loc_city = otree.find('.//info').find('.//loc').find('.//city').text
        info_loc_region = otree.find('.//info').find('.//loc').find('.//region').text
        info_loc_country = otree.find('.//info').find('.//loc').find('.//country').text

        personrefs = [x.attrib['idref'] for x in ptree.findall('.//org')]
        crisisrefs = [x.attrib['idref'] for x in ptree.findall('.//crisis')]
        misc = otree.find('.//misc').text
	    
        self.assert_(elemid == organization3.elemid)
        self.assert_(name == organization3.name)
        self.assert_(info_type == organization3.info_type)
        self.assert_(info_history == organization3.info_history)
        self.assert_(info_contacts_phone == organization3.info_contacts_phone)
        self.assert_(info_contacts_email == organization3.info_contacts_email)
        self.assert_(info_contacts_address == organization3.info_contacts_address)
        self.assert_(info_contacts_city == organization3.info_contacts_city)
        self.assert_(info_contacts_state == organization3.info_contacts_state)
        self.assert_(info_contacts_country == organization3_info_contacts_country)
        self.assert_(info_contacts_zip == organization3.info_contacts_zip)
        self.assert_(info_loc_city == organization3.info_loc_city)
        self.assert_(info_loc_region = organization3.info_loc_region)
        self.assert_(info_loc_country = organization3.info_loc_country)
        self.assert_(misc == organization3.misc)
        self.assert_(personrefs == organization3.personrefs)
        self.assert_(crisisrefs == organization3.crisisrefs)
		
	def test_buildcrisis1(self):
	    return False
	def test_buildcrisis2(self):
	    return False
	def test_buildcrisis3(self):
	    return False

	def test_exportlinks1(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        person1 = Person(elemid = "bobs",
                   name = "Bob",
                   info_type = "Salamander",
                   info_birthdate_time = "12:00PM",
                   info_birthdate_day = 12,
                   info_birthdate_month = 12,
                   info_birthdate_year = 1900,
                   info_birthdate_misc = "born under the full moon...",
                   info_nationality = "Swedish",
                   info_biography = "Bob swam a lot, as salamanders do...",
                   
                   orgrefs = ["salamanders united", "salamander liberation front"],
                   crisisrefs = ["swamp famine", "west swamp drought"])
        ptree = SubElement(tree, "person", {"id" : "bobs"})     
        XMLHelpers.buildPerson(ptree, person1)
        
        link1 = Link(link_parent = "bobs",
                    link_type = "salad",
                    title = "don't click me!!!",
                    link_url = "http://www.nevergohere.com",
                    description = "you really shouldn't go there...",
                    link_site = "a bad place")
        XMLHelpers.link_list.append(link1)
        
        XMLHelpers.exportLinks(person1, ptree)
        
        for ref in ptree.findall('.//ref'):
            for l in ref:
                new_link = Link()
                if (l.tag):
                    new_link.link_type = l.tag
                if (l.find('./site') != None):
                    new_link.link_site = l.find('./site').text
                if (l.find('./title') != None):
                    new_link.title = l.find('./title').text
                if (l.find('./url') != None):
                    new_link.link_url = db.Link(l.find('./url').text)
                if (l.find('./description') != None):
                    new_link.description = l.find('./description').text
                new_link.link_parent = ptree.attrib['id']
                
        self.assert_(new_link.link_type == link1.link_type)
        self.assert_(new_link.link_site == link1.link_site)
        self.assert_(new_link.title == link1.title)
        self.assert_(new_link.link_url == link1.link_url)
        self.assert_(new_link.description == link1.description)
        self.assert_(new_link.link_parent == link1.link_parent)
        
	def test_exportlinks2(self):
	    return False
	def test_exportlinks3(self):
		return False
		
		

		
class ImportTests(unittest.TestCase):        
    
    def test_validxml1(self):
        return False
    def test_validxml2(self):
        return False
    def test_validxml3(self):
        return False

    
    def test_addperson1(self):
        xml_file = open("test_instance1.xml", 'w')
        tree = ElementTree.parse(xml_file)

        people = tree.findall(".//person")
        
    def test_addperson2(self):
        xml_file = open("test_instance1.xml", 'w')
        tree = ElementTree.parse(xml_file)

        people = tree.findall(".//person")
        
        
    def test_addperson3(self):
        xml_file = open("test_instance1.xml", 'w')
        tree = ElementTree.parse(xml_file)

        people = tree.findall(".//person")
        

        
            
    def test_addorg1(self):
        return False
    def test_addorg2(self):
        return False
    def test_addorg3(self):
        return False
            
    def test_addcrisis1(self):
        return False
    def test_addcrisis2(self):
        return False
    def test_addcrisis3(self):
        return False
            
    def test_grablinks1(self):
        crisis = Element("crisis", {"id" : "wow"})
        ref = SubElement(crisis, "ref")
        img = SubElement(ref, "image")
        site = SubElement(img, "site")
        site.text = "i'm a site"
        title = SubElement(img, "title")
        title.text = "i'm a title"
        url = SubElement(img, "url")
        url.text = "i'm a url"
        description = SubElement(img, "description")
        description.text = "i'm a description"
        
        temp = XMLHelpers.grabLinks(crisis)
        assert (temp[0].link_site == "i'm a site")
        XMLHelpers.clearGlobals()
        
    def test_grablinks2(self):
        person = Element("person", {"id" : "globetrotter"})
        ref = SubElement(person, "ref")
        img = SubElement(ref, "image")
        site = SubElement(img, "site")
        site.text = "i'm a site"
        title = SubElement(img, "title")
        title.text = "i'm a title"
        url = SubElement(img, "url")
        url.text = "i'm a url"
        description = SubElement(img, "description")
        description.text = "i'm a description"
        
        img2 = SubElement(ref, "video")
        site2 = SubElement(img, "site")
        site2.text = "youtube"
        title2 = SubElement(img, "title")
        title2.text = "dancing cats"
        url2 = SubElement(img, "url")
        url2.text = "http://youtube.com/watch?v=si7f8f7tiuhsfi"
        description2 = SubElement(img, "description")
        description2.text = "the cats are dancing!!!"
        
        temp = XMLHelpers.grabLinks(person)
        assert (len(temp) == 2)
        XMLHelpers.clearGlobals()
        
    def test_grablinks3(self):
        person = Element("person", {"id" : "globetrotter"})
        temp = XMLHelpers.grabLinks(person)
        assert (len(temp) == 0)
        XMLHelpers.clearGlobals()
        
        
        
