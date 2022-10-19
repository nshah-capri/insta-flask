from UserBean import *
from instagrapi import Client
import os
import pandas as pd
client = Client()
pathOfCookie = ''


def loginOrCookie(username, password):
    global pathOfCookie
    try:
        pathOfCookie = 'sessions\cookie_'+username+'.json'
        if os.path.exists(pathOfCookie):
            client.load_settings(pathOfCookie)
            client.login(username, password)
            print('Logged in with cookie')
        else:
            client.login(username, password)
            client.dump_settings(pathOfCookie)
            client.set_settings(
                settings={'cookie': pathOfCookie})
            print('Logged in with password')
    except Exception as e:
        print(e)
        return False
    return True


def logout():
    if(pathOfCookie == ''):
        return False
    # delete cookie
    try:
        os.remove(pathOfCookie)
        client.logout()
    except Exception as e:
        print(e)
        return False
    return True


def getProfile(username):
    return client.user_info_by_username(username)


def getFollowers(username, amount, use_cache):
    userid = client.user_id_from_username(username)
    try:
        # dic = client.user_followers(userid, use_cache=use_cache, amount=amount)
        df = pd.DataFrame.from_dict(client.user_followers(userid, use_cache=use_cache, amount=amount), orient='index')
        followersList = []
        # print(df.head(3)) 
        # print(dic)
        
        for i, j in df.iterrows():
            # print(j['username'])
            print(j[1][1])
            followersList.append(j[1][1])
        return followersList
    except Exception as e:
        print(e)
        return False


def getFollowing(username, amount, use_cache):
    userid = client.user_id_from_username(username)
    try:
        df = pd.DataFrame.from_dict(client.user_following(userid, use_cache=use_cache, amount=amount), orient='index')
        followingList = []
        print(df.size)
        for i, j in df.iterrows():
            print(j[1][1])
            followingList.append(j[1][1])
        return followingList
    except Exception as e:
        print(e)
        return False


def getPosts(username):
    return client.user_medias(username)


def getPostInfo(postID):
    return client.media_info(postID)

def dmSingleUser(username, message):
    userid = client.user_id_from_username(username)
    return client.direct_send(text=message,user_ids=[userid])

def dmMultipleUsersAtSameTime(usernames, message):
    userids = []
    for username in usernames:
        print(username)
        userids.append(client.user_id_from_username(username))
    return client.direct_send(text=message,user_ids=userids)

def deleteCookiesFile():
    if(pathOfCookie == ''):
        return False
    # delete cookie
    try:
        os.remove(pathOfCookie)
    except Exception as e:
        print(e)
        return False
    return True