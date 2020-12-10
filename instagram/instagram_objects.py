from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

class InstagramObjects:
    def __init__(self, url=None):
        if url is None:
            self.followers_new = 0
            self.followers_old = 0
            self.following_new = 0
            self.following_old = 0
            self.posts_new = []
            self.posts_old = []
            self.igtvs_new = []
            self.igtvs_old = []
            self.tags_new = []
            self.tags_old = []
        else:
            self.set_followers(url)
            self.set_following(url)
            self.set_posts(url)
            self.set_igtvs(url)
            self.set_tags(url)

    def get_followers(self):
        return self.followers

    def get_following(self):
        return self.following

    def get_posts(self):
        return self.posts

    def get_igtvs(self):
        return self.igtvs

    def get_tags(self):
        return self.tags

    def set_followers(self, url):
        pass

    def set_following(self, url):
        pass

    def set_posts(self, url):
        pass

    def set_igtvs(self, url):
        pass

    def set_tags(self, url):
        pass
