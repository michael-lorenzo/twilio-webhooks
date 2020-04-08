from typing import Callable, Dict, Optional

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from .utils import valid_request


class SMSCommand:
    def __init__(self, twilio_auth_token: str) -> None:
        self._commands: Dict[str, Callable[..., Optional[str]]] = {}
        self.twilio_auth_token: str = twilio_auth_token

    def assign(self, cmd: str, callback: Callable[..., Optional[str]]) -> None:
        """Assign a callback to a case-insensitive command string."""
        self._commands[cmd.casefold()] = callback

    def wsgi(self) -> Flask:
        """Flask application factory."""
        app = Flask(__name__)

        @app.route("/smscommand", methods=["GET", "POST"])
        def smscommand():
            if not valid_request(self.twilio_auth_token):
                return "", 403
            msg = self._run()
            if msg:
                mr = MessagingResponse()
                mr.message(msg)
                return str(mr)
            return "", 204

        return app

    def _run(self) -> Optional[str]:
        cmd, _, arg = request.form["Body"].lstrip().partition(" ")
        cmd = cmd.casefold()
        if cmd not in self._commands:
            return "Command not found."
        return str(self._commands[cmd](request.form["From"], arg))
