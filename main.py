import twitter
from twitterApiWrapper.twitterApiWrapper import TwitterApiWrapper
from methodCallCache.MethodCallCache import MethodCallCache

# class SomeClass:
#
#     def __init__(self):
#         pass
#
#     def div(self, a, b):
#         return a / b

def main():
    cache = MethodCallCache("cache.json")
    # s = SomeClass()
    # result = cache.execute(s, 'div', a=4, b=6)
    # print(result)
    # result = cache.execute(s, 'div', a=6, b=4)
    # print(result)
    # result = cache.execute(s, 'div', a=4, b=6)
    # print(result)
    twitterApi = TwitterApiWrapper('twitterAPIAuthFile.json', cache)
    followerIDs = twitterApi.getFollowersListForUser(screenName='AGH_Krakow')

    print(followerIDs)
    listLen = len(followerIDs)
    for index in range(listLen):
        print('[{0}/{1}] {2}'.format(index, listLen, followerIDs[index]))

    print(twitterApi.getUserFromUserId(screenName='AGH_Krakow'))



if __name__ == "__main__":
    main()
