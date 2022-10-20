# create function to connect to mysql database
import mysql.connector
from instagrapi import Client

client = Client()


def connect():
    mydb = mysql.connector.connect(
        host="localhost",
        port="3309",
        user="root",
        password="",
        database="instagramlocal"
    )
    return mydb


def insertFollowers(client, username, followers) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    count = 0
    for follower in followers:
        sql = "INSERT INTO followerslist (client, username, usernametofollow) VALUES (%s, %s, %s)"
        val = (client.username, username, follower)
        mycursor.execute(sql, val)
        mydb.commit()
        count += 1
    print(count, "record inserted.")
    return {'message': 'Followers inserted', 'status': 200, 'count': count}


def insertFollowing(client, username, following) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    count = 0
    for follow in following:
        sql = "INSERT INTO followinglist (client, username, usernametofollow) VALUES (%s, %s, %s)"
        val = (client.username, username, follow)
        mycursor.execute(sql, val)
        mydb.commit()
        count += 1
    print(count, "record inserted.")
    return {'message': 'Following inserted', 'status': 200, 'count': count}


def insertMessageToDB(client, message) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "INSERT INTO messages (username, message) VALUES (%s, %s)"
    val = (client.username, message)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return {'message': 'Message inserted', 'status': 200}


def getMessagesFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "SELECT * FROM messages WHERE username = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return {'message': 'Messages fetched', 'status': 200, 'messages': myresult}


def deleteMessagesFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "DELETE FROM messages WHERE username = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    return {'message': 'Messages deleted', 'status': 200}


def getFollowersListFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "SELECT * FROM followerslist WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return {'message': 'Followers fetched', 'status': 200, 'followers': myresult}


def getFollowingListFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "SELECT * FROM followinglist WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return {'message': 'Following fetched', 'status': 200, 'following': myresult}


def deleteFollowersListFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "DELETE FROM followerslist WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    return {'message': 'Followers deleted', 'status': 200}


def deleteFollowingListFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "DELETE FROM followinglist WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    return {'message': 'Following deleted', 'status': 200}


def usersToDMFromDM(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "SELECT * FROM users WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return {'message': 'Users fetched', 'status': 200, 'users': myresult}


def usersToFollowAndDMFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "SELECT * FROM users WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return {'message': 'Users fetched', 'status': 200, 'users': myresult}


def insertUsersToFollowAndDMToDB(client, users) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    count = 0
    for user in users:
        sql = "INSERT INTO users (client, username) VALUES (%s, %s)"
        val = (client.username, user)
        mycursor.execute(sql, val)
        mydb.commit()
        count += 1
    print(count, "record inserted.")
    return {'message': 'Users inserted', 'status': 200, 'count': count}


def deleteUsersToFollowAndDMFromDB(client) -> str:
    mydb = connect()
    mycursor = mydb.cursor()
    # here username in the query is the username of the client
    sql = "DELETE FROM users WHERE client = %s"
    val = (client.username,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    return {'message': 'Users deleted', 'status': 200}
