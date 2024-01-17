# Flask imports
from flask import blueprints, jsonify

# Local imports
from app.utils import api_key_required

check = blueprints.Blueprint("status", __name__)


@check.route("/status", methods=["GET"])
def health_check():
    return jsonify({"message": "Up and running"}), 200


@check.route("/auth", methods=["GET"])
@api_key_required
def check_user_api():
    return jsonify({"message": "API token is valid"}), 200
