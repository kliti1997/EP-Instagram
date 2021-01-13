import json
import re

class ProfileData:
    """
    Class to wrap all profile data.
    """

    def __init__(self, initial_data, requests):
        """
                posts / igtvs / tagged structure:
                    type (str): 'image' or 'video'
                    id (str): alphabetical URL id
                    comments (int): number of comments
                    likes (int): number of likes
                    view_count (int): number of views (for videos only)
                """
        self.num_followers = -1
        self.num_following = -1
        self.story_timestamp = -1
        self.posts = []  # Includes Posts, IGTVs and Tagged
        self.igtvs = []
        self.tagged = []
        self.profile_pic_url = ''

        self._initial = initial_data
        self._user = self._initial["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        self._requests = requests
        self.read_followers()
        self.read_following()
        self.read_story()
        self.read_initial_nodes()
        self.read_additional_nodes()
        self.read_profile_pic_name()

    def __str__(self):
        res = f"followers: {self.num_followers}\nfollowing: {self.num_following}\nstory_timestamp: {str(self.story_timestamp)}\nnodes:\n"
        for node in self.posts:
            res += str(node) + "\n"
        return res

    def read_following(self):
        self.num_following = self._user["edge_follow"]["count"]

    def read_followers(self):
        self.num_followers = self._user["edge_followed_by"]["count"]

    def read_profile_pic_url(self):
        url = self._user['profile_pic_url']
        self.profile_pic_url = re.search("([^/]*).jpg", url).group()  # filename of the image

    @staticmethod
    def append_edges_to_list(parent_edge, target_list) -> None:
        for edge in parent_edge:
            child = edge["node"]
            item = {'type': 'video' if child["is_video"] else 'image',
                    'id': child["shortcode"],
                    'comments': child["edge_media_to_comment"]["count"],
                    'likes': child["edge_media_preview_like"]["count"]}
            if child["is_video"]:
                item.update({'view_count': child["video_view_count"]})
            if 'edge_media_preview_like' in child:
                item.update({'likes': child["edge_media_preview_like"]["count"]})  # item 13-24
            else:
                item.update({'likes': child["edge_media_to_comment"]["count"]})  # item 1-12

            target_list.append(item)

    def read_initial_nodes(self):
        """
        Extracts the first 12 posts / IGTVs from 'window._sharedData'
        Tagged posts are only loaded via additional requests.
        """
        self.append_edges_to_list(self._user["edge_owner_to_timeline_media"]["edges"], self.posts)
        self.append_edges_to_list(self._user["edge_felix_video_timeline"]["edges"], self.igtvs)

    def read_additional_nodes(self) -> None:
        """
        Identifies responses to requests that contain data about posts / IGTVs / tagged and saves that data to corresponding lists.
        Responses can be clearly identified by the existence (and abundance) of JSON nodes like 'edge_owner_to_timeline_media' for posts.
        """
        for request in self._requests:
            if request.response:
                if 'graphql' in request.url:
                    reply_content = request.response.body.decode('utf-8')

                    if 'edge_owner_to_timeline_media' in reply_content and 'edge_suggested_users' not in reply_content:  # posts
                        root = json.loads(reply_content)
                        parent_edge = root["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
                        self.append_edges_to_list(parent_edge, self.posts)
                        continue

                    if 'edge_felix_video_timeline' in reply_content:  # igtv
                        root = json.loads(reply_content)
                        parent_edge = root["data"]["user"]["edge_felix_video_timeline"]["edges"]
                        self.append_edges_to_list(parent_edge, self.igtvs)
                        continue

                    if 'edge_user_to_photos_of_you' in reply_content:  # tagged
                        root = json.loads(reply_content)
                        parent_edge = root["data"]["user"]["edge_user_to_photos_of_you"]["edges"]
                        self.append_edges_to_list(parent_edge, self.tagged)
                        continue

    def read_story(self):
        """
        Checks if an active story exists.
        Sets story timestamp accordingly.
        """
        for request in self._requests:
            if request.response:
                if 'graphql' in request.url:
                    reply_content = request.response.body.decode('utf-8')
                    if 'latest_reel_media' in reply_content and 'edge_suggested_users' not in reply_content:
                        reply_json = json.loads(reply_content)
                        self.story_timestamp = reply_json['data']['user']['reel']['latest_reel_media']
                        return
        raise RuntimeError("No request found that contains info about stories of the given user")
