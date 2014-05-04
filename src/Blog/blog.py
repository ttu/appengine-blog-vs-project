import webapp2
import logging
import Cookie
import datetime
from google.appengine.ext import db
from google.appengine.api import users

from rendering import *
from user import User
from userProfile import *
from post import Post
from oAuth2Google import *
from oAuth2Facebook import *
from security import *

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

oauth_google = OAuth2Google()
oauth_facebook = OAuth2Facebook()

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        if self.user is None:
            params['username'] = ''
        else:
            params['username'] = self.user.name

        params['login_url_facebook'] = ('/login?type=facebook')
        params['login_url_google'] = ('/login?type=google')

        params['logout_url'] = ('/logout')

        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.user = None
        uid = self.read_secure_cookie('user_id')
        if uid:
            self.user = User.by_user_id(int(uid))
            #self.update_secure_cookie('user_id', uid)
        # This is for google.appengine.api users
        #self.user = users.get_current_user()
        # This is for debugging
        #self.user = DebugUser()
        #User.try_add_user(self.user)
        #self.set_secure_cookie('user_id', str(self.user.id))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/; HttpOnly;' % (name, cookie_val))
        #expires = datetime.datetime.now() + datetime.timedelta(hours=1)
        #c = Cookie.SimpleCookie()
        #c[name]['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S') # Wdy, DD-Mon-YY HH:MM:SS GMT
        #c[name] = cookie_val

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def update_secure_cookie(self, name):
        set_secure_cookie(self, name, val)

    def clear_secure_cookie(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

class MainPage(BlogHandler):
  def get(self):
      self.redirect("/blog")

class BlogFront(BlogHandler):
    def get(self):
        posts = Post.get_posts()
        self.render('front.html', posts = posts)
    def getUser(self):
        return users.get_current_user()

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect(users.create_login_url('/login'))

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        created_by = self.user.user_id
        display_name = self.user.name

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, 
                     created_by = created_by, display_name = display_name)
            p.put()
            #rerun the query and update the cache
            Post.get_posts(True)

            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class Login(BlogHandler):
   def get(self):
        type = self.request.get('type')
        if type == 'google':
            self.redirect(oauth_google.get_authorization_url())
        elif type == 'facebook':
            self.redirect(oauth_facebook.get_authorization_url())
        else:
            self.redirect('/blog')

class Logout(BlogHandler):
    def get(self):
        self.clear_secure_cookie()
        self.redirect('/blog')

class OAuthCallbackHandler(BlogHandler):
    def process(self, oAuth):
        code = self.request.get('code')
        logging.debug('Code: %s', code)

        token = oAuth.fetch_token(code, self.request.url)
        logging.debug('Token: %s', token)

        profile = oAuth.get_profile()
        logging.debug('Profile: %s', profile)
        
        user = UserProfile(profile)
        User.try_add_user(user)
        self.set_secure_cookie('user_id', str(user.id))

        self.redirect('/blog')

class OAuthGoogleCallback(OAuthCallbackHandler):
    def get(self):
        self.process(oauth_google)

class OAuthFacebookCallback(OAuthCallbackHandler):
    def get(self):
        self.process(oauth_facebook)

class DebugUser():

    def __init__(self):
        self.name = "James"
        self.id = "1234"
