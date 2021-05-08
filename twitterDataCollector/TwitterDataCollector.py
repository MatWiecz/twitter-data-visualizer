from localTwitterDatabase.TwitterUser import TwitterUser


class TwitterDataCollector:

    def __init__(self, database, config, cache):
        self.database = database
        self.config = config
        self.pendingGetFollowersListOperations = []
        self.pendingGetUserObjectOperations = []
        self.useCacheOnly = True
        self.cache = cache
        self.cacheToWrite = False

    def executeGetFollowersListOperation(self, userId):
        user = self.database.getUser(userId)
        listInsertPos, listLength = user.requestAndExpandFollowersList(
            self.useCacheOnly)
        requestedNum = 0
        for index in range(listLength):
            curUser = TwitterUser(
                userId=user.followersList[listInsertPos + index])
            self.database.addUser(curUser)
            if requestedNum < self.config['maxNewGetUserObjectOperationsNum']:
                self.pendingGetUserObjectOperations.append(curUser.id)
                requestedNum += 1

    def executeGetUserObjectOperation(self, userId):
        user = self.database.getUser(userId)
        user.requestAndSetBasicInfo(self.useCacheOnly)
        if user.followersNum >= self.config['followersNumThreshold']:
            self.pendingGetFollowersListOperations.append(user.id)

    def startCollecting(self, seedUserScreenName=None):
        seedUser = TwitterUser(userName=seedUserScreenName)
        seedUser.requestAndSetBasicInfo(self.useCacheOnly)
        self.database.addUser(seedUser)
        self.executeGetFollowersListOperation(seedUser.id)

    def continueCollecting(self):
        cacheLoadingFinishedFlag = False
        if self.useCacheOnly:
            useCacheOnlyToUnset = True
            jobsToRemove = []
            for userId in self.pendingGetFollowersListOperations:
                try:
                    self.executeGetFollowersListOperation(userId)
                    useCacheOnlyToUnset = False
                    jobsToRemove.append(userId)
                except Exception:
                    pass
            self.pendingGetFollowersListOperations = [userId for userId in
                                                      self.pendingGetFollowersListOperations
                                                      if
                                                      userId not in jobsToRemove]
            jobsToRemove = []
            for userId in self.pendingGetUserObjectOperations:
                try:
                    self.executeGetUserObjectOperation(userId)
                    useCacheOnlyToUnset = False
                    jobsToRemove.append(userId)
                except Exception:
                    pass
            self.pendingGetUserObjectOperations = [userId for userId in
                                                  self.pendingGetUserObjectOperations
                                                  if
                                                  userId not in jobsToRemove]
            for userDbIndex in range(self.database.getUsersCount()):
                user = self.database.getUserAtIndex(userDbIndex)
                if user.basicInfoSet:
                    continue
                try:
                    self.executeGetUserObjectOperation(user.id)
                    useCacheOnlyToUnset = False
                except Exception:
                    pass
            if useCacheOnlyToUnset:
                self.useCacheOnly = False
                print('Loading from cache finished.')
                cacheLoadingFinishedFlag = True
        else:
            exceptionPoints = 0
            for i in range(5):
                if self.pendingGetFollowersListOperations:
                    bestScore = 0
                    userId = -1
                    for curUserId in self.pendingGetFollowersListOperations:
                        user = self.database.getUser(curUserId)
                        if user.followersNum > bestScore:
                            bestScore = user.followersNum
                            userId = curUserId
                    self.pendingGetFollowersListOperations.remove(userId)
                    try:
                        self.executeGetFollowersListOperation(userId)
                    except Exception:
                        exceptionPoints += 1
                        break

            for i in range(300):
                if self.pendingGetUserObjectOperations:
                    userId = self.pendingGetUserObjectOperations.pop(0)
                    try:
                        self.executeGetUserObjectOperation(userId)
                    except Exception:
                        self.pendingGetUserObjectOperations.append(userId)
                        exceptionPoints += 1
                        break
                else:
                    userDbIndex = 0
                    while userDbIndex < self.database.getUsersCount():
                        user = self.database.getUserAtIndex(userDbIndex)
                        if user.basicInfoSet:
                            userDbIndex += 1
                            continue
                        try:
                            self.executeGetUserObjectOperation(user.id)
                        except Exception:
                            exceptionPoints += 1
                            pass
                        break
            if exceptionPoints == 2:
                if self.cacheToWrite:
                    self.cache.forceCacheDump()
                    self.cacheToWrite = False
            else:
                self.cacheToWrite = True

        totalUserIdsNum = self.database.getUsersCount()
        userIdsWithBasicInfoNum = 0
        userIdsWithFollowersList = 0
        for userIndex in range(totalUserIdsNum):
            user = self.database.getUserAtIndex(userIndex)
            if user.basicInfoSet:
                userIdsWithBasicInfoNum += 1
            if len(user.followersList) > 0:
                userIdsWithFollowersList += 1
        print('Collecting step ended with status: {0}/{1}/{2}.'.format(
            userIdsWithFollowersList, userIdsWithBasicInfoNum, totalUserIdsNum))
        if cacheLoadingFinishedFlag:
            return 'cache-loading-finished'
        return 'normal-exit'
