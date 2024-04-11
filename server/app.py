from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Pizza Restaurants API</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    return make_response(jsonify(restaurants), 200)

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_or_update_or_delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)
    
    if request.method == 'GET':
        return make_response(jsonify(restaurant.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response('', 204)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(jsonify(pizzas), 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not pizza_id or not restaurant_id:
        return make_response(jsonify({"errors": ["Missing required data"]}), 400)

    restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)

    try:
        db.session.add(restaurant_pizza)
        db.session.commit()
        return make_response(jsonify(restaurant_pizza.pizza.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({"errors": [str(e)]}), 400)


    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
