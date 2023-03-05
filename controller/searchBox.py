from flask import Blueprint, jsonify,request

#-----------------------------------------------------------------------------------------------
#  SEARCH FUNCTION AND MANAGEMENT
#  STARTING FROM HERE
#-----------------------------------------------------------------------------------------------

searchBox_api = Blueprint('searchBox_api', __name__)

@searchBox_api.route("/user/search_user/<searchQuery>", methods=['GET'])
def searchUsers(searchQuery):
    from app import mysql
    if request.method == 'GET':

        #searchQuery = request.json['search']

        search = '%' + searchQuery + '%'
        search = str(search)
        cursor = mysql.cursor()
        cursor.execute("SELECT image_path, username, headline FROM user_info WHERE username LIKE %s", [search])
        result = cursor.fetchall()

        # Convert the list of tuples to a list of dictionaries
        data = [{'image_path': row[0], 'username': row[1], 'headline': row[2]} for row in result]

        # Return the data as a JSON response
        return jsonify(data)
    else:
        return "Method not allowed"
    
# @searchBox_api.route("/groups/search_groups", methods = ['GET'])
# def searchUsers():
#     from app import mysql
#     if request.method == 'GET':
        
#         searchQuery = request.json['search']
        
#         search = '%' + searchQuery + '%'
#         search = str(search)
#         cursor = mysql.cursor()
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
#         cursor = mysql.cursor()
#         cursor.execute("SELECT image_path, username, headline FROM user_info WHERE username LIKE %s",[search])
#         result = cursor.fetchall()
        
#         return jsonify(result)
#     else:
#         return "Method not allowed"
    
