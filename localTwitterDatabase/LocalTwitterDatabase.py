import copy


class LocalTwitterDatabase:

    def __init__(self):
        self.users = {}
        self.userIdsList = []

    def addUser(self, user):
        if user.id in self.users:
            return False
        self.users[user.id] = copy.deepcopy(user)
        self.userIdsList.append(user.id)
        return True

    def getUser(self, userId):
        return self.users[userId]

    def getUserAtIndex(self, userIndex):
        return self.users[self.userIdsList[userIndex]]

    def getUsersCount(self):
        return len(self.users)
