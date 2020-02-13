import base64
import io
import os
from PIL import Image
from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from flask_bootstrap import Bootstrap
import config
import pyrebase
import json
from datetime import datetime
import predict_picture
import requests
from utils import stringToRGB, RGB_to_PIL_img, PIL_img_to_RGB, rgbToString
import time
from yolo import yolo


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
    if 'email' in session:
        return render_template('home.html', username=session.get('email'))
    return render_template('index.html')


@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    json_msg = request.json
    img_base64 = json_msg["image"]
    model_to_use = json_msg["model"]

    if model_to_use != "yolo3":
        rgb_img = stringToRGB(img_base64)
        boxed_image, result = predict_picture.predict(rgb_img)
        if result is None:
            message = {"found": False}
            return jsonify(message)
        else:
            message = {"image": boxed_image[0], "found": True, "faces": result}
            json_result = jsonify(message)
            return json_result
    else:
        rgb_img = stringToRGB(img_base64)
        PIL_img = RGB_to_PIL_img(rgb_img)
        output_PIL, num_faces = yolo.yolo_model.detect_image(PIL_img)
        if num_faces == 0:
            message = {"found": False}
            return jsonify(message)
        else:
            output_rgb = PIL_img_to_RGB(output_PIL)
            boxed_image = rgbToString(output_rgb)
            message = {"image": boxed_image[0], "found": True}
            json_result = jsonify(message)
            return json_result


@app.route('/predict_img_only_api', methods=['GET', 'POST'])
def predict_img_only_api():
    img_base64 = request.json["image"]

    rgb_img = stringToRGB(img_base64)
    boxed_image = predict_picture.predict(rgb_img, img_only=True)
    if boxed_image is None:
        message = {"found": False}
        return jsonify(message)
    else:
        message = {"image": boxed_image, "found": True}
        json_result = jsonify(message)
        return json_result


@app.route('/predict_upload_api', methods=['GET', 'POST'])
def predict_upload_api():
    json_msg = request.json
    img_base64 = json_msg["image"]
    img_name = json_msg["img_name"]
    model_to_use = json_msg["model"]

    if model_to_use != "yolo3":
        rgb_img = stringToRGB(img_base64)
        boxed_image, result, face_predictions, cropped_face_buff = predict_picture.predict_upload(rgb_img)
        if result is None:
            message = {"found": False}
            return jsonify(message)
        else:
            if 'email' in session:
                time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

                entry_name = database.child('users/' + session.get('user_id')).push({"image_name": img_name,
                                                                                     "submit_time": time,
                                                                                     "result": face_predictions})["name"]

                image = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + entry_name + '.jpg')
                image.put(boxed_image[1])
                img_location = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + entry_name + '.jpg').get_url(None)
                database.child('users').child(session.get('user_id')).child(entry_name).update({"image_location": img_location})
                for i, face in enumerate(cropped_face_buff):
                    image = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + str(i) + '.jpg')
                    image.put(face)
                    img_location = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + str(i) + '.jpg').get_url(None)
                    database.child('users').child(session.get('user_id')).child(entry_name).child("result").child(str(i)).update(
                        {"image_location": img_location})

            message = {"image": boxed_image[0], "found": True, "faces": result}
            json_result = jsonify(message)
            return json_result
    else:
        rgb_img = stringToRGB(img_base64)
        PIL_img = RGB_to_PIL_img(rgb_img)
        output_PIL, num_faces = yolo.yolo_model.detect_image(PIL_img)
        if num_faces == 0:
            message = {"found": False}
            return jsonify(message)
        else:
            output_rgb = PIL_img_to_RGB(output_PIL)
            boxed_image = rgbToString(output_rgb)
            message = {"image": boxed_image[0], "found": True}
            json_result = jsonify(message)
            return json_result


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
    if 'email' in session:
        return render_template('home.html', username=session.get('email'))
    return ASK_LOGIN_TEXT


@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if 'email' in session:
        return render_template('camera.html')
    return ASK_LOGIN_TEXT


@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'email' in session:
        user = database.child('users').child(session.get('user_id')).get()
        histories = user.val()
        if histories is not None:
            return render_template('history.html', histories=histories.values())
        return render_template('history.html')
    return ASK_LOGIN_TEXT


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' in session:
        email = session['email']
        user = database.child('users').child(session.get('user_id')).get()
        histories = user.val()
        if histories is not None:
            count = len(histories)
        else:
            count = 0
        return render_template('profile.html', email=email, count=count)
    return ASK_LOGIN_TEXT


@app.route('/logout')
def logout():
    if 'email' in session:
        flash('Successful log out!')
        session.pop('email', None)
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return ASK_LOGIN_TEXT


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'email' in session:
#         # if request.method == 'POST':
#         #     file = request.files['input1']
#         #
#         #     # # read image file string data
#         #     # filestr = file.read()
#         #     # # convert string data to numpy array
#         #     # npimg = np.fromstring(filestr, np.uint8)
#         #     # # convert numpy array to image
#         #     # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#         #
#         #     if file and allowed_image(file.filename):
#         #         image = storage.child('upload/' + session.get('user_id') + '/' + randomString())
#         #         image.put(file)
#         #         image_location = storage.child('upload/' + session.get('user_id') + '/' + file.filename).get_url(None)
#         #         time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
#         #         # result = predict_picture.predict(img)
#         #         result="happy"
#         #         # if result is None:
#         #         #     pass
#         #         # else:
#         #         #     pass
#         #         #
#         #         database.child('users/' + session.get('user_id')).push({"image_name": file.filename,
#         #                                                                              "image_location": image_location,
#         #                                                                              "submit_time": time,
#         #                                                                              "result": result})
#         #         flash('Successful upload image!')
#         #         return render_template('upload.html', result=result)
#         #     else:
#         #         flash('Error: upload failed!')
#         return render_template('upload.html')
#     return "You must be logged in to access this page!<br><a href = '/login'></b>" + "click here to log in</b></a>"



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
