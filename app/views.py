import datetime
import json
import os
import requests
from flask import render_template, redirect, request, Flask
from wtforms import Form, StringField, PasswordField, validators
from app import app
from Cryptodome.PublicKey import RSA
from json import dumps
from flask_mysqldb import MySQL


# app = Flask(__name__)
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

#SQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

#Home Page
@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='Private Blockchain '
                                 'content sharing',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
    
#login Page
@app.route('/user', methods=['GET'])
def user():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def move_forward():
    return render_template('index.html',
                           title='Private Blockchain '
                                 'content sharing',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
        
#Register User
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(
    ), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.form == 'POST' and form.validate():
        return render_template('regis.html')
    return render_template('regis.html', form=form)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]
    k = RSA.generate(1025)
    puk = k.publickey().export_key().decode()
    prk = k.export_key().decode()
    cur = mysql.connection.cursor()
    post_object = {
        'author': author,
        'content': post_content,
        'public_key' : puk,
        'private_key' : prk,
    }
    cur.execute("INSERT INTO Block(author, content, publickey, privatekey) VALUES (%s, %s, %s, %s)", (author, content, public_key, private_key))
    mysql.connection.commit()
    cur.close()
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

#Database Table Schema for each transaction(Post) added.
# CREATE TABLE Block ( author VARCHAR(30) NOT NULL, content VARCHAR(100) NOT NULL, publickey VARCHAR(1025) NOT NULL, privatekey VARCHAR(1025) NOT NULL);