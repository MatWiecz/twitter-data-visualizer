import networkx as nx

class FollowersGraphGenerator:

    def __init__(self, database):
        self.database = database
        self.graph = None

    def generateGraph(self):
        self.graph = nx.DiGraph()
        usersCount = self.database.getUsersCount()
        for index in range(usersCount):
            user = self.database.getUserAtIndex(index)
            attributes = {}
            if user.name is not None:
                attributes['name'] = user.name
            if user.followersNum != -1:
                attributes['folNum'] = user.followersNum
            self.graph.add_node(user.id, **attributes)
            for followerId in user.followersList:
                self.graph.add_edge(user.id, followerId)
            print('\rGenerating Followers Graph... ' + str((index * 100) //
                  usersCount) + '%', end='')
        print('\rGenerating Followers Graph... 100% DONE')

    def getGraph(self):
        return self.graph

    def saveGraphToFile(self, fileName):
        nx.write_gexf(self.graph, fileName)
