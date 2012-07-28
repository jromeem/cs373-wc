#from XMLHelpers import validXML, parseXML

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api.labs import taskqueue 

class RandomPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
    <html><body>
    <form method="post" action="/task-test">
    <input type="submit" value="add task"></form>
    </body></html>
    """)

  def post(self):
    i = 3
    j = 4
    self.response.out.write("""
    <html><body>
    i = 3; j = 4<br>
    adding function to the task queue
    </body></html>
    """)
    
    ### Adding to the task queue ###
    logging.info("***** entering task queue")
    taskqueue.add(url='/importtask', params={'x':i, 'y':j})
    logging.info("***** leaving task queue")

application = webapp.WSGIApplication([('/task-test', RandomPage)],
                                     debug=True)
def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
