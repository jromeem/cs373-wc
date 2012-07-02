# Group Import Angtigravity
# TestWC1.py

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, dump
from minixsv import pyxsval as xsv

from DataModels import Link, Person, Organization, Crisis

import unittest
from XMLHelpers import validXML, grabLinks, addCrisis, addPerson, addOrganization
from XMLHelpers import exportLinks, buildCrisis, buildOrganization, buildPerson

crisis_list = []
person_list = []
organization_list = []
link_list = []

class ExportTests(unittest.TestCase):
		
    def test_buildperson1(self):

    def test_buildperson2(self):

    def test_buildperson3(self):

            
    def test_buildorg1(self):

    def test_buildorg2(self):

    def test_buildorg3(self):

            
    def test_buildcrisis1(self):

    def test_buildcrisis2(self):

    def test_buildcrisis3(self):


    def test_exportlinks1(self):

    def test_exportlinks2(self):

    def test_exportlinks3(self):
        
		
		
class ImportTests(unittest.TestCase):        
    
    def test_validxml1(self):

    def test_validxml2(self):

    def test_validxml3(self):
        

    
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
        
    def test_addorg2(self):
        
    def test_addorg3(self):
            
            
    def test_addcrisis1(self):
        
    def test_addcrisis2(self):
        
    def test_addcrisis3(self):
        
            
    def test_grablinks1(self):
        
    def test_grablinks2(self):
        
    def test_grablinks3(self):
