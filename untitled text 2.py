from google.appengine.api.urlfetch import DownloadError 
import httplib
import urlparse
import urllib

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
        
# Uses HTTP request to see if the url given is valid
# url : url
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

            try:
            	if (l.find('./url') != None and urllib.urlopen(l.find('./url').text) and check_url(l.find('./url').text)):
                	new_link.link_url = l.find('./url').text
            except IOError, DownloadError:
            		new_link.link_url = None