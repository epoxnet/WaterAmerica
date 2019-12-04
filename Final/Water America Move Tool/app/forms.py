from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app.USPS import AddressValidator
from app.move_date_validator import MoveDateValidator

class RegistrationForm(FlaskForm):
    last_name = StringField('Last Name')
    first_name = StringField('First Name')

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    # Register the new customer's address
    street_address = StringField('Street Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip_code = StringField('Zip Code',validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_street_address(self, street_address):
        address_validator = AddressValidator(street_address.data, self.city.data, self.state.data, self.zip_code.data)
        if not address_validator.validate_street_address():
            raise ValidationError('Please enter a valid street address.')

    def validate_city(self, city):
        address_validator = AddressValidator(self.street_address.data, city.data, self.state.data, self.zip_code.data)
        if not address_validator.validate_city():
            raise ValidationError('Please enter a valid city.')

    def validate_state(self, state):
        address_validator = AddressValidator(self.street_address.data, self.city.data, state.data, self.zip_code.data)
        if not address_validator.validate_state():
            raise ValidationError('Please enter a valid state.')

    def validate_zip_code(self, zip_code):
        address_validator = AddressValidator(self.street_address.data, self.city.data, self.state.data, zip_code.data)
        if not address_validator.validate_zip_code():
            raise ValidationError('Please enter a valid zip code.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateMoveForm(FlaskForm):
    move_date = StringField('Date', validators=[DataRequired()])
    street_address = StringField('Street Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip_code = StringField('Zip Code',validators=[DataRequired()])
    submit = SubmitField('Create Move')

    def validate_move_date(self, move_date):
        if not MoveDateValidator.validate_date_string(move_date.data):
            raise ValidationError('Please enter the date mm/dd/yyyy.')
        move_date_validator = MoveDateValidator(move_date.data)
        if not move_date_validator.validate_move_date():
            raise ValidationError('Please enter a valid future date.')

class EditMoveForm(FlaskForm):
    move_date = StringField('Date', validators=[DataRequired()])
    street_address = StringField('Street Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    zip_code = StringField('Zip Code',validators=[DataRequired()])
    submit = SubmitField('Edit Move')
    delete = SubmitField('Delete Move')
    
# Grave Yard
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')