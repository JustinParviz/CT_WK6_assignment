from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow


#internal imports
from .helpers import get_image


#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow() #makes marshmallow object


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object

#think of these as admin (keeping track of what products are available to sell)
class User(db.Model, UserMixin): 
    #CREATE TABLE User, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #this is going to grab a timestamp as soon as a User object is instantiated


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Car(db.Model): #db.Model helps us translate python code to columns in SQL 
    car_id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    horsepower =db.Column(db.String(50), nullable=True)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    prodord = db.relationship('ProdOrder', backref = 'car', lazy=True) # establishing relationship between ProdOrder & Product table


    def __init__(self, make, model, year, color, price, quantity, horsepower="", image="", description=""):
        self.car_id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.horsepower = horsepower
        self.image = self.set_image(image, make)
        self.description = description
        self.price = price
        self.quantity = quantity 

    
    def set_id(self):
        return str(uuid.uuid4())
    

    def set_image(self, image, name):

        if not image: #aka the user did not give us an image
            image = get_image(name) #name is our argument replacing the search parameter in our get_image() function 
            # come back and add the api call

        return image
    
    #we need a method for when customers buy products to decrement & increment our quantity 
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity 
    

    def __repr__(self):
        return f"<Car: {self.make}>"


#only need this for purposes of tracking what customers are tied to what orders & also how many customers we have
class Customer(db.Model):
    # CREATE TABLE
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    #this is how we tie a table to another one (so not a column but establishing a relationship)
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True) #lazy = True means is we dont need the ProdOrder table to have a customer

    def __init__(self, cust_id):
        self.cust_id = cust_id #when a customer makes an order on the frontend they will pass us their cust_id 


    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    


class Order(db.Model):
    # CREATE TABLE
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True) #establishing that relationship, NOT A COLUMN


    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00

    
    def set_id(self):
        return str(uuid.uuid4())
    

    # method to increase our order total
    def increment_ordertotal(self, price):

        self.order_total = float(self.order_total) #just making sure its a float 
        self.order_total += float(price)

        return self.order_total
    

    # method to decrement the order total for when people update or delete their order 
    def decrement_ordertotal(self, price):

        self.order_total = float(self.order_total) #just making sure its a float 
        self.order_total -= float(price)

        return self.order_total
    

    def __repr__(self):
        return f"<Order: {self.order_id}>"



#example of a join table
# because an Order can have many Products but a Product can be a part of many Orders (many-to-many) relationship


class ProdOrder(db.Model):
    # CREATE TABLE
    prodorder_id = db.Column(db.String, primary_key=True)
    #first instance of using a primary key as a foreign key on THIS table
    car_id = db.Column(db.String, db.ForeignKey('car.car_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)


    # INSERT INTO
    def __init__(self, car_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.car_id = car_id 
        self.quantity = quantity #how much quantity of that product we want to purchase
        self.price = self.set_price(quantity, price) #so price PER product 
        self.order_id = order_id
        self.cust_id = cust_id 


    def set_id(self):
        return str(uuid.uuid4())
    

    def set_price(self, quantity, price):

        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price #this total price for that product multiplied by quantity purchased 
        return self.price
    

    def update_quantity(self, quantity):

        self.quantity = int(quantity)
        return self.quantity











# creating our Schema class (Schema essentially just means what our data "looks" like, and our 
# data needs to look like a dictionary (json) not an object)


class ProductSchema(ma.Schema):

    class Meta:
        fields = ['car_id', 'make', 'model', 'year', 'color', 'horsepower', 'image', 'description', 'price', 'quantity']



#instantiate our ProductSchema class so we can use them in our application
product_schema = ProductSchema() #this is 1 singular product
products_schema = ProductSchema(many=True) #bringing back all the products in our database & sending to frontend