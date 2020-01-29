from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
import config

app = Flask(__name__)
app.config.from_object(config)
# csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
# login = LoginManager(app)
# login.login_view = 'login'

from route import *
from model import *

# db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
