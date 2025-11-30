from flask import Flask, request, jsonify
import products_dao
from backend import uom_dao
from backend.sql_connection import get_sql_connection
import json
app = Flask(__name__)
connection = get_sql_connection()
@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    uom = uom_dao.get_uoms(connection)
    response = jsonify(uom)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({'product_id': return_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({'product_id': product_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updateProduct', methods=['POST'])
def update_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.update_product(connection, request_payload)
    response = jsonify({'product_id': product_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("start")
    app.run(port=5000)
