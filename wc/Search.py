import cgi, os, sys
import cgitb; cgitb.enable()
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
template.register_template_library('django.contrib.humanize.templatetags.humanize')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from DataModels import Crisis, Organization, Person
import django.contrib.humanize.templatetags.humanize

import google.appengine.api.search

class SearchResults(webapp.RequestHandler):
    def post(self):
        search_query = self.request.get('q')
        print search_query

        
        # Get the index.
        index = search.Index(name='index-name',
                             consistency=Index.PER_DOCUMENT_CONSISTENT)
        """
        # Create a document.
        doc = search.Document(
            doc_id='document-id',
            fields=[search.TextField(name='subject', value='my first email'),
                    search.HtmlField(name='body', value='<html>some content here</html>')])

        # Index the document.
        try:
            index.add(doc)
        except search.AddError, e:
            result = e.results[0]
            if result.code == search.OperationResult.TRANSIENT_ERROR:
                # possibly retry indexing result.object_id
        except search.Error, e:
            # possibly log the failure

        # Query the index.
        try:
            results = index.search('subject:first body:here')

            # Iterate through the search results.
            for scored_document in results:
                print scored_document

        except search.Error, e:
            print "no results"
            # possibly log the failure
        """

application = webapp.WSGIApplication([('/search', SearchResults)], debug=True)

def main():
    run_wsgi_app(application)
            
if __name__ == "__main__":
    main()
