from flask import Flask, request, Request, Response, jsonify, redirect, url_for, render_template
from functions import *

# Create the app
app = Flask(__name__)
client = Client()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # if loginOrCookie(username, password):
        # return redirect(url_for('home'))
        try:
            return loginOrCookie(username, password)
        except Exception as e:
            return e
    else:
        return {'message': 'Login page'}


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if loginOrCookie(username, password):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return {'message': 'Hello, World!'}


@app.route('/logout', methods=['GET'])
def logoutFunc():
    return logout()


@app.route('/followers', methods=['POST', 'GET'])
def followers():
    if request.method == 'POST':
        username = request.form.get('username')
        # take amount of followers and if it is not specified, take 0
        # make amount into int
        amount = int(request.form.get('amount', 0))
        # take use_cache and if it is not specified, take False\
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        followersList = getFollowers(username, amount, use_cache)
        if followersList:
            return {'followers': followersList}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Followers page'}


@app.route('/following', methods=['POST', 'GET'])
def following():
    if request.method == 'POST':
        username = request.form.get('username')
        # take amount of followers and if it is not specified, take 0
        # make amount into int
        amount = int(request.form.get('amount', 0))
        # take use_cache and if it is not specified, take False\
        use_cache = request.form.get('use_cache', False)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        followingList = getFollowing(username, amount, use_cache)
        if followingList:
            return {'following': followingList}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Following page'}


@app.route('/dm', methods=['POST', 'GET'])
def dmSingle():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')
        if dmSingleUser(username, message):
            return {'message': 'Message sent'}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'DM page'}


@app.route('/dmmultiple', methods=['POST', 'GET'])
def dmMultiple():
    if request.method == 'POST':
        usernames = request.form.get('usernames')
        message = request.form.get('message')
        userList = usernames.split(',')
        if dmMultipleUsersAtSameTime(userList, message):
            return {'message': 'Message sent'}
        else:
            return {'message': 'Error'}
        # return {'usernames': usernames, 'message': message}
    else:
        return {'message': 'DM page'}


@app.route('/deletecookies', methods=['GET'])
def deleteCookies():
    if deleteCookiesFile():
        return {'message': 'Cookies deleted'}
    else:
        return {'message': 'Error'}


@app.route("/follow", methods=['POST', 'GET'])
def follow():
    if request.method == 'POST':
        username = request.form.get('username')
        followstatus = followUser(username)
        if followstatus == "Already followed":
            return {'message': 'User Already followed'}

        elif followstatus == "Follow request has been sent":
            return {'message': 'Request sent'}

        elif followstatus == "Followed the user":
            return {'message': 'Followed the user'}

        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Follow page'}


@app.route("/unfollow", methods=['POST', 'GET'])
def unfollow():
    if request.method == 'POST':
        username = request.form.get('username')
        if unfollowUser(username):
            return {'message': 'User unfollowed'}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Unfollow page'}


@app.route(rule='/storefollowers', methods=['POST', 'GET'])
def storeFollowers():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        result = storeFollowersInDatabase(username, amount)
        if result:
            return result
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Store followers page'}

@app.route(rule='/storefollowing', methods=['POST', 'GET'])
def storeFollowing():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        result = storeFollowingInDatabase(username, amount)
        if result:
            return result
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Store following page'}

@app.route(rule='/storemessages', methods=['POST', 'GET'])
def storeMessages():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        result = storeMessagesInDatabase(username, amount)
        if result:
            return result
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Store messages page'}

@app.route('/getmessages', methods=['POST', 'GET'])
def getMessages():
    if request.method == 'POST':
        username = request.form.get('username')
        amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        messages = getMessagesFromDatabase(username, amount)
        if messages:
            return {'messages': messages}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Get messages page'}

@app.route('/getfollowers', methods=['POST', 'GET'])
def getFollowers():
    if request.method == 'POST':
        username = request.form.get('username')
        # amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        followers = getFollowersFromDatabase(username)
        if followers:
            return {'followers': followers}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Get followers page'}

@app.route('/getfollowing', methods=['POST', 'GET'])
def getFollowing():
    if request.method == 'POST':
        username = request.form.get('username')
        # amount = int(request.form.get('amount', 100))
        use_cache = request.form.get('use_cache', True)
        if use_cache == 'True':
            use_cache = True
        else:
            use_cache = False
        following = getFollowingFromDatabase(username)
        if following:
            return {'following': following}
        else:
            return {'message': 'Error'}
    else:
        return {'message': 'Get following page'}


if __name__ == '__main__':
    print("Starting Python Flask Server For Prime Sieve...")
    app.run(debug=True, port=6000)
