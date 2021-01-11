from instagram.data.config import *
from instagram.src.helper import get_new_html_path, get_old_html_path
from lxml import etree, html

logger = logging.getLogger('instagram')
NEW = 0
OLD = 1


class InstagramObject:
    def __init__(self, url, flag, content=None):
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
        # Default Video thumbnail path
        self.video_thumbnail_path = os.path.join(config_folder, "video_thumbnail.jpeg")

        self.__set_tree(url, content)
        self.__set_followers(url)
        self.__set_following(url)
        if url["type"] == "posts":
            self.__set_posts()
        elif url["type"] == "igtv":
            self.__set_igtvs()
        elif url["type"] == "tagged":
            self.__set_tags()

    def get_flag(self) -> int:
        """
        The flag specifies if dom objects of a new, or old html
        file are stored in the current instance.

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
        The method returns a list which contains all of the 24 posts, which are included
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

    def get_profile_pic_download(self, picture_url: str) -> etree:
        """
        Returns the etree element of the profile picture in the original DOM.
        """
        return self.tree.xpath(f"//img[starts-with(@src,'{picture_url}')]")[0].getparent()

    def get_profile_pic_modify(self):
        """
        Returns the etree element of the profile picture in the saved html file.
        The get_profile_pic_download can't be used because the picture url is not available anymore.
        """
        return self.tree.xpath("//span[@data-story-timestamp]")[0]

    def get_video_thumbnail_path(self):
        return self.video_thumbnail_path

    def __set_tree(self, url, content) -> None:
        if content is not None:
            print("Test 0")
            print("self.content")
            print(content)
            html_parser = html.HTMLParser()
            self.tree = etree.fromstring(content, parser=html_parser)
        else:
            if self.flag == NEW:
                self.tree = html.parse(get_new_html_path(url))
            elif self.flag == OLD:
                self.tree = html.parse(get_old_html_path(url))
            else:
                logger.error("Flag was not set.")

    def __set_followers(self, url) -> None:
        self.followers = list(
            self.tree.xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/followers/']")[0].iter())[0]

    def __set_following(self, url) -> None:
        self.following = list(
            self.tree.xpath("//a[@href='https://www.instagram.com/" + url["id"] + "/following/']")[0].iter())[0]

    def __set_posts(self) -> None:
        self.posts = self.tree.xpath("//div[@id='react-root']//article//a")

    def __set_igtvs(self) -> None:
        all_links = self.tree.xpath("//div[@id='react-root']//main//div//a")
        self.igtvs = [igtv_ele for igtv_ele in all_links if igtv_ele.attrib["href"].startswith("https://www.instagram.com/tv/")]

    def __set_tags(self) -> None:
        self.tags = self.tree.xpath("//div[@id='react-root']//article//a")

    """
    Returns the Tree,flag, posts etc.
    """
    def __tostr__(self, attr):
        ret = b""
        if attr == "flag":
            return self.get_flag()
        elif attr == "tree":
            return etree.tostring(self.tree, pretty_print=True)
        elif attr == "followers":
            return etree.tostring(self.tree, pretty_print=True)
        elif attr == "following":
            return etree.tostring(self.tree, pretty_print=True)
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
    Saves the etree in a HTML file after the changes were executed. It is important for the download
    phase after inserting the HTML Tags like data-liked-by.
    """
    def write(self, url):
        if self.get_flag() == NEW:
            open(get_new_html_path(url), "wb").write(etree.tostring(self.tree, method="html"))
        else:
            open(get_old_html_path(url), "wb").write(etree.tostring(self.tree, method="html"))
