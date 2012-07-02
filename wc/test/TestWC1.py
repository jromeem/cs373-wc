import unittest
import XMLHelpers
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
from DataModels import Link, Person, Organization, Crisis

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
        
       
        #self.assert_(elemid == person1.elemid)
        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography = person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
        
	def test_buildperson2(self):
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
        
       
        #self.assert_(elemid == person1.elemid)
        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography = person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
        
	def test_buildperson3(self):
	    tree = Element("worldCrises", {"xmlns:xsi" : "http://www.w3.org/2001/XMLSchema-instance", "xsi:noNamespaceSchemaLocation" : "wc.xsd"})
        
        person1 = Person(elemid = "null",
                   name = "nully",
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
        
       
        #self.assert_(elemid == person1.elemid)
        self.assert_(name == person1.name)
        self.assert_(info_type == person1.info_type)
        self.assert_(info_birthdate_time == person1.info_birthdate_time)
        self.assert_(info_birthdate_day == person1.info_birthdate_day)
        self.assert_(info_birthdate_month == person1.info_birthdate_month)
        self.assert_(info_birthdate_year == person1.info_birthdate_year)
        self.assert_(info_birthdate_misc == person1.info_birthdate_misc)
        self.assert_(info_nationality == person1.info_nationality)
        self.assert_(info_biography = person1.info_biography)
        self.assert_(orgrefs == person1.orgrefs)
        self.assert_(crisisrefs == person1.crisisrefs)
		
	def test_buildorg1(self):
	    return False
	def test_buildorg2(self):
	    return False
	def test_buildorg3(self):
	    return False
		
	def test_buildcrisis1(self):
	    return False
	def test_buildcrisis2(self):
	    return False
	def test_buildcrisis3(self):
	    return False

	def test_exportlinks1(self):
	    return False
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
        return False
    def test_grablinks2(self):
        return False
    def test_grablinks3(self):
        return False
