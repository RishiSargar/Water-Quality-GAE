import webapp2
import logging

MAIN_PAGE_HTML = """<html>
<head>
<meta name="google-site-verification" content="sZkBe87qAnjSshAdYU-UuMIrzotExNMY0WydkAagojM" />
</head>
<body>
test
</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)