from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def init_app(app):
    # Existing database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ticket'
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    app.config['SQLALCHEMY_POOL_SIZE'] = 30
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'your-app-password'     # Replace with your app password
    
    db.init_app(app)
    mail.init_app(app)