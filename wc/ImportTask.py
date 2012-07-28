#from XMLHelpers import validXML, parseXML

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def function(x, y):
  z = x*y
  return z

class ImportTask(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <html><body>
    this page does not do anything
    </body></html>
    """)
  
  def post(self):
    x = eval(self.request.get('x'))
    y = eval(self.request.get('y'))

    typee = "***** type is," + str(type(x))
    logging.info(typee)

    string = 'Adding ' + str(x) + '*' + str(y) + ' to the Task Queue.'
    logging.info(string)
    z = function(x, y)
    logging.info("***** z is " + str(z))

application = webapp.WSGIApplication([('/importtask', ImportTask)],
                                     debug=True)
def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
