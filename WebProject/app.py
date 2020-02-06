import app as app
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
import config
import pyrebase

firebase = pyrebase.initialize_app(config.config)

app = Flask(__name__)
app.config.from_object(config)
# csrf = CSRFProtect(app)
# db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


from route import *
from model import *


if __name__ == '__main__':
    app.run(debug=True)
