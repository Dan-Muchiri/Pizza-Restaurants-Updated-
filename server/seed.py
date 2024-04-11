from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

def seed():
    with app.app_context():
        # Clear existing data
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()

        # Create some restaurants
        dominion_pizza = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue", phone="123456789")
        pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100", phone="987654321")
        
        db.session.add(dominion_pizza)
        db.session.add(pizza_hut)

        # Create some pizzas
        cheese_pizza = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
        pepperoni_pizza = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        
        db.session.add(cheese_pizza)
        db.session.add(pepperoni_pizza)

        # Commit the pizza objects to the session to generate their IDs
        db.session.commit()

        # Create RestaurantPizza objects to associate pizzas with restaurants
        dominion_pizza_cheese = RestaurantPizza(restaurant=dominion_pizza, pizza=cheese_pizza, price=10.99)
        dominion_pizza_pepperoni = RestaurantPizza(restaurant=dominion_pizza, pizza=pepperoni_pizza, price=12.99)
        
        pizza_hut_cheese = RestaurantPizza(restaurant=pizza_hut, pizza=cheese_pizza, price=11.99)
        pizza_hut_pepperoni = RestaurantPizza(restaurant=pizza_hut, pizza=pepperoni_pizza, price=13.99)
        
        # Add RestaurantPizza objects to the session
        db.session.add(dominion_pizza_cheese)
        db.session.add(dominion_pizza_pepperoni)
        db.session.add(pizza_hut_cheese)
        db.session.add(pizza_hut_pepperoni)

        # Commit the changes
        db.session.commit()

if __name__ == '__main__':
    seed()
