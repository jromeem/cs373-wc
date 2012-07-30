#from XMLHelpers import validXML, parseXML

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import XMLHelpers
import cPickle
import zlib

def zloads(zstr):
  return cPickle.loads(zlib.decompress(zstr))

class ImportTask(webapp.RequestHandler):
  def get(self):
	self.response.out.write("""
	<html><body>
	this page does not do anything
	</body></html>
	""")
  
  def post(self):

	#logging.info('***** starting task')

	
	#crises = self.request.get('crises')

	payload = zloads(self.request.body)
	if payload[0] == 'crisis':
	    XMLHelpers.addCrisis(payload[1])
	if payload[0] == 'person':
	    XMLHelpers.addPerson(payload[1])
	if payload[0] == 'org':
	    XMLHelpers.addOrganization(payload[1])
	
	
	#logging.info("AHHJDKHSKJHSJHKJKHJKHJKHJLHKLHJJLHK")
	#logging.info('***** finished task')

    

application = webapp.WSGIApplication([('/importtask', ImportTask)],
									 debug=True)
def main():
	run_wsgi_app(application)
			
if __name__ == "__main__":
	main()
