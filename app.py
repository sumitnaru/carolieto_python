from flask import Flask, request, render_template, redirect, url_for, flash
from flask_oauthlib.provider import OAuth2Provider
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
oauth = OAuth2Provider(app)

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['oauth2_server']
users = db['users']
clients = db['clients']
tokens = db['tokens']

# Dummy user data for MongoDB (in a production environment, you'd have a registration mechanism)
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

dummy_users = [
    User('user1', 'password1', 'user1@example.com'),
    User('user2', 'password2', 'user2@example.com'),
    User('user3', 'password3', 'user3@example.com'),
]

# Define client ID and secret for account linking
# In a production environment, securely manage these values
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# OAuth2.0 Configuration
@oauth.clientgetter
def load_client(client_id):
    # Retrieve client details from MongoDB or any other storage
    client = clients.find_one({'client_id': client_id})
    return client

@oauth.tokengetter
def load_token(access_token=None):
    # Retrieve token from MongoDB
    token = tokens.find_one({'access_token': access_token})
    return token

@oauth.tokensetter
def save_token(token, request):
    # Save token to MongoDB
    tokens.insert_one(token)

@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    # Retrieve user from MongoDB using username and password
    user = users.find_one({'username': username, 'password': password})
    return user

# Authorization and Access Token Endpoints
@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize():
    if request.method == 'GET':
        # Display authorization form
        return render_template('authorize.html')

    # Handle user's decision (approve or deny)
    if request.form['confirm'] == 'yes':
        return True  # User approved access
    return False

@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None  # OAuth2Provider will handle token creation

# Login endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)
        if user:
            return redirect(url_for('oauth.authorize'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True)
