from flask import request, jsonify, send_from_directory
from models import Friends
from config import db, app
import os


frontend_folder = os.path.join(os.getcwd(), "..", "frontend")
dist_folder = os.path.join(frontend_folder, "dist")

# server static files from "dist" folder under the "frontend" directory
@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(dist_folder, filename)

# CRUD API


# Get friends data
@app.route("/api/friends", methods=['GET'])
def get_friends():
    friends = Friends.query.all()
    result = [friend.to_json() for friend in friends]
    return (jsonify(result), 200)

# Create a friends
@app.route('/api/friends', methods=['POST'])
def create_friends():
    try:
        data = request.json

        required_fields = ['name', 'role', 'description', 'gender']
        for field in required_fields:
            if field not in data or not data.get(field):
                return (jsonify({'error': f'{field} is required'}), 400)

        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')
        
        # Fetch avatar image based on gender
        if gender == 'male':
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None 

        new_friend = Friends(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_friend)
        db.session.commit()

        return (jsonify(new_friend.to_json()), 201)

    except Exception as e:
        db.session.rollback()
        return (jsonify({"error": str(e)}), 400)
    

# Delete a friend
@app.route('/api/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    try:
        friend = Friends.query.get(id)
        
        if not friend:
            return (jsonify({'error': 'Friend not found'}), 404)
        
        db.session.delete(friend)
        db.session.commit()
        return (jsonify({'msg': 'Friend successfuly deleted!'}), 200)
    
    except Exception as e:
        db.session.rollback()
        return (jsonify({"error": str(e)}), 400)
    

# Upadate profile data
@app.route('/api/friends/<int:id>', methods=['PATCH'])
def update_friends(id):
    try:
        friend = Friends.query.get(id)
        
        if not friend:
            return (jsonify({'error': 'Friend not found'}), 404)
        
        data = request.json
        
        friend.name = data.get('name', friend.name)
        friend.role = data.get('role', friend.role)
        friend.description = data.get('description', friend.description)
        friend.gender = data.get('gender', friend.gender)

        db.session.commit()
        return (jsonify(friend.to_json()), 200)
    except Exception as e:
        db.session.rollback()
        return (jsonify({"error": str(e)}), 400)
        

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)