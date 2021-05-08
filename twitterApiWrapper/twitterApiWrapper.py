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

    def getFollowersListForUser(self, userId=None, screenName=None,
                                cursor=-1, useCacheOnly=False):
        if self.cache is not None:
            if useCacheOnly:
                if not self.cache.checkIfCached(self.twitterApi,
                                                'GetFollowerIDsPaged',
                                                user_id=userId,
                                                screen_name=screenName,
                                                cursor=cursor):
                    raise Exception('Not cached.')
            nextCursor, _, followersList = self.cache.execute(self.twitterApi,
                                                              'GetFollowerIDsPaged',
                                                              user_id=userId,
                                                              screen_name=screenName,
                                                              cursor=cursor)
            return followersList, nextCursor

    def getUserObject(self, userId=None, screenName=None, useCacheOnly=False):
        if self.cache is not None:
            if useCacheOnly:
                if not self.cache.checkIfCached(self.twitterApi, 'GetUser',
                                                user_id=userId,
                                                screen_name=screenName,
                                                return_json=True):
                    raise Exception('Not cached.')
            return self.cache.execute(self.twitterApi, 'GetUser',
                                      user_id=userId,
                                      screen_name=screenName,
                                      return_json=True)
