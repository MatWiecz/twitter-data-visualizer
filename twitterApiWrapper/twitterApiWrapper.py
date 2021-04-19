import twitter
import json


class TwitterApiWrapper:

    def __init__(self, authFileName=None, cache=None):
        if not authFileName:
            raise Exception('The Twitter API requires authorization '
                            'information '
                            'for an initiation. No authorization file name '
                            'provided.')
        self.authFileName = authFileName
        authFileData = {}
        with open(self.authFileName, 'r') as authFile:
            authFileData = json.load(authFile)
        self.twitterApi = twitter.Api(**authFileData)
        self.cache = cache

    def getFollowersListForUser(self, userId=None, screenName=None):
        if self.cache is not None:
            return self.cache.execute(self.twitterApi, 'GetFollowerIDs',
                                      user_id=userId,
                                      screen_name=screenName,
                                      count=5000,
                                      total_count=5000)

    def getUserFromUserId(self, userId=None, screenName=None):
        if self.cache is not None:
            return self.cache.execute(self.twitterApi, 'GetUser',
                                      user_id=userId,
                                      screen_name=screenName,
                                      return_json=True)
