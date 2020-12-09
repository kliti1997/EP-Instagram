import json


class ProfileData:
    #TODO: Exceptions fangen, aufhübschen
    """
    Class to wrap all profile data.
    """
    num_followers = -1
    num_following = -1
    story_timestamp = -1
    nodes = []  # Beinhaltet Posts, IGTV's, Markiert
    """
    Node structure:
      type (str): 'image' or 'video'
      id (str): alphabetical URL id
      comments (int): number of comments
      likes (int): number of likes
      view_count (int): number of views (for videos only)
    """

    def __init__(self, initial_data, requests):
        self._initial = initial_data
        self._user = self._initial["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        self._requests = requests

        self.read_followers()
        self.read_following()
        self.read_story()
        self.read_initial_nodes()
        self.read_additional_nodes()

    def __str__(self):
        res = f"followers: {self.num_followers}\nfollowing: {self.num_following}\nstory_timestamp: {str(self.story_timestamp)}\nnodes:\n"
        for node in self.nodes:
            res += str(node) + "\n"
        return res

    def read_following(self):
        self.num_following = self._user["edge_follow"]["count"]

    def read_followers(self):
        self.num_followers = self._user["edge_followed_by"]["count"]

    def read_initial_nodes(self):
        for edge in self._user["edge_owner_to_timeline_media"]["edges"]:
            node = {'type': 'video' if edge["node"]["is_video"] else 'image',
                    'id': edge["node"]["shortcode"],
                    'comments': edge["node"]["edge_liked_by"]["count"],
                    'likes': edge["node"]["edge_liked_by"]["count"]}

            if edge["node"]["is_video"]:
                node.update({'view_count': edge["node"]["video_view_count"]})
            self.nodes.append(node)

    def read_additional_nodes(self):
        for request in self._requests:
            if request.response:
                if 'graphql' in request.url:
                    reply_content = request.response.body.decode('utf-8')
                    if 'edge_owner_to_timeline_media' in reply_content:
                        root = json.loads(reply_content)
                        for edge in root["data"]["user"]["edge_owner_to_timeline_media"]["edges"]:
                            node = {'type': 'video' if edge["node"]["is_video"] else 'image',
                                    'id': edge["node"]["shortcode"],
                                    'comments': edge["node"]["edge_media_to_comment"]["count"],
                                    'likes': edge["node"]["edge_media_preview_like"]["count"]}
                            if edge["node"]["is_video"]:
                                node.update({'view_count': edge["node"]["video_view_count"]})
                            self.nodes.append(node)

    def read_story(self):
        """
        Checks if an active story exists.
        Sets story timestamp accordingly.
        """
        for request in self._requests:
            if request.response:
                if 'graphql' in request.url:
                    reply_content = request.response.body.decode('utf-8')
                    if 'latest_reel_media' in reply_content and 'edge_suggested_users' not in reply_content:  # Identifying correct request
                        reply_json = json.loads(reply_content)
                        self.story_timestamp = reply_json['data']['user']['reel']['latest_reel_media']
