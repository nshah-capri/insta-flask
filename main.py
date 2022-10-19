from flask import Flask, request, Request, Response, jsonify, redirect, url_for, render_template
from instagrapi import Client
from functions import *
# Create the app
app = Flask(__name__)
client = Client()
@app.route('/login', methods=['POST', 'GET'])
def login() -> str:
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
def logoutFunc() -> str:
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
        userList = []
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
        if not followUser(username):
            return {'message': 'User followed or if private, request sent'}
        else:
            return {'message': 'User is already followed or error'}
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


if __name__ == '__main__':
    print("Starting Python Flask Server For Prime Sieve...")
    app.run(debug=True, port=5000)
