from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from flask_bootstrap import Bootstrap
import config
import pyrebase
import json
import requests


firebase = pyrebase.initialize_app(config.config)

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)

ASK_LOGIN_TEXT = "You must be logged in to access this page!<br><a href = '/login'></b>click here to log in</b></a>"

storage = firebase.storage()
auth = firebase.auth()
database = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


from file_for_test import img_string

@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    json_msg = request.json
    model_to_use = json_msg["model"]

    if model_to_use != "yolo3":
        return img_string
    else:
        message = {"found": False}
        return jsonify(message)


@app.route('/predict_img_only_api', methods=['GET', 'POST'])
def predict_img_only_api():
    return img_string

@app.route('/predict_upload_api', methods=['GET', 'POST'])
def predict_upload_api():
    json_msg = request.json
    model_to_use = json_msg["model"]

    if model_to_use != "yolo3":
        return img_string
    else:
        message = {"found": False}
        return jsonify(message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' not in session:
        if request.method == "POST":
            user_info = request.form.to_dict()
            email = user_info.get("email")
            password = user_info.get("password")
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                flash('Successful login!')
                session['email'] = email
                session['user_id'] = user['localId']
                return redirect(url_for('home'))
            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']
                flash(error['message'])
        return render_template('login.html')
    return render_template('home.html', username=session.get('email'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user_info = request.form.to_dict()
        email = user_info.get("email")
        password = user_info.get("password")

        if password != user_info.get("password2"):
            flash("Passwords are different")
            return redirect(url_for("register"))

        try:
            auth.create_user_with_email_and_password(email, password)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            flash(error['message'])
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', username=session.get('email'))


@app.route('/camera', methods=['GET', 'POST'])
def camera():
    return render_template('camera.html')


@app.route('/history', methods=['GET', 'POST'])
def history():
    user = database.child('users').child("ylIm4Q0EQCg6IO5WTEqQkWjZEeI3").get()
    histories = user.val()
    if histories is not None:
        return render_template('history.html', histories=histories.values())
    return render_template('history.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html', email="test", count=0)

@app.route('/logout')
def logout():
    flash('Successful log out!')
    return redirect(url_for('login'))
    return ASK_LOGIN_TEXT


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
