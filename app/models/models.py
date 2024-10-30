from app import database
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# user model
class User(database.Model):
    __tablename__='users'
    id= database.Column(database.Integer, primary_key=True)
    username= database.Column(database.String(80), unique=True, nullable=False)
    email= database.Column(database.String(120), unique=True, nullable=False)
    password_hash= database.Column(database.String(255), nullable=False)
    created_at= database.Column(database.DateTime, default=datetime.utcnow)
    is_admin= database.Column(database.Boolean, default=False)

    # model relationships
    orders= database.relationship('Order', back_populates='user')
    cart= database.relationship('Cart', uselist=False, back_populates='user')

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# product category model
class Category(database.Model):
    __tablename__='categories'
    id= database.Column(database.Integer, primary_key=True)
    name= database.Column(database.String(80), unique=True, nullable=False)

    # model relationships
    products= database.relationship('Product', back_populates='category')


# product model
class Product(database.Model):
    __tablename__='products'
    id= database.Column(database.Integer, primary_key=True)
    name= database.Column(database.String(80), unique=True, nullable=False)
    description= database.Column(database.Text, nullable=False)
    price= database.Column(database.Float, nullable=False)
    stock= database.Column(database.Integer, nullable=False)

    # foreign keys
    category_id= database.Column(database.Integer, database.ForeignKey('categories.id'))

    # model relationships
    category= database.relationship('Category', back_populates='products')
    order_items= database.relationship('OrderItem', back_populates='product')
    cart_items= database.relationship('CartItem', back_populates='product')


# order model
class Order(database.Model):
    __tablename__='orders'
    id= database.Column(database.Integer, primary_key=True)
    status= database.Column(database.String(20), default='Pending')
    total_amount= database.Column(database.Float, nullable=False)
    created_at= database.Column(database.DateTime, default= datetime.utcnow)

    # foreign keys
    user_id= database.Column(database.Integer, database.ForeignKey('users.id'))
    cart_id= database.Column(database.Integer, database.ForeignKey('carts.id'), nullable=True)

    # order relationships
    user= database.relationship('User', back_populates='orders')
    items= database.relationship('OrderItem', back_populates='order')
    cart= database.relationship('Cart')


# order item model
class OrderItem(database.Model):
    __tablename__='order_items'
    id= database.Column(database.Integer, primary_key=True)
    quantity= database.Column(database.Integer, nullable=False)
    price= database.Column(database.Float, nullable=False)

    # foreign keys
    order_id= database.Column(database.Integer, database.ForeignKey('orders.id'))
    product_id= database.Column(database.Integer, database.ForeignKey('products.id'))

    # model relationships
    order= database.relationship('Order', back_populates='items')
    product= database.relationship('Product', back_populates='order_items')


# cart model
class Cart(database.Model):
    __tablename__='carts'
    id= database.Column(database.Integer, primary_key=True)
    created_at= database.Column(database.DateTime, default=datetime.utcnow())

    # foreign keys
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    # model relationships
    user= database.relationship('User', back_populates='cart')
    items= database.relationship('CartItem', back_populates='cart')


# cart item model
class CartItem(database.Model):
    __tablename__='cart_items'
    id= database.Column(database.Integer, primary_key=True)
    quantity= database.Column(database.Integer, nullable=False)

    # foreign keys
    cart_id= database.Column(database.Integer, database.ForeignKey('carts.id'))
    product_id= database.Column(database.Integer, database.ForeignKey('products.id'))

    # model relationships
    cart= database.relationship('Cart', back_populates='items')
    product= database.relationship('Product', back_populates='cart_items')