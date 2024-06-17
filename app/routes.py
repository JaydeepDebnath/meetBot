from flask import jsonify, request, render_template,session, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from app import app
from app.models import User,Bot
import secrets
import datetime 
import bcrypt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

# Create routes

app.secret_key = secrets.token_urlsafe(100)
login_manager = LoginManager()
login_manager.init_app(app)

# Generete session token
def generate_refresh_token():
    return secrets.token_urlsafe(100)

# Generate refresh token
def generate_refresh_token():
    return secrets.token_urlsafe(100)

def  validate_session_token(session_token):
    if 'session_expire' in session and session['session_expire'] > datetime.datetime.now():
        return True
    else:
        return False


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)

@app.route('/register',methods=['POST'])
def user_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    contactNumber = request.form.get('contactNumber')

    existedUser = User.objects('username')
    existedEmail = User.objects('email')
    if existedUser or existedEmail:
        return jsonify({'error': 'Username or email already exists'}), 404
    
    # Bcrypt password

    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    

    newUser = User(username=username, email=email,password=hashed_password, contactNumber=contactNumber)
    newUser.save()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login',methods=['POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.objects(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'message': 'Login successful'}),201
    else:
        return jsonify({'error': 'Invalid username or password'}),404
    

@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    return redirect(url_for('index'))

@app.route('/join_meeting',methods=['POST'])
@login_required
def join_meeting():
    bot_id = Bot.form.get('bot_id')
    meeting_link = Bot.form.get('meeting_link')

    # Validate the link
    if not is_valid_meeting_link(meeting_link):
        return jsonify({'error': 'Invalid meeting link'}), 400

    # Retrive bot data
    bot = Bot.objects.get(id=bot_id)

    # retrive auth user from session
    user_id = session.get('user_id')

    if user_id:
        user = load_user(user_id)
    else:
        return jsonify({'error':'User not authenticated'}),401
    
    # check user auth or not

    if user != bot.owner:
        return jsonify({'error': 'Unauthorized access'}), 403

    driver = webdriver.Chrome()

    try:
        driver.get('https://meet.google.com/')
        time.sleep(7)

        # Metting code
        code_input = driver.find_element_by_xpath("//input[@id='i3']")
        code_input.send_keys(meeting_link)
        code_input.send_keys(Keys.RETURN)
        time.sleep(7)

        # Join meeting
        join_button = driver.find_element_by_xpath("//span[text()='Join now']")
        join_button.click()
        
        return jsonify({'message': 'Bot joined the meeting successfully'}), 200

    except Exception as e:
        return jsonify({'error':str(e)})
    finally:
        driver.quit()



def is_valid_meeting_link(link):
    pattern = r'https://meet\.google\.com/[a-z0-9-]+'
    return re.match(pattern, link) is not None




    
    

