import os
from flask import Flask


#Configs
app = Flask(__name__)

app.config['SECRET_KEY']='d45eec911428443e6d6c6c7d45eec911428443e6d6c6c7'
app.config['SESSION_COKKIE_NAME']='google-login-session'
from WI import routes


