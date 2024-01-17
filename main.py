# Third-party libraries
import functions_framework
from dotenv import load_dotenv
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

# Local imports
from app.endpoints.check import check
from app.endpoints.demo import demo
from app.utils import log

load_dotenv()

app = Flask("internal")


@app.errorhandler(HTTPException)
def handle_http_exception(err):
    if err.code >= 500:
        log.error(err.description)
    elif err.code not in (404, 405):
        log.warning(err.description)
    return jsonify({"error": err.description}), err.code


app.register_blueprint(check, url_prefix="/api/v1/")
app.register_blueprint(demo, url_prefix="/api/v1/demo")


@functions_framework.http
def main(request):
    """
    This is the entry point for the cloud function.
    This function overcomes Google Cloud Function's limitation of handling only one
    API route per function.
    This custom function creates an internal Flask app for routing requests to
    multiple API routes.
    Import the Flask app from main.py and use it as you would with a normal Flask app.

    Note: that this approach is not officially supported by Google,
    as they recommend one function per route, so use with caution.
    With that being said, it has worked for years.
    """
    # Create a new app context for the internal Flask app
    internal_ctx = app.test_request_context(
        path=request.full_path, method=request.method
    )

    # Copy the request data from original request.
    internal_ctx.request = request

    # Activate the context
    internal_ctx.push()
    # Dispatch the request to the internal app and get the result
    return_value = app.full_dispatch_request()
    # Offload the context
    internal_ctx.pop()

    # Return the result of the internal app routing and processing
    return return_value
