from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurant_pizzas.restaurant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')
    pizzas = association_proxy('restaurant_pizzas', 'pizza',
                                 creator=lambda pizza_obj: RestaurantPizza(pizza=pizza_obj))
   

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) > 50:
            raise ValueError('Name must be less than 50 characters')
        return name

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurant_pizzas.pizza',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=True)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')
    restaurants = association_proxy('restaurant_pizzas', 'restaurants',
                                 creator=lambda restaurant_obj: RestaurantPizza(restaurant=restaurant_obj))
    

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-pizza.restaurant_pizzas','-restaurant.restaurant_pizzas',)

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError('Price must be between 1 and 30')
        return price
