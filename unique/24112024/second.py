class Product():
    def __init__(self, name, price, rating):
        self.name = name
        self.price = price
        self.rating = rating


class Category():
    def __init__(self, name, list_of_category):
        self.name = name
        self.list_of_category = list_of_category

    def show(self):
        print(f"{self.name}:")
        for el in self.list_of_category:
            print(f"  {el.name}:  {el.price}")

class Basket():
    def __init__(self, list_of_basket):
        self.list_of_basket = list_of_basket

class User():
    def __init__(self, login, password, basket):
        self.login = login
        self.password = password
        self.basket = basket

    def min_prices(self):
        print("Cheap products: ")
        for el in food.list_of_category:
            if el.price < 100:
                print(el.name, f"({el.price})")

        for el in drinks.list_of_category:
            if el.price < 100:
                print(el.name, f"({el.price})")


pizza = Product('Pizza (30 cm)', 700, 4)
coke = Product("Coke (0.3 l)", 125, 4.5)
hamburger = Product("Hamburger (middle)", 100, 4.4)
water = Product("Water (0.5 l)", 50, 4.8)

food = Category("Food", [pizza, hamburger])
drinks = Category("Drinks", [coke, water])

basket = Basket(["Hamburger (middle)", "Coke (0.3 l)"])

food.show()
drinks.show()

user = User('145', '543', basket)
print()
user.min_prices()
