from flask import Blueprint, request, jsonify
from backend.app.utils.auth_utils import token_required
from backend.app import database
from backend.app.models.models import Cart, CartItem, Product, User


cart_blueprint= Blueprint('cart', __name__)


# function to get user's cart or create it if it doesn't exist
def get_or_create_cart(user_id):
    cart= Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        cart= Cart(user_id=user_id)
        database.session.add(cart)
        database.session.commit()

    return cart


# view cart and its items
@cart_blueprint.route('/cart', methods=["GET"])
@token_required
def view_cart(user_cart):
    user_cart= Cart.query.filter_by(user_id=user_cart.id).first()

    if not user_cart:
        return jsonify({'message':'Cart is empty!'}), 200

    items= [
        {
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity
        }
        for item in user_cart.items
    ]

    return jsonify({'items': items}), 200


# add items to cart
@cart_blueprint.route('/cart/add', methods=['POST'])
@token_required
def add_to_cart(user_id):
    data= request.get_json()
    product_id= data.get('product_id')
    quantity= data.get('quantity', 1)

    if not product_id:
        return jsonify({'message':'Product ID is required.'}), 400

    # fetch or create cart for the user
    cart= get_or_create_cart(user_id)

    # check if the item is already in cart
    cart_item= CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        cart_item= CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)

        database.session.add(cart_item)
        database.session.commit()
        return jsonify({'message':'Item added to cart successfully!'}), 200

    cart_item.quantity += quantity # if product with id already exists, increase quantity


# remove from cart
@cart_blueprint.route('/cart/remove', methods=['DELETE'])
@token_required
def remove_from_cart(user_id):
    data= request.get_json()
    item_id= data.get('item.id')

    if not item_id:
        return jsonify({'message':'Item ID is required.'}), 400

    cart_item= CartItem.query.filter_by(id=item_id, cart_id=user_id.cart.id).first()
    if not cart_item:
        return jsonify({'message':'Item not found in cart!'}), 404

    database.session.delete(cart_item)
    database.session.commit()

    return jsonify({'message':'Item removed from cart successfully!'}), 200