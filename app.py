from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
import pymysql

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Renuka@321',
    'database': 'user_creds',
}

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**db_config)
    return g.db

# Close the database connection when the application ends
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

class UserProfile(Resource):
    def post(self):
        data = request.get_json()

        # Validate mandatory fields
        if not data.get('customer_name') or not data.get('username') or not data.get('password'):
            return {'error': 'Customer name, username, and password are mandatory fields and cannot be empty.'}, 400

        customer_name = data['customer_name']
        username = data['username']
        password = data['password']
        gender = data.get('gender', None) if data.get('gender') != "" else None
        preferred_category = data.get('preferred_category', None) if data.get('preferred_category') != "" else None
        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            # Insert data into the user_creds table
            with get_db().cursor() as cur:
                cur.execute('''
                    INSERT INTO user_creds (customer_name, username, password, gender, preferred_category)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (customer_name, username, hashed_password, gender, preferred_category))
                get_db().commit()

            return {'message': 'User profile successfully inserted.'}, 201

        except pymysql.IntegrityError:
            return {'error': 'Username already exists. Choose a different username.'}, 409

        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(UserProfile, '/user-profile')

if __name__ == '__main__':
    app.run(debug=True)
