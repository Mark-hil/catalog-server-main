from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import func
from . import app, db
from .models import Product, User

# Catalog Endpoints
@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify(
        [
            {"id": p.id, "name": p.name, "description": p.description, "price": p.price}
            for p in products
        ]
    )


@app.route("/api/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
    )


# Add Product Endpoint
@app.route("/api/products", methods=["POST"])
@jwt_required()  # Protect this endpoint with JWT authentication
def add_product():
    data = request.get_json()

    # Validate required fields
    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "Name and price are required"}), 400

    # Create a new product
    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),  # Optional field
        price=data["price"],
    )

    # Save the product to the database
    db.session.add(new_product)
    db.session.commit()

    return jsonify(
        {
            "message": "Product added successfully",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "description": new_product.description,
                "price": new_product.price,
            },
        }
    ), 201


# User Authentication Endpoints
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate the credentials
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate the input
    if not username or not password or not email:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful", "user": new_user.to_dict()}), 201


# Search Endpoint
@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # If the query is empty, return all products
    if not query:
        all_products = Product.query.paginate(page=page, per_page=per_page)
        results = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
            }
            for product in all_products.items
        ]
        return jsonify(
            {
                "results": results,
                "total": all_products.total,
                "page": all_products.page,
                "per_page": all_products.per_page,
                "total_pages": all_products.pages,
            }
        )

    # Perform a case-insensitive search on the product name
    search_results = Product.query.filter(
        Product.name.ilike(f"%{query}%")
    ).paginate(page=page, per_page=per_page)

    # Format the results
    results = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        for product in search_results.items
    ]

    # Return the results with pagination metadata
    return jsonify(
        {
            "results": results,
            "total": search_results.total,
            "page": search_results.page,
            "per_page": search_results.per_page,
            "total_pages": search_results.pages,
        }
    )

# Protected Endpoint (Example)
@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200