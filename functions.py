from UserBean import *
from instagrapi import Client
import os
import pandas as pd
import gc
client = Client()
pathOfCookie = ''
import db as db

def loginOrCookie(username, password) -> str:
    global pathOfCookie
    try:
        pathOfCookie = 'sessions\cookie_'+username+'.json'
        if os.path.exists(pathOfCookie):
            client.load_settings(pathOfCookie)
            if client.login(username, password):
                try:
                    client.user_id_from_username(username)
                    print('Logged in with cookie')
                    return {'message': 'Logged in with cookie', 'status': 200, 'sessionid': client.sessionid}
                except Exception as e:
                    try:
                        client.relogin()
                        client.dump_settings(pathOfCookie)
                        client.set_settings(settings={'use_cache': True, 'cookie' : pathOfCookie})
                        print('Logged in with cookie....')

                        return {'message': 'Logged in with cookie', 'status': 200, 'sessionid': client.sessionid}
                    except Exception as e:
                        print(e)
                        return False
        else:
            client.login(username, password)
            client.dump_settings(pathOfCookie)
            client.set_settings(
                settings={'cookie': pathOfCookie})
            print('Logged in with password')
            return {'message': 'Logged in with password', 'status': 200, 'sessionid': client.sessionid}
    except Exception as e:
        print(e)
        return False
    return False


def logout() -> str:
    if(pathOfCookie == ''):
        return False
    # delete cookie
    try:
        os.remove(pathOfCookie)
        gc.collect()
        client.logout()
        return {'message': 'Logged out', 'status': 200}
    except Exception as e:
        print(e)
        return {'message' : 'Error while logging out', 'status': 500}
    return {'message' : 'Error while logging out', 'status': 500}

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
        try:
            dmSingleUser(username, message)
        except Exception as e:
            print(e)
            return False
    return True
    

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

def followUser(username):
    useridofuser = client.user_id_from_username(username)
    print(useridofuser)
    return client.user_follow(useridofuser)

def unfollowUser(username):
    userid = client.user_id_from_username(username)
    return client.user_unfollow(userid)

def storeFollowersInDatabase(username, amount) -> str:
    userid = client.user_id_from_username(username)
    followers = client.user_followers(userid, use_cache=True, amount=amount)
    result =  db.insertFollowers(client, username, followers)
    return result