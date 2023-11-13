from flask import Flask, request, jsonify
import pymysql
import random

app = Flask(__name__)

# Database configurations
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Renuka@321',
    'database': 'user_creds',
}

# Function to connect to the database
def connect_db():
    return pymysql.connect(**db_config)

# API endpoint to get product recommendations
@app.route('/get_product_recommendations', methods=['POST'])
def get_product_recommendations():
    # Get user input from the request
    data = request.get_json()
    username = data.get('username')
    
    

    with connect_db().cursor() as cursor:
        cursor.execute("SELECT * FROM user_creds WHERE username = %s", (username,))
        user_data = cursor.fetchone()

    if not user_data:
        return jsonify({'error': 'User not found'}), 404

    # Assuming that the preferred_category is the second column in user_creds table
    preferred_category_index = -1  # Index for the last element
    preferred_category = user_data[preferred_category_index]
    
    
    # Check if the preferred category is available
            
    # ...

    if not preferred_category:
    # If not available, return random 10 products
        with connect_db().cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY ranks LIMIT 10")
            columns = [desc[0] for desc in cursor.description]  # Get column names
            products = cursor.fetchall()
        print(products)
        print(f"Preferred Category: {preferred_category}")
        print("hello")
    else:
    # If available, return top 10 products based on ranks in the preferred category
        with connect_db().cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE product_category = %s ORDER BY ranks LIMIT 10", (preferred_category,))
            products = cursor.fetchall()
            print(f"Preferred Category: {preferred_category}")

            

# Get column names from cursor description
    columns = [column[0] for column in cursor.description]

# Format the result and return
    result = []
    for product in products:
        result.append(dict(zip(columns, product)))

    return jsonify(result)

    print(username)

if __name__ == '__main__':
    app.run(debug=True)
