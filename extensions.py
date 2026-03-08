"""
Flask extensions for DropBy.HOLLOW
"""

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
CORS()
