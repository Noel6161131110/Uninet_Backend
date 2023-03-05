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
        
        cursor = mysql.cursor()
        cursor.execute("SELECT username, headline, image_path FROM user_info WHERE (id = %s);",[uid])
        account = cursor.fetchone()
        
        cursor = mysql.cursor()
        cursor.execute('''INSERT INTO {posts}(username,userid,image_path,headline,project_description,postid,likes) VALUES(%s,%s,%s,%s,%s,%s,%s);'''.format(posts=uniqueIDposts), (account[0], uid, account[2], account[1], project_description, 0, 0))
        mysql.commit()
 
        cursor.execute('''SELECT id FROM {posts} ORDER BY id DESC LIMIT 1'''.format(posts=uniqueIDposts))
        account1 = cursor.fetchone()  
        
        postid = str(uid) + str(account1[0])     
        cursor.execute('''UPDATE {posts} SET postid = %s WHERE id= %s;'''.format(posts=uniqueIDposts),(int(postid),account1[0]))
        mysql.commit()   
             
        cursor = mysql.cursor()
        cursor.execute('''INSERT INTO posts (username,image_path,headline,project_description,likes,userid,postid) VALUES(%s,%s,%s,%s,%s,%s,%s);''', (account[0], account[2], account[1], project_description, 0, uid, int(postid)))
        mysql.commit()
       
        d["status"] = 1
        
        return jsonify(d)
    else:
        return "Method not allowed"

@userPost_api.route('/user/<uid>/add/upload', methods = ['PUT'])
def uploadUserPostImage(uid):   
    from app import mysql
    d = {}
    if request.method == 'PUT':           
        
        file = request.files['post_image']
        
        new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
        split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
        ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
        ext = split_filename[ext_pos] # Using last index to get the file extension
        db_path = f"storage/user_posts/{new_filename}.{ext}"
        file.save(f"storage/user_posts/{new_filename}.{ext}")
        
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.cursor()
        
        cursor.execute('''SELECT id FROM {posts} ORDER BY id DESC LIMIT 1;'''.format(posts = uniqueIDposts))
        account1 = cursor.fetchone() 
        
        cursor.execute('''UPDATE {posts} SET project_image_path = %s WHERE id= %s;'''.format(posts = uniqueIDposts),(db_path,account1[0]))
        mysql.commit()
        
        cursor.execute('''SELECT id FROM posts ORDER BY id DESC LIMIT 1;''')
        account2 = cursor.fetchone() 
        
        cursor.execute('''UPDATE posts SET project_image_path = %s WHERE id= %s;''',(db_path,account2[0]))
        mysql.commit()       
        
        d["status"] = 1
        d["message"] = "File uploaded successfully"
        d["path"] = db_path
        
        return jsonify(d)

    else:
        return "Method not allowed"

@userPost_api.route('/user/<uid>/get/post', methods=['GET'])
def getCurrentUserPost(uid):
    from app import mysql
    
    if request.method == 'GET': 
        uniqueIDposts = str(uid) + "posts"
        
        cursor = mysql.cursor()
        cursor.execute('''SELECT id, username, image_path, headline, project_image_path, project_description, likes, userid, postid FROM {posts}'''.format(posts=uniqueIDposts))
        result = cursor.fetchall()
        
        # Convert list of tuples to list of dictionaries
        posts = [
            {
                'id': post[0],
                'username': post[1],
                'image_path': post[2],
                'headline': post[3],
                'project_image_path': post[4],
                'project_description': post[5],
                'likes': post[6],
                'userid': post[7],
                'postid': post[8]
            }
            for post in result
        ]
        
        return jsonify(posts) 
    else:
        return 'Something is wrong'
    
@userPost_api.route('/user/get/allposts', methods=['GET'])
def getAllUserPost():
    from app import mysql
    
    if request.method == 'GET': 
        cursor = mysql.cursor()
        cursor.execute('''SELECT id, username, image_path, headline, project_image_path, project_description, likes, userid, postid FROM posts ORDER BY id DESC LIMIT 10''')
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        posts = []
        for row in result:
            post = {
                'id': row[0],
                'username': row[1],
                'image_path': row[2],
                'headline': row[3],
                'project_image_path': row[4],
                'project_description': row[5],
                'likes': row[6],
                'userid': row[7],
                'postid': row[8]
            }
            posts.append(post)

        # Return the result as JSON
        return jsonify(posts) 
    else:
        return 'Something is wrong'
    
@userPost_api.route('/user/<uid>/<id>/delete/post', methods=['DELETE'])
def deleteUserPost(uid, id):
    from app import mysql

    if request.method == 'DELETE':

        uniqueIDposts = str(uid) + "posts"

        cursor = mysql.cursor()

        cursor.execute(''' SELECT postid, userid FROM {posts} WHERE id = %s'''.format(posts=uniqueIDposts), (id,))
        postInfo = cursor.fetchone()

        cursor.execute(''' DELETE FROM posts WHERE postid = %s AND userid = %s''',
                       (postInfo[0], postInfo[1]))
        mysql.commit()

        cursor.execute(''' DELETE FROM {posts} WHERE postid = %s AND userid = %s'''.format(posts=uniqueIDposts),
                       (postInfo[0], postInfo[1]))
        mysql.commit()

        return "Deleted"

    else:
        return 'Something is wrong'
    
@userPost_api.route('/post/<id>/update/likes', methods=['PUT'])
def updateLikesAllPost(id):
    from app import mysql
    try:
        if request.method == 'PUT':

            cursor = mysql.cursor()

            cursor.execute('''SELECT postid, userid, likes FROM posts WHERE id = %s''', (id,))
            postInfo = cursor.fetchone()

            uniqueIDposts = str(postInfo[1]) + "posts"

            cursor.execute('''UPDATE {posts} SET likes = %s WHERE postid = %s AND userid = %s;'''.format(posts=uniqueIDposts), (postInfo[2] + 1, postInfo[0], postInfo[1]))
            mysql.commit()

            cursor.execute('''UPDATE posts SET likes = %s WHERE postid = %s AND userid = %s;''', (postInfo[2] + 1, postInfo[0], postInfo[1]))
            mysql.commit()

            d = {"status": "success", "message": "Updated likes count."}
            return jsonify(d)
        else:
            return jsonify({"status": "error", "message": "Method not allowed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})