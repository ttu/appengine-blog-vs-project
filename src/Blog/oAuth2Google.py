import os
import re

from requests_oauthlib import OAuth2Session

# Credentials you get from registering a new application
client_id = 'yourid'
client_secret = 'yoursecret'
redirect_uri = 'https://yoururl.appspot.com/oauthgooglecallback'

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"
scope = ["https://www.googleapis.com/auth/userinfo.profile"]

class OAuth2Google():

    def __init__(self):	
        self._google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

    def get_authorization_url(self):
        authorization_url, state = self._google.authorization_url(authorization_base_url,
            access_type="online", approval_prompt="auto")
        return str(authorization_url)

    def fetch_token(self, code, response):
        return self._google.fetch_token(token_url, client_secret=client_secret,
                authorization_response=response)
        
    def get_profile(self):
        request = self._google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        return request.content