class TwitterUser:
    twitterApi = None

    def setTwitterApi(twitterApi):
        TwitterUser.twitterApi = twitterApi

    def __init__(self, userId=None, userName=None):
        self.basicInfoSet = False
        self.id = userId
        self.name = userName
        self.followersNum = -1
        self.followersList = []
        self.followersListCursor = -1
        self.mentionedList = []

    def requestAndSetBasicInfo(self, useCacheOnly=False):
        if not self.basicInfoSet:
            userObject = TwitterUser.twitterApi.getUserObject(
                screenName=self.name,
                userId=self.id,
                useCacheOnly=useCacheOnly)
            self.id = userObject['id']
            self.name = userObject['screen_name']
            self.followersNum = userObject['followers_count']
            self.basicInfoSet = True

    def requestAndExpandFollowersList(self, useCacheOnly=False):
        if self.basicInfoSet and len(self.followersList) < self.followersNum:
            insertPos = len(self.followersList)
            receivedFollowersList, self.followersListCursor = \
                TwitterUser.twitterApi.getFollowersListForUser(userId=self.id,
                                                               screenName=self.name,
                                                               cursor=self.followersListCursor,
                                                               useCacheOnly=useCacheOnly)
            self.followersList.extend(receivedFollowersList)
            return insertPos, len(receivedFollowersList)
        return None, None
