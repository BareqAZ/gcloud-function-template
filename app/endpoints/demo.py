# Flask imports
from flask import blueprints, jsonify, request

# Local imports
from app.utils import api_key_required

demo = blueprints.Blueprint("demo", __name__)


@demo.route("", methods=["GET", "POST"])
@api_key_required
def get_demo():
    """
    This is an example of a simple API endpoint.

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = {}
    request_args = request.args

    if request.method == "POST":
        request_json = request.get_json(silent=True) or {}

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "World"
    return jsonify({"message": f"Hello {name}!"}), 200
