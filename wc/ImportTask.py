#from XMLHelpers import validXML, parseXML

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import XMLHelpers
import cPickle
import zlib

def function(x, y):
  z = x*y
  return z

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
	'''
	x = eval(self.request.get('x'))
	y = eval(self.request.get('y'))

	typee = "***** type is," + str(type(x))
	logging.info(typee)

	string = 'Adding ' + str(x) + '*' + str(y) + ' to the Task Queue.'
	logging.info(string)
	z = function(x, y)
	logging.info("***** z is " + str(z))
	'''

	logging.info('***** starting task')

	
	#crises = self.request.get('crises')
	
	crisis = zloads(self.request.body)
	XMLHelpers.addCrisis(crisis)
	"""
	orgs = self.request.get('orgs')
	people = self.request.get('people')
	flags = self.request.get('flags')	 
	"""
	
"""	  
	#build crisis list
	for crisis in crises:
		XMLHelpers.addCrisis(crisis)

	#build person list
	for person in people:
		XMLHelpers.addPerson(person)

	#build organization list
	for org in orgs:
		XMLHelpers.addOrganization(org)
"""	  
"""		
	check = 0
	merge = 0
  """  
	#logging.info('***** finished task')

application = webapp.WSGIApplication([('/importtask', ImportTask)],
									 debug=True)
def main():
	run_wsgi_app(application)
			
if __name__ == "__main__":
	main()
