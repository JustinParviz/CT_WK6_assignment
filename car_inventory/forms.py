from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo

#creating our login & register forms 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired() ])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[ DataRequired() ])
    email = StringField('Email', validators= [ DataRequired(), Email()])
    password = PasswordField('Password', validators = [ DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class CarForm(FlaskForm):
    make = StringField('Make', validators=[ DataRequired() ] )
    model = StringField('Model', validators=[ DataRequired() ] )
    year = IntegerField('Year', validators=[ DataRequired() ])
    color = StringField('Color', validators=[ DataRequired() ] )
    horsepower = IntegerField('Horsepower **Optional')
    image = StringField('Img url **Optional')
    description = StringField('Description **Optional')
    price = DecimalField('Price', validators=[ DataRequired() ])
    quantity = IntegerField('Quantity', validators=[ DataRequired() ])
    submit = SubmitField('Submit')