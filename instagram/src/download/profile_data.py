import json


class ProfileData:
    """
    Class to wrap all profile data.
    """
    num_followers = -1
    num_following = -1
    story_timestamp = -1
    nodes = []  # Beinhaltet Posts, IGTV's, Markiert

    def __init__(self, initial_data, requests):
        self._initial = initial_data
        self._user = self._initial["entry_data"]["ProfilePage"]["graphql"]["user"]
        print(self._user)
        self._requests = requests

    def __str__(self):
        return f"followers: {self.num_followers}\nfollowing: {self.num_following}\nstory_timestamp: {self.story_timestamp}\nnodes:\n" + [str(node) + "\n" for node in self.nodes]

    def read_following(self):
        self.num_following = self._user["edge_follow"]["count"]

    def read_followers(self):
        self.num_followers = self._user["edge_followed_by"]["count"]

    def read_story(self):
        """
        Checks if an active story exists.

        Returns:
            int: timestamp of last story, 0 if none exists
        """
        for request in self.requests:
            if request.response:
                if 'graphql' in request.url:
                    reply_content = request.response.body
                    if 'latest_reel_media' in reply_content and 'edge_suggested_users' not in reply_content:  # Identifying correct request
                        reply_json = json.loads(reply_content)
                        self.story_timestamp = reply_json['data']['user']['reel']['latest_reel_media']
