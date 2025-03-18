import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes, allowing requests from http://localhost:3001
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001"}})
CORS(app, resources="*")


# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")  # Get from .env file
database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print(f"Connecting to database: {database_uri}")

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Get from .env file

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import routes
from app import models, routes
