from time import sleep

import twitter

from localTwitterDatabase.LocalTwitterDatabase import LocalTwitterDatabase
from localTwitterDatabase.TwitterUser import TwitterUser
from twitterApiWrapper.twitterApiWrapper import TwitterApiWrapper
from methodCallCache.MethodCallCache import MethodCallCache
from twitterDataCollector.TwitterDataCollector import TwitterDataCollector
from graphGenerator.FollowersGraphGenerator import FollowersGraphGenerator


def main():
    cache = MethodCallCache("cache.json")
    twitterApi = TwitterApiWrapper('twitterAPIAuthFile.json', cache)
    TwitterUser.setTwitterApi(twitterApi)
    database = LocalTwitterDatabase()
    collectorConfig = {
        'followersNumThreshold': 500,
        'maxNewGetUserObjectOperationsNum': 60
    }
    collector = TwitterDataCollector(database, collectorConfig, cache)
    collector.startCollecting('szymon_holownia')
    followersGraphGenerator = FollowersGraphGenerator(database)
    for i in range(1000000):
        if collector.continueCollecting() == 'cache-loading-finished':
            followersGraphGenerator.generateGraph()
            followersGraphGenerator.saveGraphToFile('followersGraph.gexf')
        sleep(1)



if __name__ == "__main__":
    main()
