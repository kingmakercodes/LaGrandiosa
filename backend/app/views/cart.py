from flask import Blueprint, request, jsonify
from backend.app.utils.auth_utils import token_required
from backend.app import database
from backend.app.models.models import Cart, CartItem, Product, User


cart_blueprint= Blueprint('cart', __name__)


# function to get user's cart or create it if it doesn't exist
def get_cart(user_id):
    cart= Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        cart= Cart(user_id=user_id)
        database.session.add(cart)
        database.session.commit()

    return cart

