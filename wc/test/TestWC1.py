import unittest
import XMLHelpers
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from DataModels import Link, Person, Organization, Crisis

class ExportTests(unittest.TestCase):
		
	def test_buildperson1(self):
	    ptree = ElementTree.ElementTree()
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
                   XMLHelpers.buildPerson(ptree, person1)
                   
                   
                   
	def test_buildperson2(self):
	    return False
	def test_buildperson3(self):
	    return False
		
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
	
	def test_addperson1(self):
	    return False
	def test_addperson2(self):
	    return False
	def test_addperson3(self):
	    return False
		
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
