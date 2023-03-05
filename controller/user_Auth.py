from flask import Blueprint, jsonify,request, send_file
from werkzeug.security import check_password_hash, generate_password_hash
import controller.emailOtp as eOTP
import re
from datetime import datetime
import os
#-----------------------------------------------------------------------------------------------
#  USER AUTHENTICATION AND MANAGEMENT
#  STARTING FROM HERE
#-----------------------------------------------------------------------------------------------
userAuth_api = Blueprint('userAuth_api', __name__)
     
@userAuth_api.route("/")
def hello():
    return "Hello World"

@userAuth_api.route('/users/<uid>/upload/image', methods =['PUT'])
def userAddImage(uid):
    from app import mysql
    d = {}     
    if request.method == 'PUT':
                 
        file = request.files['profile_image']
        
        new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
        split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
        ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
        ext = split_filename[ext_pos] # Using last index to get the file extension
        db_path = f"storage/users_profile_photo/{new_filename}.{ext}"
        file.save(f"storage/users_profile_photo/{new_filename}.{ext}")
        
        cursor = mysql.cursor()
        cursor.execute("UPDATE user_info SET image_path = %s WHERE id= %s ",(db_path,uid))
        mysql.commit()
        
        d["message"] = "File uploaded successfully"
        d["path"] = db_path
        
        return jsonify(d)
        
    else:
        return 'Method not allowed'
    
@userAuth_api.route("/users/<uid>/get/image")
def getUserProfileImage(uid):
    
    from app import mysql, app
    
    #if request.method == 'GET':
        
    cursor = mysql.cursor()
    cursor.execute("SELECT image_path FROM user_info WHERE id = %s",[uid])
    path = cursor.fetchone()
    root_dir = os.path.dirname(app.instance_path)            
    return send_file(root_dir+'/'+ path["image_path"])
    # else:
    #     return 'Method not allowed'

@userAuth_api.route("/login_user", methods=['POST'])
def login():
    from app import mysql
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        
        cursor = mysql.cursor()
        cursor.execute('SELECT password_hash, email FROM user_info WHERE email = %s limit 0,1', [email])
        login = cursor.fetchone()
        
        if login:          
            if check_password_hash(login[0], password): 
                cursor.execute('SELECT id, username, bio, headline, image_path FROM user_info WHERE email = %s', [email])
                account = cursor.fetchone()
                
                # Create unique IDs for the user's posts and updates
                uniqueIDposts = str(account[0]) + "posts"
                uniqueIDUpdates = str(account[0]) + 'updates'
                
                # Create a dictionary with the user's account information
                d = {
                    "id": account[0],
                    "username": account[1],
                    "bio": account[2],
                    "headline": account[3],
                    "image_path": account[4],
                    "projects": uniqueIDposts,
                    "updates": uniqueIDUpdates
                }
                
                # Return the account information as a JSON response
                return jsonify(d)
            else:
                return "Error password"
        else:
            # account not exist
            d = {"status": 0}
            return jsonify(d)

            
@userAuth_api.route('/sendOtp')
def emailOtp():
    email_id = request.json['email']
    
    otp = eOTP.send_email(email_id)
    
    return jsonify(otp)
    

@userAuth_api.route('/register_user', methods=['GET', 'POST'])
def register():
    d = {}
    from app import mysql
    if request.method == 'POST':
        
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        headline = request.json['headline']
        
        cursor = mysql.cursor()
        cursor.execute('SELECT * FROM user_info WHERE email = %s', [email])
        account = cursor.fetchone()
        
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            password_hash = generate_password_hash(password)
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('''INSERT INTO user_info(username,email,password_hash,bio,headline) VALUES (%s, %s, %s, %s, %s)''', (username,  email, password_hash, bio, headline))
            mysql.commit()
            
            cursor.execute('SELECT id FROM user_info WHERE email = %s', [email])
            account1 = cursor.fetchone()        
            
            print(account1[0])
            uniqueIDposts = str(account1[0]) + "posts"
            print(uniqueIDposts)
            uniqueIDUpdates = str(account1[0]) + 'updates'
            
            
            cursor.execute('''CREATE TABLE {projects} (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username varchar(255),
    userid INT NOT NULL,
    postid INT ,
    image_path varchar(255),
    headline varchar(255),
    project_image_path varchar(255),
    project_description varchar(255),
    likes INT
);'''.format(projects = uniqueIDposts))
            mysql.commit()
            
            cursor.execute('''CREATE TABLE {updates} (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username varchar(255),
    userid INT NOT NULL,
    updatesid INT,
    image_path varchar(255),
    headline varchar(255),
    project_description varchar(255)
);'''.format(updates = uniqueIDUpdates))
            mysql.commit()
            
            
            msg = 'You have successfully registered!'
            
            d['email'] = email
            d['username'] = username
            d['bio'] = bio
            d['headline'] = headline
            d['updates'] = uniqueIDUpdates
            d['projects'] = uniqueIDposts
        
        d['msg'] = msg
        return jsonify(d)
               
#-----------------------------------------------------------------------------------------------
#  ENDED HERE
#  USER AUTHENTICATION AND MANAGEMENT
#-----------------------------------------------------------------------------------------------
