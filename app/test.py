import pytest
from app import app, db
from app.models import Product, User
import json

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client
#             db.session.remove()
#             db.drop_all()

# @pytest.fixture
# def auth_headers():
#     # Create a test user and get JWT token
#     user = User(username='testuser', email='test@test.com')
#     user.set_password('password123')
#     db.session.add(user)
#     db.session.commit()
    
#     response = client.post('/api/login', 
#         json={'username': 'testuser', 'password': 'password123'})
#     token = response.json['access_token']
#     return {'Authorization': f'Bearer {token}'}

def test_get_products(client):
    # Test getting all products
    response = client.get('/api/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_product(client):
    # Create a test product
    product = Product(name='Test Product', description='Test Description', price=99.99)
    db.session.add(product)
    db.session.commit()

    # Test getting a specific product
    response = client.get(f'/api/products/{product.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Product'
    assert response.json['price'] == 99.99

# def test_add_product(client, auth_headers):
#     # Test adding a new product
#     product_data = {
#         'name': 'New Product',
#         'description': 'New Description',
#         'price': 199.99
#     }
#     response = client.post('/api/products', 
#         json=product_data,
#         headers=auth_headers)
    
#     assert response.status_code == 201
#     assert response.json['product']['name'] == 'New Product'
#     assert response.json['message'] == 'Product added successfully'

def test_search_products(client):
    # Create test products
    products = [
        Product(name='iPhone', description='Apple Phone', price=999.99),
        Product(name='Galaxy', description='Samsung Phone', price=899.99)
    ]
    db.session.bulk_save_objects(products)
    db.session.commit()

    # Test search functionality
    response = client.get('/api/search?q=iphone')
    assert response.status_code == 200
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['name'] == 'iPhone'

def test_user_signup(client):
    # Test user registration
    user_data = {
        'username': 'newuser',
        'email': 'new@user.com',
        'password': 'password123'
    }
    response = client.post('/api/signup', json=user_data)
    assert response.status_code == 201
    assert response.json['message'] == 'Signup successful'

def test_user_login(client):
    # Create a test user
    user = User(username='logintest', email='login@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    # Test login
    response = client.post('/api/login', 
        json={'username': 'logintest', 'password': 'password123'})
    assert response.status_code == 200
    assert 'access_token' in response.json