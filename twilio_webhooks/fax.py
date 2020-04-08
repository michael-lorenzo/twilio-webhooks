import pathlib
from datetime import datetime

import requests
from flask import Flask, request
from twilio.twiml.fax_response import FaxResponse

from .utils import valid_request


class ReceiveFax:
    def __init__(self, twilio_auth_token: str, path) -> None:
        self.twilio_auth_token: str = twilio_auth_token
        self.path = pathlib.Path(path)

    def wsgi(self) -> Flask:
        """Flask application factory."""
        app = Flask(__name__)

        @app.route("/receivefax", methods=["GET", "POST"])
        def receivefax():
            if not valid_request(self.twilio_auth_token):
                return "", 403
            fr = FaxResponse()
            fr.receive("/receivefax/data")
            return str(fr)

        @app.route("/receivefax/data", methods=["POST"])
        def receivefax_data():
            if not valid_request(self.twilio_auth_token):
                return "", 403
            t = datetime.now().strftime("%Y%m%d_%H%M%S")
            with (self.path / f"{request.form['From'][1:]}_{t}.pdf").open("wb") as f:
                f.write(requests.get(request.form["MediaUrl"]).content)
            return "", 200

        return app
