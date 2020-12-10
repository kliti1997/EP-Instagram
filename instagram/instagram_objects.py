from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

class InstagramObjects:
    def __init__(self, url=None):
        if url is None:
            self.followers = 0
            self.following = 0
            self.posts = []
            self.igtvs = []
            self.tags = []
        else:
            self.followers = self.set_followers(url)
            self.following = self.set_following(url)
            self.posts = self.set_posts(url)
            self.igtvs = self.set_igtvs(url)
            self.tags = self.set_tags(url)

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

    def set_followers(self):
        pass

    def set_following(self):
        pass

    def set_posts(self):
        pass

    def set_igtvs(self):
        pass

    def set_tags(self):
        pass
