# temporary script to delete all data-store enities
# for debug-use only

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Meow(webapp.RequestHandler):
    def get(self):
        db.delete(db.Query())
        #db.delete(Entry.all())
        self.response.out.write("deleted your crap!")

application = webapp.WSGIApplication([('/meow', Meow)],
                                     debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
