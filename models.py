# app/models.py
from .extensions import mongo

def insert_token(token_data):
    return mongo.db.tokens.insert_one(token_data).inserted_id

def insert_product(data):
    return mongo.db.nfc_products.insert_one(data)

def find_token_by_nfc(nfc_tag_id):
    return mongo.db.tokens.find_one({"nfc_tag_id": nfc_tag_id})

def find_token_by_token_id(token_id):
    return mongo.db.tokens.find_one({"token_id": token_id})

def get_collection():
    return mongo.db.tokens
