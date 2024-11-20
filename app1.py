from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for products
products = []
product_id_counter = 1

@app.route('/products', methods=['GET'])
def get_products():
    """Retrieve the list of products."""
    return jsonify(products), 200

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    global product_id_counter
    data = request.get_json()
    
    # Validate input data
    if not data or 'name' not in data or 'description' not in data or 'price' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Missing required fields'}), 400

    new_product = {
        'id': product_id_counter,
        'name': data['name'],
        'description': data['description'],
        'price': data['price']
    }
    products.append(new_product)
    product_id_counter += 1
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Retrieve a single product by ID."""
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Not Found', 'message': 'Product not found'}), 404
    return jsonify(product), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product by ID."""
    data = request.get_json()
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product is None:
        return jsonify({'error': 'Not Found', 'message': 'Product not found'}), 404

    if 'name' in data:
        product['name'] = data['name']
    if 'description' in data:
        product['description'] = data['description']
    if 'price' in data:
        product['price'] = data['price']

    return jsonify(product), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product by ID."""
    global products
    products = [prod for prod in products if prod['id'] != product_id]
    return jsonify({'message': 'Product deleted successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)