import os
import re

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

# Credentials you get from registering a new application
client_id = 'yourcode'
client_secret = 'yoursecret'
redirect_uri = 'https://yoururl.appspot.com/oauthfacebookcallback'     # Should match Site URL

# OAuth endpoints given in the Facebook API documentation
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'

class OAuth2Facebook():

    def __init__(self):	
        self._facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
        self._facebook = facebook_compliance_fix(self._facebook)

    def get_authorization_url(self):
        authorization_url, state = self._facebook.authorization_url(authorization_base_url)
        return str(authorization_url)

    def fetch_token(self, code, response):
        return self._facebook.fetch_token(token_url, client_secret=client_secret, 
                                          authorization_response=response)
        
    def get_profile(self):
        request = self._facebook.get('https://graph.facebook.com/me?')
        return request.content