from flask import Flask, request, redirect
import os
import json
import requests

app = Flask(__name__) 

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = 'https://localhost:5000/callback'
authorization_base_url = 'https://api.pinterest.com/v1/'
token_url = 'https://api.pinterest.com/v1/oauth/token'


@app.route('/')
def homepage():

    return '<form action="/login"> <input type=submit>Get your pinterest boards here! />'


@app.route('/login')
def login():

    authorization_url = 'https://api.pinterest.com/oauth/?response_type=code&redirect_uri={}&client_id={}&scope=read_public&state=123hjkl'.format(REDIRECT_URI, CLIENT_ID)
    return redirect(authorization_url)


@app.route('/callback')
def callback():

    import pdb; pdb.set_trace()

    code = request.args.get('code')

    response = requests.post(token_url, data={'code': code,
                                              'grant_type': 'authorization_code',
                                              'client_id': CLIENT_ID,
                                              'client_secret': CLIENT_SECRET})
    token = response.json()
    access_token = token[access_token]
    data = requests.get('https://api.pinterest.com/v1/me/?access_token={}'.format(access_token))

    return data

if __name__ == "__main__":

    app.run(port=5000, host='0.0.0.0', debug=True)