import json
from datetime import datetime
from flask import render_template, request, redirect, flash, url_for, session, jsonify
from app import app, firebase
import predict_picture
import numpy as np
import cv2
import random
import string
import requests
from PIL import Image
import cv2
from utils import stringToRGB

# @csrf.exempt

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' in session:
        return render_template('home.html', username=session.get('email'))

    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"


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
            user = firebase.auth().create_user_with_email_and_password(email, password)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            flash(error['message'])
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' not in session:
        if request.method == "POST":
            user_info = request.form.to_dict()
            email = user_info.get("email")
            password = user_info.get("password")
            try:
                user = firebase.auth().sign_in_with_email_and_password(email, password)
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


@app.route('/logout')
def logout():
    if 'email' in session:
        flash('Successful log out!')
        session.pop('email', None)
        session.pop('user_id', None)
        return redirect(url_for('login'))

    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"


def allowed_image(filename):
    ALLOWED_EXTENSIONS = set(['TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'email' in session:
        if request.method == 'POST':
            file = request.files['input1']

            # # read image file string data
            # filestr = file.read()
            # # convert string data to numpy array
            # npimg = np.fromstring(filestr, np.uint8)
            # # convert numpy array to image
            # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            if file and allowed_image(file.filename):
                image = firebase.storage().child('upload/' + session.get('user_id') + '/' + randomString())
                image.put(file)
                image_location = firebase.storage().child('upload/' + session.get('user_id') + '/' + file.filename).get_url(None)
                time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
                # result = predict_picture.predict(img)
                result="happy"
                # if result is None:
                #     pass
                # else:
                #     pass
                #
                firebase.database().child('users/' + session.get('user_id')).push({"image_name": file.filename,
                                                                                     "image_location": image_location,
                                                                                     "submit_time": time,
                                                                                     "result": result})
                flash('Successful upload image!')
                return render_template('upload.html', result=result)
            else:
                flash('Error: upload failed!')
        return render_template('upload.html')
    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if 'email' in session:
        return render_template('camera.html')
    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'email' in session:
        user = firebase.database().child('users').child(session.get('user_id')).get()
        histories = user.val()
        if histories is not None:
            return render_template('history.html', histories=histories.values())
        return render_template('history.html')
    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' in session:
        email = session['email']
        user = firebase.database().child('users').child(session.get('user_id')).get()
        histories = user.val()
        if histories is not None:
            count = len(histories)
        else:
            count = 0
        return render_template('profile.html', email=email, count=count)
    return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/', methods=['GET', 'POST'])
# @app.route('/function', methods=['GET', 'POST'])
def function():
    # if request.method == 'POST':
    #     file = request.files['input2']
    #     # read image file string data
    #     filestr = file.read()
    #     # convert string data to numpy array
    #     npimg = np.fromstring(filestr, np.uint8)
    #     # convert numpy array to image
    #     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    #
    #     if file and allowed_image(file.filename):
    #         result = predict_picture.predict(img)
    #         # result = "happy"
    #         if result is None:
    #             pass
    #         else:
    #             pass
    #
    #         flash('Successful upload image!')
    #
    #         json_result = jsonify(result)
    #
    #         return json_result
    #         # return render_template('index.html', result=result)
    #     else:
    #         flash('Error: upload failed!')
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    img_base64 = request.json["image"]

    rgb_img = stringToRGB(img_base64)

    boxed_image, result = predict_picture.predict(rgb_img)
    if result is None:
        message = {"found": False}
        return jsonify(message)
    else:
        message = {"image": boxed_image, "found": True, "faces": result}
        json_result = jsonify(message)
        return json_result


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     if request.method == "POST":
#         user_info = request.form.to_dict()
#         check_user = User.query.filter_by(username=user_info.get("username")).first()
#         email = User.query.filter_by(email=user_info.get("email")).first()
#         if user_info.get("email") == "":
#             flash("Please enter an email address.")
#             return redirect(url_for("register"))
#         if user_info.get("username") == "":
#             flash("Please enter a username.")
#             return redirect(url_for("register"))
#         if email is not None:
#             flash("Please use a different email address.")
#             return redirect(url_for("register"))
#         if check_user is not None:
#             flash("Please use a different username.")
#             return redirect(url_for("register"))
#         if user_info.get("password") != user_info.get("password2"):
#             flash("Passwords are different")
#             return redirect(url_for("register"))
#         user = User(username=user_info.get("username"), email=user_info.get("email"), password=user_info.get("password"))
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         user_info = request.form.to_dict()
#         user = User.query.filter_by(username=user_info.get("username")).first()
#         if user is not None:
#             if user.valid_login(user_info.get("username"), user_info.get("password")):
#                 flash('Successful login!')
#                 # login_user(user)
#                 session['username'] = request.form.get('username')
#                 return redirect(url_for('home'))
#             else:
#                 flash('Invalid username or password')
#         else:
#             flash('Invalid username')
#     return render_template('login.html')



# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
#     if not os.path.exists(file_dir):
#         os.makedirs(file_dir)
#     if request.method == 'POST':
#         file = request.files['input1']
#
#         # # read image file string data
#         # filestr = file.read()
#         # # convert string data to numpy array
#         # npimg = np.fromstring(filestr, np.uint8)
#         # # convert numpy array to image
#         # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#
#         if file and allowed_image(file.filename):
#             # filename = secure_filename(file.filename)
#             # ext = fname.rsplit('.', 1)[1]
#             # new_filename = Pic_str().create_uuid() + '.' + ext
#             # f.save(os.path.join(file_dir, new_filename))
#
#             file_path = os.path.join(file_dir, file.filename)
#             file.save(file_path)
#             time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
#             user_id = User.query.filter_by(username=session['username']).first().id
#             result = predict_picture.predict(img)
#             # result="happy"
#             if result is None:
#                 pass
#             else:
#                 pass
#
#             image_file = History(image_name=file.filename, image_location=file_path, submit_time=time, result=result, user_id=user_id)
#             db.session.add(image_file)
#             db.session.commit()
#             flash('Successful upload image!')
#             return render_template('upload.html', result=result)
#         else:
#             flash('Error: upload failed!')
#     return render_template('upload.html')

# @app.route('/history', methods=['GET', 'POST'])
# def history():
#     user = User.query.filter_by(username=session['username']).first()
#     user_id = user.id
#     histories = History.query.filter_by(user_id=user_id).all()
#     return render_template('history.html', histories=histories)

# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     user = User.query.filter_by(username=session['username']).first()
#     user_id = user.id
#     count = History.query.filter_by(user_id=user_id).count()
#     return render_template('profile.html', user=user, count=count)

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/function', methods=['GET', 'POST'])
# def function():
#     if request.method == 'POST':
#         file = request.files['input2']
#         # read image file string data
#         filestr = file.read()
#         # convert string data to numpy array
#         npimg = np.fromstring(filestr, np.uint8)
#         # convert numpy array to image
#         img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#
#         if file and allowed_image(file.filename):
#             result = predict_picture.predict(img)
#             # result = "happy"
#             if result is None:
#                 pass
#             else:
#                 pass
#
#             flash('Successful upload image!')
#             return render_template('index.html', result=result)
#         else:
#             flash('Error: upload failed!')
#     return render_template('index.html')

# @app.route('/camera', methods=['GET', 'POST'])
# def camera():
#     return render_template('camera.html')
