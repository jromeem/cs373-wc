import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class OneDay(webapp.RequestHandler):
    def get(self):
        self.response.out.write("tasks are run here")
        
    def post(self):
        i = int(self.request.get('dayI'))
        for x in range(5):
            self.response.out.write("i is " + str(i*x))

application = webapp.WSGIApplication([('/one-day', OneDay)], debug=True)

def main():
	run_wsgi_app(application)
			
if __name__ == "__main__":
	main()
