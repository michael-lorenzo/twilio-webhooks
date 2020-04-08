from flask import request
from twilio.request_validator import RequestValidator


def valid_request(twilio_auth_token: str) -> bool:
    return RequestValidator(twilio_auth_token).validate(
        request.url, request.form, request.headers["X-Twilio-Signature"]
    )
