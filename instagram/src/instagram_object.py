from instagram.data.config import *
from instagram.src.helper import get_new_html_path, get_old_html_path
from lxml import etree, html

NEW = 0
OLD = 1

class InstagramObject:
    def __init__(self, url, flag):
        if flag == "new":
            self.flag = NEW
        else:
            self.flag = OLD
        # Dummy values
        self.tree = None
        self.followers = None
        self.following = None
        self.posts = None
        self.igtvs = None
        self.tags = None

        self.__set_tree(url)
        self.__set_followers(url)
        self.__set_following(url)
        self.__set_posts()
        self.__set_igtvs()
        self.__set_tags()

    def get_flag(self) -> int:
        """
        The flag specifies if dom objects of a new, or old html
        file are stored in the current isntance.

        Returns:
            int: 0 if objects of a new file are stored, otherwise 1.
        """
        return self.flag

    def get_tree(self) -> etree:
        """
        The dom representation of the html file to inspect.

        Returns:
            etree: The dom tree of the whole html file.
        """
        return self.tree

    def get_followers(self) -> etree:
        """
        The method returns the parent node, which is an a-tag, of the followers count.
        The followers count is the text attribute of the first and only child element, 
        which is a span-tag.

        Example:
        <a class="-nal3 " href="/polizei.hannover/followers/" tabindex="0">
            <span class="g47SY " title="28,324">28.3k</span> 
            followers
        </a>

        Returns:
            etree: The parent node which includes the followers count.
        """
        return self.followers

    def get_following(self) -> etree:
        """
        The method returns the parent node, which is an a-tag, of the followers count.
        The followers count is the text attribute of the first and only child element, 
        which is a span-tag.

        Example:
        <a class="-nal3 " href="/polizei.hannover/following/" tabindex="0">
            <span class="g47SY ">122</span> 
            following
        </a>

        Returns:
            etree: The parent node which includes the following count.
        """
        return self.following

    def get_posts(self) -> list:
        """
        The method returns a list which contains all of the 24 posts, whihc are included
        in the dom tree. 
        We set the first a-tag element as the root element of the post, because it contains
        the most important data like the unique href-attribute, which is referring to the
        thumbnail of the post.

        Example:
        <a href="/p/CInvvcLqYWw/" tabindex="0">
            <div class="eLAPa">
                <div class="KL4Bh">
                    <img alt="Photo by Polizei Hannover " class="FFVAD" ...>
                </div>
                <div class="_9AhH0"></div>
            </div>
        </a>

        Returns:
            list: The list contains etree-elements, each element is a post.
        """
        return self.posts

    def get_igtvs(self) -> list:
        return self.igtvs

    def get_tags(self) -> list:
        return self.tags

    def __set_tree(self, url) -> None:
        if self.flag == NEW:
            self.tree = html.parse(get_new_html_path(url))
        else:
            self.tree = html.parse(get_old_html_path(url))

    def __set_followers(self, url) -> None:
        self.followers = list(
            self.get_tree().xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/followers/']")[0].iter())[0]

    def __set_following(self, url) -> None:
        self.following = list(
            self.get_tree().xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/following/']")[0].iter())[0]

    def __set_posts(self) -> None:
        self.posts = self.get_tree().xpath("//div[@id='react-root']//article//a")

    def __set_igtvs(self) -> None:
        all_links = self.get_tree().xpath("//div[@id='react-root']//main//div//a")
        self.igtvs = [igtv_ele for igtv_ele in all_links if igtv_ele.attrib["href"].startswith("https://www.instagram.com/tv/")]

    def __set_tags(self) -> None:
        # TODO
        self.tags = (0, 0)

    """
    Gibt den Tree, flag, posts, etc. zurück.
    """
    def __tostr__(self, attr):
        ret = b""
        if attr == "flag":
            return self.get_flag()
        elif attr == "tree":
            return etree.tostring(self.get_tree(), pretty_print=True)
        elif attr == "followers":
            return etree.tostring(self.get_followers(), pretty_print=True)
        elif attr == "following":
            return etree.tostring(self.get_following(), pretty_print=True)
        elif attr == "posts":
            for post in self.get_posts():
                ret += etree.tostring(post, pretty_print=True)
        elif attr == "igtvs":
            for igtv in self.get_igtvs():
                ret += etree.tostring(igtv, pretty_print=True)
        elif attr == "tags":
            for tag in self.get_tags():
                ret += etree.tostring(tag, pretty_print=True)
        return ret

    """
    Speichert den etree in einem hthml file ab, nachdem Änderungen vorgenommen worden sind.
    Wichtig für die download Phase, nachdem html tags wie data-liked-by hinzugefügt. worden sind.
    """
    def write(self, url):
        if self.get_flag() == NEW:
            open(get_new_html_path(url), "wb").write(etree.tostring(self.get_tree(), method="html"))
        else:
            open(get_old_html_path(url), "wb").write(etree.tostring(self.get_tree(), method="html"))