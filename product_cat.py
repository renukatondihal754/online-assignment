from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Connect to the database
db = pymysql.connect(host='localhost', user='root', password='Renuka@321', database='user_creds')
cursor = db.cursor()

@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()

    keyword = data.get('search_keyword')
    price_min = data.get('price_min')
    price_max = data.get('price_max')

    # Build the SQL query based on the provided parameters
    sql_query = "SELECT * FROM products WHERE 1"

    if keyword is not None:
        sql_query += " AND (product_description LIKE %s OR brand_name LIKE %s)"
        keyword_pattern = '%' + keyword + '%'
    else:
        keyword_pattern = None

    if price_min and price_max:
        sql_query += " AND price BETWEEN %s AND %s"

    sql_query += " ORDER BY ranks LIMIT 10"

    # Execute the query
    cursor.execute(sql_query, (keyword_pattern, keyword_pattern, price_min, price_max))

    # Fetch results
    results = cursor.fetchall()

    # Convert results to a list of dictionaries
    products_list = []
    for row in results:
        product = {
            "product_id": row[0],
            "product_category": row[1],
            "rank": row[2],
            "brand_name": row[3],
            "product_description": row[4],
            "price": row[5],
            "image_link": row[6]
        }
        products_list.append(product)

    # Close the database connection
    db.close()

    return jsonify(products_list)

if __name__ == '__main__':
    app.run(debug=True)
