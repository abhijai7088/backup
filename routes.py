import os

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from .extensions import mongo

# for checking and testing the mongo db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)





bp = Blueprint('api', __name__, url_prefix='/api')

# Allowed extensions for uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload image file and product data
@bp.route('/upload', methods=['POST'])
def upload():
    product_name = request.form.get('product_name')
    brand_name = request.form.get('brand_name')
    nfc_token = request.form.get('nfc_token')
    file = request.files.get('file')

    if not file:
        logger.error("No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    file_url = f"/api/uploads/{filename}"

    product_data = {
        'product_name': product_name,
        'brand_name': brand_name,
        'nfc_token': nfc_token,
        'image_url': file_url
    }

    try:
        result = mongo.db.nfc_products.insert_one(product_data)
        logger.info(f"Inserted product with id: {result.inserted_id}")
        return jsonify({'message': 'File and data saved successfully', 'image_url': file_url}), 200
    except Exception as e:
        logger.error(f"Failed to insert into MongoDB: {str(e)}")
        return jsonify({'error': 'Failed to insert into MongoDB', 'details': str(e)}), 500


# Serve uploaded files from uploads folder
@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)


# Store blockchain token metadata
@bp.route('/token', methods=['POST'])
def store_token_data():
    try:
        data = request.get_json(force=True, silent=True)
        logger.debug(f"Received token data: {data}")

        if not data:
            logger.error("Invalid JSON or no data provided")
            return jsonify({"error": "Invalid JSON or no data provided"}), 400

        required_fields = ["token_id", "nfc_tag_id", "metadata_uri", "owner_address", "product_name", "timestamp"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            logger.error(f"Missing fields: {missing_fields}")
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        token_document = {field: data[field] for field in required_fields}
        logger.info(f"Inserting token metadata into MongoDB: {token_document}")

        result = mongo.db.tokens.insert_one(token_document)
        logger.info(f"Inserted token with id: {result.inserted_id}")
        return jsonify({"message": "Token data stored successfully"}), 201

    except Exception as e:
        logger.error(f"Exception during token store: {str(e)}")
        return jsonify({"error": f"Failed to store data: {str(e)}"}), 500

# Verify token or NFC tag
@bp.route('/verify_nfc', methods=['GET', 'POST'])
def verify_nfc():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True) or request.form.to_dict()
        else:
            data = request.args.to_dict()

        token_id = data.get('token_id')
        nfc_tag_id = data.get('nfc_tag_id')

        if not token_id and not nfc_tag_id:
            return jsonify({"error": "Please provide either token_id or nfc_tag_id"}), 400

        query = {}
        if token_id:
            query['token_id'] = token_id
        if nfc_tag_id:
            query['nfc_tag_id'] = nfc_tag_id

        token_data = mongo.db.tokens.find_one(query, {"_id": 0})

        if token_data:
            return jsonify({"valid": True, "token_data": token_data}), 200
        else:
            return jsonify({"valid": False, "message": "Token or NFC tag not found"}), 404

    except Exception as e:
        current_app.logger.error(f"Error in verify_nfc: {str(e)}")
        return jsonify({"error": "Server error occurred"}), 500


# Health check endpoint
@bp.route('/status', methods=['GET'])
def status():
    return "Smart NFC + Blockchain Backend is running."


# Serve React SPA with fallback to index.html
@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def serve_react_app(path):
    dist_path = current_app.static_folder
    full_path = os.path.join(dist_path, path)

    if path and os.path.exists(full_path):
        return send_from_directory(dist_path, path)
    else:
        return send_from_directory(dist_path, 'index.html')
