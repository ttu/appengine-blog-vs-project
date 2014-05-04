import os
import sys
import logging

root_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(root_dir, 'lib'))

import webapp2
from blog import *

logging.getLogger().setLevel(logging.DEBUG)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
							   ('/login/?', Login),
                               ('/logout', Logout),
                               ('/oauthgooglecallback/?', OAuthGoogleCallback),
                               ('/oauthfacebookcallback/?', OAuthFacebookCallback)],
                              debug=True)