    def test_parse1(self):
        xml_file = open("test/test_parse1.xml", 'rb')
        XMLHelpers.parseXML(xml_file,1)
        temp = db.GqlQuery("SELECT * FROM Link")
        for i in temp:
        	if i.link_type == "image":
        		
        		assert i.link_url == "https://www.google.com"
        		break
        db.delete(db.Query())   

    def test_parse2(self):
        xml_file = open("test/test_parse2.xml", 'rb')
        XMLHelpers.parseXML(xml_file,1)
        temp = db.GqlQuery("SELECT * FROM Link")
        for i in temp:
        	if i.link_type == "image":
        		assert i.link_url == None 
        		break
        db.delete(db.Query())        
        
    def test_parse3(self):
        xml_file = open("test/test_parse3.xml", 'rb')
        XMLHelpers.parseXML(xml_file,1)
        temp = db.GqlQuery("SELECT * FROM Link")
        for i in temp:
        	if i.link_type == "image":
        		assert i.link_url == None 
        		break
        db.delete(db.Query())   
    
    def test_parse4(self):
        xml_file = open("test/test_parse4.xml", 'rb')
        XMLHelpers.parseXML(xml_file,0)
        temp = db.GqlQuery("SELECT * FROM Link")
        for i in temp:
        	if i.link_type == "image":
        		assert i.link_url == "aaaa"
        		break
        db.delete(db.Query()) 
