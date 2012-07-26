import wsgiref.handlers
from google.appengine.ext import webapp
from XMLHelpers import validXML, parseXML


class ImportTask(webapp.RequestHandler):
  def post(self):
    flags = self.request.get('flags')
    file = self.request.get('xml_file')
	
    logging.info('************Parsing file************* '+ file.filename +' to the Task Queue.')
    parseXML(file.file, flags)

    # ... and here you get your hands dirty; use i and do the work.

"""
def main():
  logging.info('************Parsing file************* to the Task Queue.')
  application = webapp.WSGIApplication([
                (r'/importtask', ImportTask),
                ], debug=True)
  
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
"""