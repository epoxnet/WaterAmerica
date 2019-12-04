from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

    
class User(UserMixin, db.Model):
    # meta data
    id = db.Column(db.Integer, primary_key=True)
    date_of_creation = db.Column(db.DateTime, index=True, default = datetime.utcnow)

    # personal information
    last_name = db.Column(db.String(128), index=True)
    first_name = db.Column(db.String(128), index=True)
    current_street_address = db.Column(db.String(120), index=True)
    current_city = db.Column(db.String(120), index=True)
    current_state = db.Column(db.String(20), index=True)
    current_zip_code = db.Column(db.String(120), index=True)

    # account information
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # WA_MOVE information
    is_moving = db.Column(db.Boolean, index=True, default=False)
    move_date = db.Column(db.DateTime, index=True, default=None)

    future_street_address = db.Column(db.String(120), index=True, default=None)
    future_city = db.Column(db.String(120), index=True, default=None)
    future_state = db.Column(db.String(20), index=True, default=None)
    future_zip_code = db.Column(db.String(120), index=True, default=None)

    def __repr__(self):
        return 'ID: {}\nDate of Creation: {}\nLast Name: {}\nFirst Name: {}\nCurrent Street Address: {}\n'\
            'Current City: {}\nCurrent State: {}\nCurrent Zip Code: {}\nUsername: {}\n'\
                'email: {}\nIs Moving: {}\nMove Date: {}\nFuture Street Address: {}\n'\
                    'Future City: {}\nFuture State: {}\nFuture Zip Code: {}\n'.format(
                        self.id,
                        self.date_of_creation,
                        self.last_name,
                        self.first_name,
                        self.current_street_address,
                        self.current_city,
                        self.current_state,
                        self.current_zip_code,
                        self.username,
                        self.email,
                        self.is_moving,
                        self.move_date,
                        self.future_street_address, 
                        self.future_city,
                        self.future_state, 
                        self.future_zip_code
                    ) 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))