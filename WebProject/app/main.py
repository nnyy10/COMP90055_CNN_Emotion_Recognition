# -*- coding: utf-8 -*-
"""
Main flask application with all the routes.
"""

from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from flask_bootstrap import Bootstrap
import config
import pyrebase
import json
from datetime import datetime
import predict_picture
import requests
import utils
from yolo import yolo


firebase = pyrebase.initialize_app(config.config)
storage = firebase.storage()
auth = firebase.auth()
database = firebase.database()

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)


""" HTML to be shown to the unregistered user if they try to access a page only accessible for signed in users """
ASK_LOGIN_TEXT = "You must be logged in to access this page!<br><a href = '/login'></b>click here to log in</b></a>"

"""Error messages to be sent if the user passes in invalid json or error on image processing possibly due to bad data"""
JSON_ERROR_INVALID_JSON = {"error": "failed to parse json, invalid format"}
JSON_ERROR_PREDICTION_FAILED = {"error": "failed to process image, try another image"}


@app.route('/', methods=['GET', 'POST'])
def index():
    """ home page """
    if 'email' in session:
        return render_template('home.html', username=session.get('email'))
    return render_template('index.html')


@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    """
    API which detect all faces in an image and makes a prediction of the emotion for each face.
    predict_api accepts JSON as input. Input must contain:
        image: Base64 encoded image
        model: Must be one of the following: yolo3, mobilenetv2, incpetion-resnet. Defaults to inception-resnet if the
               model is not valid.
    The API returns a JSON in the format of:
        {
        image: "Base64 encoded image with bounding boxes (present only if found is true)"
        found: "Boolean value of whether a face(s) are found in the image."
        faces: "List of {
                            face: "Bse64 encoded cropped face image",
                            prediction: "list of {
                                                  emotion: "the emotion with the highest probability
                                                  probability: "the probability"
                                                 }"
                         }"(present only if found is true)
        }
    """

    try:
        json_msg = request.json
        img_base64 = json_msg["image"]
        model_to_use = json_msg["model"]
    except:
        return jsonify(JSON_ERROR_INVALID_JSON)

    try:
        if model_to_use != "yolo3":
            rgb_img = utils.base64_to_rgb(img_base64)
            message = predict_picture.predict(rgb_img, model_to_use=model_to_use)
            return jsonify(message)
        else:
            pil_img = utils.base64_to_pil(img_base64)
            message = yolo.yolo_model.detect_image(pil_img)
            return jsonify(message)
    except:
        return jsonify(JSON_ERROR_PREDICTION_FAILED)


@app.route('/predict_upload_api', methods=['GET', 'POST'])
def predict_upload_api():
    """
    API which detect all faces in an image and makes a prediction of the emotion for each face and uploads the result
    to the user's firebase database if the user is logged in. Functions like normal predict_api if the user is not
    signed in.
    However, uploading for yolo3 model is not yet implemented.
    predict_upload_api accepts JSON as input. Input must contain:
        image: Base64 encoded image
        model: Must be one of the following: yolo3, mobilenetv2, incpetion-resnet. Defaults to inception-resnet if the
               model is not valid.
        img_name: The name of the image to be uploaded to firebase databse.
    The API returns a JSON in the format of:
        {
        image: "Base64 encoded image with bounding boxes (present only if found is true)"
        found: "Boolean value of whether a face(s) are found in the image."
        faces: "List of {
                            face: "Bse64 encoded cropped face image",
                            prediction: "list of {
                                                  emotion: "the emotion with the highest probability
                                                  probability: "the probability"
                                                 }"
                         }"(present only if found is true)
        }
    """

    try:
        json_msg = request.json
        img_base64 = json_msg["image"]
        img_name = json_msg["img_name"]
        model_to_use = json_msg["model"]
    except:
        return jsonify(JSON_ERROR_INVALID_JSON)

    try:
        if model_to_use != "yolo3":
            rgb_img = utils.base64_to_rgb(img_base64)
            message, face_predictions, boxed_img_buff, cropped_face_buff = predict_picture.predict_upload(rgb_img, model_to_use=model_to_use)
            if message["found"] is False:
                return jsonify(message)
            else:
                if 'email' in session:
                    """the following code uploades the result to the database"""
                    time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

                    entry_name = database.child('users/' + session.get('user_id')).push({"image_name": img_name,
                                                                                         "submit_time": time,
                                                                                         "result": face_predictions})["name"]

                    image = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + entry_name + '.jpg')
                    image.put(boxed_img_buff)
                    img_location = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + entry_name + '.jpg').get_url(None)
                    database.child('users').child(session.get('user_id')).child(entry_name).update({"image_location": img_location})
                    for i, face in enumerate(cropped_face_buff):
                        image = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + str(i) + '.jpg')
                        image.put(face)
                        img_location = storage.child('upload/' + session.get('user_id') + '/' + entry_name + '/' + str(i) + '.jpg').get_url(None)
                        database.child('users').child(session.get('user_id')).child(entry_name).child("result").child(str(i)).update(
                            {"image_location": img_location})

                json_result = jsonify(message)
                return json_result
        else:
            """uploading to database for yolo3 model is not yet implemented."""
            pil_img = utils.base64_to_pil(img_base64)
            message = yolo.yolo_model.detect_image(pil_img)
            return jsonify(message)
    except:
        return jsonify(JSON_ERROR_PREDICTION_FAILED)


@app.route('/predict_img_only_api', methods=['GET', 'POST'])
def predict_img_only_api():
    """
    API which detect all faces in an image and makes a prediction of the emotion for each face.
    Unlike the previous 2 functions, it only return a single large image and no individual faces that are cropped are
    sent back. This is used by our real time emotion detection web page to cut down computation.
    This api uses inception-reset as default since it is the model with the best accuracy.

    predict_img_only_api accepts JSON as input. Input must contain:
        image: Base64 encoded image
    The API returns a JSON in the format of:
        {
        image: "Base64 encoded image with bounding boxes (present only if found is true)"
        found: "Boolean value of whether a face(s) are found in the image."
    """

    try:
        img_base64 = request.json["image"]
    except:
        return jsonify(JSON_ERROR_INVALID_JSON)

    try:
        rgb_img = utils.base64_to_rgb(img_base64)
        message = predict_picture.predict_img_only(rgb_img)
        return message
    except:
        return jsonify(JSON_ERROR_PREDICTION_FAILED)


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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'email' in session:
        return render_template('upload.html', username=session.get('email'))
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
