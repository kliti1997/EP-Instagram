from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

NEW = 0
OLD = 1

class InstagramObject:
    def __init__(self, url, type):
        if type == "new":
            self.type = NEW
        else:
            self.type = OLD
        # Dummy values
        self.tree = None
        self.followers = None
        self.following = None
        self.posts = None
        self.igtvs = None
        self.tags = None

        self.__set_tree(self, url)
        self.__set_followers(self, url)
        self.__set_following(self, url)
        self.__set_posts(self)
        self.__set_igtvs(self)
        self.__set_tags(self)

    def get_type(self):
        return self.type

    def get_tree(self):
        return self.trees

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

    def __set_tree(self, url):
        if self.type == NEW:
            self.tree = html.parse(get_new_html_path(url))
        else:
            self.tree = html.parse(get_old_html_path(url))

    def __set_followers(self, url):
        self.followers = list(
            self.get_tree().xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/followers/']")[0].iter())

    def __set_following(self, url):
        self.following = list(
            self.get_tree().xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/following/']")[0].iter())

    def __set_posts(self):
        self.posts = self.get_tree().xpath("//div[@id='react-root']//article//a")

    def __set_igtvs(self):
        self.igtvs = self.get_tree().xpath("//div[@id='react-root']//main//div//a")

    def __set_tags(self):
        # TODO
        self.tags = (0, 0)
