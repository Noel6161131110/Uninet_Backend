from flask import Blueprint, jsonify,request, send_file
from datetime import datetime

userPost_api = Blueprint('userPost_api', __name__)

@userPost_api.route('/user/<uid>/add/post', methods = ['POST'])
def uploadUserPost(uid):
    from app import mysql
    d = {}
    if request.method == 'POST':
        
        project_description = request.json['project_description']
        
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, headline, image_path FROM user_info WHERE (id = %s);",[uid])
        account = cursor.fetchone()
        
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO {posts}(username,userid,image_path,headline,project_description,postid,likes) VALUES(%s,%s,%s,%s,%s,%s,%s);'''.format(posts = uniqueIDposts), (account["username"], uid, account["image_path"], account["headline"], project_description,0,0))
        mysql.connection.commit()
 
        cursor.execute('''SELECT id FROM {posts} ORDER BY id DESC LIMIT 1'''.format(posts = uniqueIDposts))
        account1 = cursor.fetchone()  
        
        postid = str(uid) + str(account1["id"])     
        cursor.execute('''UPDATE {posts} SET postid = %s WHERE id= %s;'''.format(posts = uniqueIDposts),(int(postid),account1["id"]))
        mysql.connection.commit()   
             
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO posts (username,image_path,headline,project_description,likes,userid,postid) VALUES(%s,%s,%s,%s,%s,%s,%s);''', (account["username"], account["image_path"], account["headline"], project_description,0 ,uid,int(postid)))
        mysql.connection.commit()
       
        d["status"] = 1
        
        return jsonify(d)
    else:
        return "Method not allowed"

@userPost_api.route('/user/<uid>/add/upload', methods = ['POST'])
def uploadUserPostImage(uid):   
    from app import mysql
    d = {}
    if request.method == 'POST':           
        
        file = request.files['post_image']
        
        new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
        split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
        ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
        ext = split_filename[ext_pos] # Using last index to get the file extension
        db_path = f"storage/user_posts/{new_filename}.{ext}"
        file.save(f"storage/user_posts/{new_filename}.{ext}")
        
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.connection.cursor()
        
        cursor.execute('''SELECT id FROM {posts} ORDER BY id DESC LIMIT 1;'''.format(posts = uniqueIDposts))
        account1 = cursor.fetchone() 
        
        cursor.execute('''UPDATE {posts} SET project_image_path = %s WHERE id= %s;'''.format(posts = uniqueIDposts),(db_path,account1["id"]))
        mysql.connection.commit()
        
        cursor.execute('''SELECT id FROM posts ORDER BY id DESC LIMIT 1;''')
        account2 = cursor.fetchone() 
        
        cursor.execute('''UPDATE posts SET project_image_path = %s WHERE id= %s;''',(db_path,account2["id"]))
        mysql.connection.commit()       
        
        d["status"] = 1
        d["message"] = "File uploaded successfully"
        d["path"] = db_path
        
        return jsonify(d)

    else:
        return "Method not allowed"

@userPost_api.route('/user/<uid>/get/post', methods = ['GET'])
def getCurrentUserPost(uid):
    from app import mysql
    
    if request.method == 'GET': 
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM {posts}'''.format(posts = uniqueIDposts))
        result = cursor.fetchall()
        return jsonify(result) 
    else:
        return 'Something is wrong'
    
@userPost_api.route('/user/get/allposts', methods = ['GET'])
def getAllUserPost():
    from app import mysql
    
    if request.method == 'GET': 
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM posts ORDER BY id DESC LIMIT 10''')
        result = cursor.fetchall()
        return jsonify(result) 
    else:
        return 'Something is wrong'
    
@userPost_api.route('/user/<uid>/<id>/delete/post', methods = ['DELETE'])
def deleteUserPost(uid,id):
    from app import mysql
    
    if request.method == 'DELETE':
        
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.connection.cursor()
        
        cursor.execute(''' SELECT postid, userid FROM {posts} WHERE id = %s'''.format(posts = uniqueIDposts),(id))
        postInfo = cursor.fetchone()

        cursor.execute(''' DELETE FROM posts WHERE postid = %s AND userid = %s''',
                        (postInfo["postid"], postInfo["userid"]))
        mysql.connection.commit()
                
        cursor.execute(''' DELETE FROM {posts} WHERE postid = %s AND userid = %s'''.format(posts = uniqueIDposts),
                        (postInfo["postid"], postInfo["userid"]))
        mysql.connection.commit()
        
        return "Deleted"
        
    else:
        return 'Something is wrong' 
    
@userPost_api.route('/post/<id>/update/likes', methods = ['PUT'])
def updateLikesAllPost(id):
    from app import mysql
    d = {}
    if request.method == 'PUT':
        
        cursor = mysql.connection.cursor()
        
        cursor.execute('''SELECT postid, userid, likes FROM posts WHERE id = %s''',(id))
        postInfo = cursor.fetchone()
        
        uniqueIDposts = str(postInfo["userid"]) + "posts"
        
        cursor.execute('''UPDATE {posts} SET likes = %s WHERE postid = %s AND userid = %s;'''.format(posts = uniqueIDposts),(postInfo["likes"]+1, postInfo["postid"], postInfo["userid"]))
        mysql.connection.commit()             
           
        cursor.execute('''UPDATE posts SET likes = %s WHERE postid = %s AND userid = %s;''',(postInfo["likes"]+1, postInfo["postid"], postInfo["userid"]))
        mysql.connection.commit()
        
        return "updated likes"  
    else:
        return "Method not allowed"