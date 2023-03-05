from flask import Blueprint, jsonify,request

#-----------------------------------------------------------------------------------------------
#  SEARCH FUNCTION AND MANAGEMENT
#  STARTING FROM HERE
#-----------------------------------------------------------------------------------------------

searchBox_api = Blueprint('searchBox_api', __name__)

@searchBox_api.route("/user/search_user", methods = ['GET'])
def searchUsers():
    from app import mysql
    if request.method == 'GET':
        
        searchQuery = request.json['search']
        
        search = '%' + searchQuery + '%'
        search = str(search)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT image_path, username, headline FROM user_info WHERE username LIKE %s",[search])
        result = cursor.fetchall()
        
        return jsonify(result)
    else:
        return "Method not allowed"
    
# @searchBox_api.route("/groups/search_groups", methods = ['GET'])
# def searchUsers():
#     from app import mysql
#     if request.method == 'GET':
        
#         searchQuery = request.json['search']
        
#         search = '%' + searchQuery + '%'
#         search = str(search)
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT image_path, username, headline FROM user_info WHERE username LIKE %s",[search])
#         result = cursor.fetchall()
        
#         return jsonify(result)
#     else:
#         return "Method not allowed"
    
# @searchBox_api.route("/projects/search_projects", methods = ['GET'])
# def searchUsers():
#     from app import mysql
#     if request.method == 'GET':
        
#         searchQuery = request.json['search']
        
#         search = '%' + searchQuery + '%'
#         search = str(search)
#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT image_path, username, headline FROM user_info WHERE username LIKE %s",[search])
#         result = cursor.fetchall()
        
#         return jsonify(result)
#     else:
#         return "Method not allowed"
    
