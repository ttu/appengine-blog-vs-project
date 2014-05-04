from google.appengine.ext import db
from google.appengine.api import memcache
from rendering import *

key = "posts"

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    created_by = db.StringProperty(required = True)
    display_name = db.StringProperty(required = True)

    @staticmethod
    def get_posts(update = False):
        posts = memcache.get(key)
        if posts is None or update:
            posts = Post.all().order('-created')
            memcache.set(key, posts)
        return posts

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)