# Python standard library
import json
import logging
import logging.handlers
import os
import sys
from functools import wraps
from typing import Callable

# Third-party libraries
from flask import jsonify, request

# Set API_KEY as a Cloud function environment variable
api_key = os.getenv("API_KEY")


class GCloudLogger:
    ALLOWED_LOG_METHODS = (
        "debug",
        "info",
        "notice",
        "warning",
        "error",
        "critical",
        "alert",
        "emergency",
    )

    LOG_LEVEL_MAP = {"notice": "info", "alert": "critical", "emergency": "critical"}

    def __init__(self, name: str = "gcloud-func", debug_mode=False):
        self.log = logging.getLogger(name)

        if self._running_locally():
            if debug_mode:
                self.log.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                    f"{name}: %(levelname)s: [%(funcName)s] %(message)s"
                )
            else:
                self.log.setLevel(logging.INFO)
                formatter = logging.Formatter(f"{name}: %(levelname)s: %(message)s")

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.log.addHandler(stream_handler)

    def _running_locally(self):
        return "K_SERVICE" not in os.environ

    def _send_log_message_to_gcloud(self, message, level):
        """
        Logs a message according to Google's Stackdriver specifications.
        """
        log_entry = {
            "severity": level.upper(),
            "message": message,
            "method": request.method,
            "endpoint": request.path,
            "urlFull": request.url,
            "urlParams": request.args,
            "headers": dict(request.headers),
            "payload": request.data.decode("utf-8"),
            "secure": request.is_secure,
        }
        print(json.dumps(log_entry))

    def __getattr__(self, name):
        if name in self.ALLOWED_LOG_METHODS:

            def log_method(fmt, *args):
                if not isinstance(fmt, str):
                    fmt = str(fmt)

                if args:
                    message = fmt % args
                else:
                    message = fmt

                if self._running_locally():
                    log_level = self.LOG_LEVEL_MAP.get(name, name)
                    getattr(self.log, log_level)(message)
                else:
                    self._send_log_message_to_gcloud(message, name)

            return log_method
        else:
            raise AttributeError(f"Log method '{name}' is not allowed.")


if os.getenv("DEBUG", "False").lower() in ("true", "t", "1"):
    log = GCloudLogger(debug_mode=True)
else:
    log = GCloudLogger()


def api_key_required(f: Callable) -> Callable:
    """
    Simple API key required decorator.
    Use this to enforce using a valid API key when accessing an endpoint.

    The recommendation by Google is to use the Google API Gateway to handle external
    authentication, but for my use case this simplifies the deployment and testing.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Not authorized"}), 401

        user_provided_api_key = auth_header.split("Bearer ")[1].strip()

        if user_provided_api_key == api_key:
            return f(*args, **kwargs)

        return jsonify({"error": "A valid authorization token is required"}), 401

    return decorator
