from datetime import datetime

from flask import render_template, request, redirect, flash, url_for, session, Response
from flask_login import login_user

from app import db, app
from form import RegistrationForm, LoginForm
from model import User, History
import os
import predict_picture
import numpy as np
import cv2

# @csrf.exempt
from utils import load_model


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', username=session.get('username'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user_info = request.form.to_dict()
        check_user = User.query.filter_by(username=user_info.get("username")).first()
        email = User.query.filter_by(email=user_info.get("email")).first()
        if user_info.get("email") == "":
            flash("Please enter an email address.")
            return redirect(url_for("register"))
        if user_info.get("username") == "":
            flash("Please enter a username.")
            return redirect(url_for("register"))
        if email is not None:
            flash("Please use a different email address.")
            return redirect(url_for("register"))
        if check_user is not None:
            flash("Please use a different username.")
            return redirect(url_for("register"))
        if user_info.get("password") != user_info.get("password2"):
            flash("Passwords are different")
            return redirect(url_for("register"))
        user = User(username=user_info.get("username"), email=user_info.get("email"), password=user_info.get("password"))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html')

# @app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_info = request.form.to_dict()
        user = User.query.filter_by(username=user_info.get("username")).first()
        if user is not None:
            if user.valid_login(user_info.get("username"), user_info.get("password")):
                flash('Successful login!')
                # login_user(user)
                session['username'] = request.form.get('username')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
        else:
            flash('Invalid username')
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash('Successful log out!')
    session.pop('username', None)
    return redirect(url_for('login'))

def allowed_image(filename):
    ALLOWED_EXTENSIONS = set(['TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if request.method == 'POST':
        file = request.files['input1']

        # read image file string data
        filestr = file.read()
        # convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if file and allowed_image(file.filename):
            # filename = secure_filename(file.filename)
            # ext = fname.rsplit('.', 1)[1]
            # new_filename = Pic_str().create_uuid() + '.' + ext
            # f.save(os.path.join(file_dir, new_filename))

            file_path = os.path.join(file_dir, file.filename)
            file.save(file_path)
            time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            user_id = User.query.filter_by(username=session['username']).first().id
            result = predict_picture.predict(img)
            # result="happy"
            if result is None:
                pass
            else:
                pass

            image_file = History(image_name=file.filename, image_location=file_path, submit_time=time, result=result, user_id=user_id)
            db.session.add(image_file)
            db.session.commit()
            flash('Successful upload image!')
            return render_template('upload.html', result=result)
        else:
            flash('Error: upload failed!')
    return render_template('upload.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
    user = User.query.filter_by(username=session['username']).first()
    user_id = user.id
    histories = History.query.filter_by(user_id=user_id).all()
    return render_template('history.html', histories=histories)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.query.filter_by(username=session['username']).first()
    user_id = user.id
    count = History.query.filter_by(user_id=user_id).count()
    return render_template('profile.html', user=user, count=count)

@app.route('/', methods=['GET', 'POST'])
@app.route('/function', methods=['GET', 'POST'])
def function():
    if request.method == 'POST':
        file = request.files['input2']
        # read image file string data
        filestr = file.read()
        # convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if file and allowed_image(file.filename):
            result = predict_picture.predict(img)
            # result = "happy"
            if result is None:
                pass
            else:
                pass

            flash('Successful upload image!')
            return render_template('function.html', result=result)
        else:
            flash('Error: upload failed!')
    return render_template('function.html')




@app.route('/camera', methods=['GET', 'POST'])
def camera():
    return render_template('camera.html')
