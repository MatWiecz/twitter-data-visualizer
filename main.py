import twitter
from twitterApiWrapper.twitterApiWrapper import TwitterApiWrapper


def main():
    twitterApi = TwitterApiWrapper('twitterAPIAuthFile.json',
                                   'twitterResponsesCache')
    followerIDs = twitterApi.getFollowersListForUser(screenName='AGH_Krakow')

    print(followerIDs)
    # listLen = len(followerIDs)
    # for index in range(listLen):
    #     print('[{0}/{1}] {2}'.format(index, listLen, followerIDs[index]))

    print(twitterApi.getUserFromUserId(screenName='AGH_Krakow'))


if __name__ == "__main__":
    main()
